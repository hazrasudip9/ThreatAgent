#!/usr/bin/env python3
"""
ThreatAgent Data Source Configuration Tool
=========================================

This script helps configure the ThreatAgent system to use only real threat intelligence
datasets or allow mixed real/synthetic data for training.
"""

import os
import sys
import json
from pathlib import Path

# Add the threatcrew module to the path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')
sys.path.insert(0, src_dir)

try:
    from threatcrew.config.data_source_config import DATA_SOURCE_CONFIG, TRAINING_CONFIG
except ImportError:
    # Fallback to direct file reading if module import fails
    config_file = os.path.join(current_dir, 'src', 'threatcrew', 'config', 'data_source_config.py')
    if os.path.exists(config_file):
        import importlib.util
        spec = importlib.util.spec_from_file_location("data_source_config", config_file)
        config_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(config_module)
        DATA_SOURCE_CONFIG = config_module.DATA_SOURCE_CONFIG
        TRAINING_CONFIG = config_module.TRAINING_CONFIG
    else:
        # Default configuration if file doesn't exist
        DATA_SOURCE_CONFIG = {
            "USE_REAL_DATA_ONLY": True,
            "DISABLE_SYNTHETIC_DATA": True,
            "MIN_CONFIDENCE_THRESHOLD": 0.5,
            "MAX_EXAMPLES_PER_CATEGORY": 1000,
            "ALLOWED_DATA_SOURCES": ["memory_database", "historical_analysis", "real_iocs", "actual_reports"],
            "EXCLUDED_DATA_SOURCES": ["synthetic", "generated", "example", "demo", "test"]
        }
        TRAINING_CONFIG = {
            "VERIFIED_DATA_ONLY": True,
            "REQUIRE_SOURCE_ATTRIBUTION": True,
            "FILTER_SUSPICIOUS_PATTERNS": True
        }


def set_real_data_only_mode(enabled: bool = True):
    """
    Configure the system to use only real threat intelligence data.
    
    Args:
        enabled: True to enable real data only mode, False to allow mixed data
    """
    config_file = os.path.join(os.path.dirname(__file__), '..', 'src', 'threatcrew', 'config', 'data_source_config.py')
    
    # Read current configuration
    with open(config_file, 'r') as f:
        content = f.read()
    
    # Update configuration values
    new_content = content.replace(
        '"USE_REAL_DATA_ONLY": True' if enabled else '"USE_REAL_DATA_ONLY": False',
        f'"USE_REAL_DATA_ONLY": {enabled}'
    ).replace(
        '"DISABLE_SYNTHETIC_DATA": True' if enabled else '"DISABLE_SYNTHETIC_DATA": False',
        f'"DISABLE_SYNTHETIC_DATA": {enabled}'
    )
    
    # Write updated configuration
    with open(config_file, 'w') as f:
        f.write(new_content)
    
    mode = "REAL DATA ONLY" if enabled else "MIXED DATA"
    print(f"✅ ThreatAgent configured for {mode} mode")
    print(f"📁 Configuration updated: {config_file}")


def show_current_config():
    """Display the current data source configuration."""
    print("🔧 Current ThreatAgent Data Source Configuration:")
    print("=" * 50)
    print(f"Use Real Data Only: {DATA_SOURCE_CONFIG['USE_REAL_DATA_ONLY']}")
    print(f"Disable Synthetic Data: {DATA_SOURCE_CONFIG['DISABLE_SYNTHETIC_DATA']}")
    print(f"Min Confidence Threshold: {DATA_SOURCE_CONFIG['MIN_CONFIDENCE_THRESHOLD']}")
    print(f"Max Examples Per Category: {DATA_SOURCE_CONFIG['MAX_EXAMPLES_PER_CATEGORY']}")
    print(f"Allowed Data Sources: {', '.join(DATA_SOURCE_CONFIG['ALLOWED_DATA_SOURCES'])}")
    print(f"Excluded Data Sources: {', '.join(DATA_SOURCE_CONFIG['EXCLUDED_DATA_SOURCES'])}")
    print()
    print("🎯 Training Configuration:")
    print(f"Verified Data Only: {TRAINING_CONFIG['VERIFIED_DATA_ONLY']}")
    print(f"Require Source Attribution: {TRAINING_CONFIG['REQUIRE_SOURCE_ATTRIBUTION']}")
    print(f"Filter Suspicious Patterns: {TRAINING_CONFIG['FILTER_SUSPICIOUS_PATTERNS']}")


def validate_real_data_availability():
    """Check if sufficient real threat intelligence data is available."""
    try:
        from threatcrew.tools.memory_system import get_memory
        import sqlite3
        
        memory = get_memory()
        db_path = memory.db_path if hasattr(memory, 'db_path') else memory
        
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            
            # Check IOCs
            cursor.execute("SELECT COUNT(*) FROM iocs WHERE source NOT LIKE '%demo%' AND source NOT LIKE '%synthetic%'")
            real_iocs = cursor.fetchone()[0]
            
            # Check analysis history
            cursor.execute("SELECT COUNT(*) FROM analysis_history WHERE input_data IS NOT NULL")
            analysis_records = cursor.fetchone()[0]
            
            print("📊 Real Data Availability Assessment:")
            print("=" * 40)
            print(f"Real IOCs in database: {real_iocs}")
            print(f"Analysis history records: {analysis_records}")
            
            if real_iocs < 10:
                print("⚠️  WARNING: Limited real IOC data available!")
                print("   Consider importing more real threat intelligence before enabling real-data-only mode.")
            else:
                print("✅ Sufficient real data available for training")
                
            return real_iocs >= 10
            
    except Exception as e:
        print(f"❌ Error checking data availability: {e}")
        return False


def main():
    """Main configuration interface."""
    print("🕵️ ThreatAgent Data Source Configuration Tool")
    print("=" * 50)
    
    if len(sys.argv) < 2:
        show_current_config()
        print("\nUsage:")
        print("  python configure_data_sources.py show              # Show current configuration")
        print("  python configure_data_sources.py real-only         # Enable real data only mode")
        print("  python configure_data_sources.py mixed             # Enable mixed data mode")
        print("  python configure_data_sources.py validate          # Check data availability")
        return
    
    command = sys.argv[1].lower()
    
    if command == "show":
        show_current_config()
    elif command == "real-only":
        if validate_real_data_availability():
            set_real_data_only_mode(True)
            print("\n✅ System configured to use ONLY real threat intelligence data")
            print("🚫 Synthetic data generation has been DISABLED")
        else:
            print("\n⚠️  Insufficient real data available. Import more real threat intelligence first.")
    elif command == "mixed":
        set_real_data_only_mode(False)
        print("\n✅ System configured to use MIXED real and synthetic data")
        print("🔄 Synthetic data generation has been ENABLED")
    elif command == "validate":
        validate_real_data_availability()
    else:
        print(f"❌ Unknown command: {command}")
        print("Valid commands: show, real-only, mixed, validate")


if __name__ == "__main__":
    main()
