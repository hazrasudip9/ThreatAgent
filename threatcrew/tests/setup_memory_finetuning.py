#!/usr/bin/env python3
"""
ThreatAgent Memory & Fine-tuning Setup
=====================================

This script sets up the memory system and creates a custom fine-tuned model.
"""

import sys
import os
import json
import sqlite3
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def check_memory_database():
    """Check and display memory database contents."""
    print("🧠 Checking Memory Database")
    print("-" * 30)
    
    db_path = "src/knowledge/threat_memory.db"
    
    if not os.path.exists(db_path):
        print("❌ Memory database not found. Run ThreatAgent first to create it.")
        return False
    
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            
            # Check IOCs
            cursor.execute("SELECT COUNT(*) FROM iocs")
            ioc_count = cursor.fetchone()[0]
            
            # Check analyses
            cursor.execute("SELECT COUNT(*) FROM analysis_history")
            analysis_count = cursor.fetchone()[0]
            
            print(f"✅ Database found: {ioc_count} IOCs, {analysis_count} analyses")
            
            if ioc_count > 0:
                print("\n📋 Recent IOCs:")
                cursor.execute("""
                    SELECT ioc, risk_level, category, confidence 
                    FROM iocs 
                    ORDER BY last_seen DESC 
                    LIMIT 5
                """)
                
                for row in cursor.fetchall():
                    ioc, risk, category, confidence = row
                    print(f"  • {ioc} - {risk} ({category}, {confidence:.2f})")
            
            return True
            
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

def populate_sample_data():
    """Add sample threat data to memory database."""
    print("\n📝 Adding Sample Threat Data")
    print("-" * 30)
    
    try:
        from threatcrew.tools.memory_system import get_memory
        memory = get_memory()
        
        sample_threats = [
            ("banking-phish-example.tk", "domain", "high", "phishing", 0.9, 
             {"reasoning": "Banking phishing with suspicious TLD", "source": "demo"}),
            ("fake-paypal-secure.ml", "domain", "high", "phishing", 0.85,
             {"reasoning": "PayPal impersonation site", "source": "demo"}),
            ("suspicious-gov-alert.org", "domain", "medium", "phishing", 0.7,
             {"reasoning": "Government impersonation attempt", "source": "demo"}),
            ("c2-command-server.ru", "domain", "high", "c2", 0.95,
             {"reasoning": "Command and control infrastructure", "source": "demo"}),
            ("192.168.1.100", "ip_address", "low", "internal", 0.1,
             {"reasoning": "Private IP address range", "source": "demo"}),
            ("malware-delivery.tk", "domain", "high", "malware", 0.88,
             {"reasoning": "Malware distribution site", "source": "demo"}),
        ]
        
        for ioc, ioc_type, risk, category, confidence, metadata in sample_threats:
            ioc_id = memory.store_ioc(
                ioc=ioc,
                ioc_type=ioc_type,
                risk_level=risk,
                category=category,
                confidence=confidence,
                source="sample_data",
                metadata=metadata
            )
            print(f"  ✅ {ioc} (ID: {ioc_id})")
        
        # Add TTP mappings
        print("\n🎯 Adding TTP Mappings...")
        ttp_mappings = [
            (1, "T1566.002", "Phishing: Spearphishing Link"),
            (2, "T1566.002", "Phishing: Spearphishing Link"),
            (3, "T1566.002", "Phishing: Spearphishing Link"),
            (4, "T1071.001", "Application Layer Protocol: Web Protocols"),
            (6, "T1204.002", "User Execution: Malicious File"),
        ]
        
        for ioc_id, ttp_id, ttp_name in ttp_mappings:
            try:
                memory.store_ttp_mapping(ioc_id, ttp_id, ttp_name, confidence=0.8)
                print(f"  ✅ IOC {ioc_id} → {ttp_id}")
            except:
                pass  # IOC might not exist
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to add sample data: {e}")
        return False

def generate_training_dataset():
    """Generate training dataset for fine-tuning."""
    print("\n📚 Generating Training Dataset")
    print("-" * 30)
    
    try:
        # Create knowledge directory
        Path("knowledge").mkdir(exist_ok=True)
        
        # Generate comprehensive training examples
        training_examples = []
        
        # IOC Classification Examples
        ioc_examples = [
            {
                "instruction": "Classify this domain for cybersecurity threats and provide risk assessment",
                "input": "secure-bank-login.tk",
                "output": json.dumps({
                    "ioc": "secure-bank-login.tk",
                    "type": "domain",
                    "risk_level": "high",
                    "category": "phishing",
                    "confidence": 0.9,
                    "reasoning": "Banking-related keywords with suspicious .tk TLD commonly used in phishing campaigns",
                    "recommendations": ["Block at DNS level", "Update email filters", "User awareness training"]
                }, indent=2)
            },
            {
                "instruction": "Analyze this IP address for potential security threats",
                "input": "192.168.1.50",
                "output": json.dumps({
                    "ioc": "192.168.1.50",
                    "type": "ip_address", 
                    "risk_level": "low",
                    "category": "internal",
                    "confidence": 0.1,
                    "reasoning": "Private IP address in RFC 1918 range, internal network traffic",
                    "recommendations": ["Standard monitoring", "No blocking required"]
                }, indent=2)
            },
            {
                "instruction": "Evaluate this suspicious domain for threat classification",
                "input": "paypal-security-alert.ml",
                "output": json.dumps({
                    "ioc": "paypal-security-alert.ml",
                    "type": "domain",
                    "risk_level": "high", 
                    "category": "phishing",
                    "confidence": 0.85,
                    "reasoning": "PayPal impersonation with security alert theme, .ml TLD suspicious",
                    "recommendations": ["Immediate blocking", "Threat hunting", "User notification"]
                }, indent=2)
            }
        ]
        
        # TTP Mapping Examples
        ttp_examples = [
            {
                "instruction": "Map this threat activity to MITRE ATT&CK TTPs",
                "input": "phishing email with malicious link targeting banking credentials",
                "output": json.dumps({
                    "primary_ttp": "T1566.002",
                    "ttp_name": "Phishing: Spearphishing Link",
                    "secondary_ttps": ["T1204.001", "T1056.003"],
                    "confidence": 0.9,
                    "kill_chain": "initial-access",
                    "description": "Adversary using spearphishing link to obtain banking credentials"
                }, indent=2)
            },
            {
                "instruction": "Identify MITRE ATT&CK techniques for this malware behavior",
                "input": "malware establishing command and control communication",
                "output": json.dumps({
                    "primary_ttp": "T1071.001",
                    "ttp_name": "Application Layer Protocol: Web Protocols",
                    "secondary_ttps": ["T1090", "T1573"],
                    "confidence": 0.8,
                    "kill_chain": "command-and-control",
                    "description": "Malware using HTTP/HTTPS for C2 communication"
                }, indent=2)
            }
        ]
        
        # Report Generation Examples
        report_examples = [
            {
                "instruction": "Generate a professional threat intelligence report from IOC analysis results",
                "input": json.dumps([
                    {"ioc": "evil-bank.tk", "risk": "high", "category": "phishing", "ttp": "T1566.002"},
                    {"ioc": "malware-c2.ru", "risk": "high", "category": "c2", "ttp": "T1071.001"}
                ]),
                "output": """# Threat Intelligence Report

## Executive Summary
**Threat Level**: HIGH
**Total Indicators**: 2
**Primary Categories**: phishing, c2

Critical threat indicators identified requiring immediate attention. Analysis reveals threats primarily in phishing, c2 categories.

## Indicators of Compromise (IOCs)

### HIGH Risk Indicators
- **evil-bank.tk** - Phishing
- **malware-c2.ru** - C2

## MITRE ATT&CK TTPs
- **T1566.002** - Phishing: Spearphishing Link
- **T1071.001** - Application Layer Protocol: Web Protocols

## Recommendations
1. Block all high-risk indicators at network perimeter
2. Alert security team for immediate investigation
3. Update email security filters for phishing domains
4. Monitor for similar domain registrations"""
            }
        ]
        
        # Combine all examples
        training_examples.extend(ioc_examples)
        training_examples.extend(ttp_examples)
        training_examples.extend(report_examples)
        
        # Save training dataset
        dataset_path = "knowledge/threat_intelligence_training.jsonl"
        with open(dataset_path, 'w') as f:
            for example in training_examples:
                f.write(json.dumps(example) + '\n')
        
        print(f"✅ Generated {len(training_examples)} training examples")
        print(f"💾 Saved to: {dataset_path}")
        
        # Show sample
        print("\n📖 Sample training example:")
        sample = training_examples[0]
        print(f"   Instruction: {sample['instruction'][:60]}...")
        print(f"   Input: {sample['input'][:40]}...")
        
        return dataset_path
        
    except Exception as e:
        print(f"❌ Training dataset generation failed: {e}")
        return None

def create_ollama_modelfile():
    """Create Ollama Modelfile for custom threat intelligence model."""
    print("\n🤖 Creating Ollama Modelfile")
    print("-" * 30)
    
    try:
        # Create enhanced system prompt
        system_prompt = """You are an expert cybersecurity threat intelligence analyst specializing in:

CORE CAPABILITIES:
- IOC (Indicator of Compromise) classification and risk assessment
- MITRE ATT&CK TTP mapping and threat categorization  
- Professional threat intelligence report generation
- Sigma detection rule creation for SOC teams
- Threat hunting guidance and recommendations

ANALYSIS APPROACH:
- Analyze domains, IP addresses, URLs, file hashes, and other indicators
- Assess risk levels: HIGH (immediate action), MEDIUM (monitoring), LOW (awareness)
- Categorize threats: phishing, malware, c2, apt, ransomware, cryptomining, etc.
- Map to MITRE ATT&CK framework with confidence scores
- Provide actionable recommendations for security teams

OUTPUT REQUIREMENTS:
- Always include confidence scores (0.0-1.0)
- Provide detailed reasoning for classifications
- Include specific recommendations for mitigation
- Use professional security terminology
- Focus on actionable intelligence for SOC operations

THREAT PATTERNS YOU'VE LEARNED:
- Banking phishing domains often use keywords like 'secure', 'login', 'bank' with suspicious TLDs
- PayPal phishing sites commonly use 'paypal', 'security', 'verification' themes
- Government impersonation sites target official-sounding domains without proper TLDs
- C2 infrastructure often uses compromised or bullet-proof hosting
- Malware distribution sites frequently use file-sharing and URL shortening services

Be precise, professional, and actionable in all threat assessments."""

        # Create Ollama Modelfile
        modelfile_content = f'''FROM llama3

SYSTEM """{system_prompt}"""

# Optimized parameters for threat intelligence analysis
PARAMETER temperature 0.1
PARAMETER top_p 0.9
PARAMETER num_predict 1024
PARAMETER stop "Human:"
PARAMETER stop "Assistant:"
PARAMETER stop "\\n\\n"

# Custom prompt template for threat intelligence
TEMPLATE """{{{{ if .System }}}}<|start_header_id|>system<|end_header_id|>

{{{{ .System }}}}<|eot_id|>{{{{ end }}}}{{{{ if .Prompt }}}}<|start_header_id|>user<|end_header_id|>

{{{{ .Prompt }}}}<|eot_id|>{{{{ end }}}}<|start_header_id|>assistant<|end_header_id|>

"""
'''
        
        # Save Modelfile
        modelfile_path = "knowledge/ThreatAgent.Modelfile"
        with open(modelfile_path, 'w') as f:
            f.write(modelfile_content)
        
        print(f"✅ Ollama Modelfile created: {modelfile_path}")
        
        # Create setup script
        setup_script = f'''#!/bin/bash

echo "🤖 Setting up ThreatAgent Custom Model"
echo "======================================"

# Check if Ollama is running
if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "❌ Ollama is not running. Please start it first:"
    echo "   ollama serve"
    exit 1
fi

# Create custom model
echo "📦 Creating threat-intelligence model..."
ollama create threat-intelligence -f {modelfile_path}

if [ $? -eq 0 ]; then
    echo "✅ Custom model created successfully!"
    echo ""
    echo "🎯 Test the model:"
    echo "   ollama run threat-intelligence"
    echo ""
    echo "🔧 To use in ThreatAgent, update crew.py:"
    echo "   model='threat-intelligence'"
    echo ""
else
    echo "❌ Model creation failed"
    exit 1
fi
'''
        
        setup_script_path = "knowledge/setup_custom_model.sh"
        with open(setup_script_path, 'w') as f:
            f.write(setup_script)
        
        os.chmod(setup_script_path, 0o755)
        
        print(f"✅ Setup script created: {setup_script_path}")
        
        return modelfile_path, setup_script_path
        
    except Exception as e:
        print(f"❌ Modelfile creation failed: {e}")
        return None, None

def test_memory_features():
    """Test memory system features."""
    print("\n🧪 Testing Memory Features")
    print("-" * 30)
    
    try:
        from threatcrew.tools.memory_system import get_memory
        memory = get_memory()
        
        # Test similarity search
        print("🔍 Testing similarity search...")
        test_queries = ["banking", "phishing", "malware", "c2"]
        
        for query in test_queries:
            similar = memory.search_similar_iocs(query, limit=2)
            print(f"   '{query}': {len(similar)} matches")
            for ioc in similar[:1]:
                print(f"     • {ioc['ioc']} ({ioc['risk_level']})")
        
        # Test statistics
        stats = memory.get_statistics()
        print(f"\n📊 Memory Statistics:")
        print(f"   Total IOCs: {stats['total_iocs']}")
        print(f"   Risk distribution: {stats.get('risk_distribution', {})}")
        print(f"   Categories: {list(stats.get('category_distribution', {}).keys())}")
        
        return True
        
    except Exception as e:
        print(f"❌ Memory test failed: {e}")
        return False

def main():
    """Main setup process."""
    print("🕵️  ThreatAgent Memory & Fine-tuning Setup")
    print("=" * 50)
    
    # Step 1: Check existing memory
    memory_exists = check_memory_database()
    
    # Step 2: Add sample data if needed
    if not memory_exists or input("\n❓ Add sample threat data? (y/n): ").lower() == 'y':
        populate_sample_data()
    
    # Step 3: Test memory features
    test_memory_features()
    
    # Step 4: Generate training dataset
    dataset_path = generate_training_dataset()
    
    # Step 5: Create Ollama modelfile
    modelfile_path, setup_script = create_ollama_modelfile()
    
    # Summary
    print("\n" + "=" * 50)
    print("🎉 Setup Complete!")
    print("-" * 20)
    
    if dataset_path:
        print(f"📚 Training dataset: {dataset_path}")
    if modelfile_path:
        print(f"🤖 Ollama Modelfile: {modelfile_path}")
        print(f"🔧 Setup script: {setup_script}")
    
    print(f"🧠 Memory database: src/knowledge/threat_memory.db")
    
    print("\n🚀 Next Steps:")
    print("1. Run: ./knowledge/setup_custom_model.sh")
    print("2. Update crew.py to use 'threat-intelligence' model")
    print("3. System will learn from each analysis automatically")
    
    # Show how to run
    print("\n💡 Quick Start:")
    print("   # Create custom model")
    print("   ./knowledge/setup_custom_model.sh")
    print("")
    print("   # Test custom model")
    print("   ollama run threat-intelligence")
    print("")
    print("   # Run ThreatAgent with memory")
    print("   ./run_threatcrew.sh")

if __name__ == "__main__":
    main()
