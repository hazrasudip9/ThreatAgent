#!/usr/bin/env python3
"""
ThreatAgent System Verification Script
=====================================

This script performs comprehensive system verification to ensure all components
are properly installed and configured for ThreatAgent operation.
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple

def check_file_exists(file_path: str, description: str) -> Tuple[bool, str]:
    """Check if a file exists and return status with message."""
    path = Path(file_path)
    if path.exists():
        size = path.stat().st_size
        return True, f"✅ {description}: {file_path} ({size:,} bytes)"
    else:
        return False, f"❌ {description}: {file_path} (NOT FOUND)"

def check_ollama_model(model_name: str) -> Tuple[bool, str]:
    """Check if Ollama model is available."""
    try:
        # Check if Ollama is running
        result = subprocess.run(
            ["curl", "-s", "http://localhost:11434/api/tags"],
            capture_output=True, text=True, timeout=10
        )
        
        if result.returncode != 0:
            return False, f"❌ Ollama service not running (curl failed)"
        
        # Check if model exists
        if model_name in result.stdout:
            return True, f"✅ Custom model: {model_name} (available)"
        else:
            return False, f"❌ Custom model: {model_name} (not found in Ollama)"
            
    except subprocess.TimeoutExpired:
        return False, f"❌ Ollama service: timeout (service may be down)"
    except Exception as e:
        return False, f"❌ Ollama check failed: {str(e)}"

def check_python_imports() -> Tuple[bool, str]:
    """Check if required Python modules can be imported."""
    required_modules = [
        "crewai", "langchain", "sqlite3", "yaml", "dotenv"
    ]
    
    missing_modules = []
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            missing_modules.append(module)
    
    if missing_modules:
        return False, f"❌ Missing Python modules: {', '.join(missing_modules)}"
    else:
        return True, f"✅ Python modules: All required modules available"

def check_environment_variables() -> Tuple[bool, str]:
    """Check if required environment variables are set."""
    # Check for .env file in multiple possible locations
    possible_env_files = [
        Path('.env'),
        Path('threatcrew/.env'),
        Path('../.env')
    ]
    
    env_file = None
    for env_path in possible_env_files:
        if env_path.exists():
            env_file = env_path
            break
    
    if not env_file:
        return False, f"❌ Environment: .env file not found in expected locations"
    
    required_vars = ["OLLAMA_API_BASE", "MODEL"]
    missing_vars = []
    
    # Load .env file manually
    try:
        with open(env_file, 'r') as f:
            for line in f:
                if '=' in line and not line.strip().startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value
    except Exception as e:
        return False, f"❌ Environment: Error reading .env file: {str(e)}"
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        return False, f"❌ Environment variables missing: {', '.join(missing_vars)}"
    else:
        return True, f"✅ Environment: All required variables set (from {env_file})"

def verify_system() -> Dict:
    """Perform comprehensive system verification."""
    
    print("🕵️ ThreatAgent System Verification")
    print("=" * 50)
    
    results = {
        "status": "unknown",
        "checks": [],
        "errors": [],
        "warnings": [],
        "summary": {}
    }
    
    # File checks
    file_checks = [
        ("src/knowledge/threat_memory.db", "Memory database"),
        ("knowledge/threat_intelligence_training.jsonl", "Training data"),
        ("knowledge/ThreatAgent.Modelfile", "Modelfile"),
        ("knowledge/setup_custom_model.sh", "Setup script"),
        (".env", "Environment file"),
        ("src/threatcrew/__init__.py", "Core package"),
        ("src/threatcrew/crew.py", "CrewAI configuration"),
    ]
    
    passed_checks = 0
    total_checks = len(file_checks) + 3  # +3 for Ollama, Python, Environment
    
    print("\n📁 File System Checks:")
    for file_path, description in file_checks:
        status, message = check_file_exists(file_path, description)
        print(f"   {message}")
        results["checks"].append({
            "type": "file",
            "description": description,
            "status": status,
            "message": message
        })
        if status:
            passed_checks += 1
        else:
            results["errors"].append(message)
    
    print("\n🐍 Python Environment Checks:")
    status, message = check_python_imports()
    print(f"   {message}")
    results["checks"].append({
        "type": "python",
        "description": "Python modules",
        "status": status,
        "message": message
    })
    if status:
        passed_checks += 1
    else:
        results["errors"].append(message)
    
    print("\n⚙️ Configuration Checks:")
    status, message = check_environment_variables()
    print(f"   {message}")
    results["checks"].append({
        "type": "config",
        "description": "Environment variables",
        "status": status,
        "message": message
    })
    if status:
        passed_checks += 1
    else:
        results["errors"].append(message)
    
    print("\n🤖 Ollama Model Checks:")
    status, message = check_ollama_model("threat-intelligence")
    print(f"   {message}")
    results["checks"].append({
        "type": "ollama",
        "description": "Ollama model",
        "status": status,
        "message": message
    })
    if status:
        passed_checks += 1
    else:
        results["warnings"].append(message)  # Ollama issues are warnings, not errors
    
    # System summary
    results["summary"] = {
        "total_checks": total_checks,
        "passed_checks": passed_checks,
        "failed_checks": total_checks - passed_checks,
        "success_rate": (passed_checks / total_checks) * 100
    }
    
    # Determine overall status
    if passed_checks == total_checks:
        results["status"] = "healthy"
        print("\n🚀 System Status: HEALTHY - Ready for production use!")
    elif passed_checks >= total_checks * 0.75:
        results["status"] = "warning"
        print(f"\n⚠️ System Status: WARNING - {passed_checks}/{total_checks} checks passed")
        print("   Some components may need attention but core functionality available")
    else:
        results["status"] = "error"
        print(f"\n❌ System Status: ERROR - {passed_checks}/{total_checks} checks passed")
        print("   Critical components missing, system may not function properly")
    
    # Show recommendations
    if results["errors"]:
        print("\n🔧 Required Actions:")
        for i, error in enumerate(results["errors"][:3], 1):  # Show first 3 errors
            print(f"   {i}. {error.replace('❌ ', '')}")
    
    if results["warnings"]:
        print("\n💡 Recommendations:")
        for i, warning in enumerate(results["warnings"][:2], 1):  # Show first 2 warnings
            print(f"   {i}. {warning.replace('❌ ', '')}")
    
    print(f"\n� Summary: {passed_checks}/{total_checks} checks passed ({results['summary']['success_rate']:.1f}%)")
    
    return results

def main():
    """Main entry point."""
    if len(sys.argv) > 1 and sys.argv[1] == "--json":
        # JSON output mode for programmatic usage
        results = verify_system()
        print("\n" + "="*50)
        print(json.dumps(results, indent=2))
    else:
        # Regular output mode for CLI usage
        verify_system()

if __name__ == "__main__":
    main()
