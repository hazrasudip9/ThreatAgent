#!/usr/bin/env python3
"""
Test Real Data Only Configuration
=================================

This script tests the real data only mode to ensure synthetic data is properly excluded.
"""

import os
import sys
import json
import tempfile

# Add the threatcrew module to the path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')
sys.path.insert(0, src_dir)

def test_real_data_only_mode():
    """Test that the system correctly uses only real data when configured."""
    print("🧪 Testing Real Data Only Mode")
    print("=" * 40)
    
    try:
        from threatcrew.tools.finetuning_system import ThreatFineTuner
        
        # Create a test finetuner
        with tempfile.TemporaryDirectory() as temp_dir:
            finetuner = ThreatFineTuner(training_data_dir=temp_dir)
            
            # Generate a dataset
            print("📊 Generating test dataset...")
            dataset_path = finetuner.generate_training_dataset()
            
            # Verify the dataset file was created
            if os.path.exists(dataset_path):
                print(f"✅ Dataset created: {dataset_path}")
                
                # Check if it's a real data dataset
                if "real_data" in os.path.basename(dataset_path):
                    print("✅ Dataset correctly labeled as 'real_data'")
                else:
                    print("⚠️  Dataset not labeled as real data")
                
                # Read and analyze the dataset content
                with open(dataset_path, 'r') as f:
                    lines = f.readlines()
                    
                print(f"📈 Dataset contains {len(lines)} training examples")
                
                # Check a few examples for synthetic content
                synthetic_indicators = ["secure-login-bank.tk", "malicious-site.com", "evil-domain.net"]
                real_data_count = 0
                synthetic_count = 0
                
                for line in lines[:10]:  # Check first 10 examples
                    try:
                        example = json.loads(line.strip())
                        input_data = example.get('input', '')
                        output_data = example.get('output', '')
                        
                        # Check if this looks like synthetic data
                        is_synthetic = any(indicator in input_data or indicator in output_data 
                                         for indicator in synthetic_indicators)
                        
                        if is_synthetic:
                            synthetic_count += 1
                            print(f"⚠️  Found potential synthetic data: {input_data[:50]}...")
                        else:
                            real_data_count += 1
                            
                    except json.JSONDecodeError:
                        continue
                
                print(f"📊 Analysis Results:")
                print(f"   Real data examples: {real_data_count}")
                print(f"   Synthetic examples detected: {synthetic_count}")
                
                if synthetic_count == 0:
                    print("✅ SUCCESS: No synthetic data detected in real-data-only mode!")
                else:
                    print("❌ WARNING: Synthetic data found in real-data-only mode")
                
                return synthetic_count == 0
                
            else:
                print("❌ Dataset file was not created")
                return False
                
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        return False

def test_configuration_values():
    """Test that configuration values are correctly set for real data only mode."""
    print("\n🔧 Testing Configuration Values")
    print("=" * 40)
    
    try:
        from threatcrew.config.data_source_config import DATA_SOURCE_CONFIG, TRAINING_CONFIG
        
        # Check key configuration values
        use_real_only = DATA_SOURCE_CONFIG.get("USE_REAL_DATA_ONLY", False)
        disable_synthetic = DATA_SOURCE_CONFIG.get("DISABLE_SYNTHETIC_DATA", False)
        excluded_sources = DATA_SOURCE_CONFIG.get("EXCLUDED_DATA_SOURCES", [])
        
        print(f"USE_REAL_DATA_ONLY: {use_real_only}")
        print(f"DISABLE_SYNTHETIC_DATA: {disable_synthetic}")
        print(f"EXCLUDED_DATA_SOURCES: {excluded_sources}")
        
        # Verify correct settings
        if use_real_only and disable_synthetic:
            print("✅ Configuration correctly set for real data only mode")
            return True
        else:
            print("❌ Configuration not properly set for real data only mode")
            return False
            
    except ImportError as e:
        print(f"❌ Could not import configuration: {e}")
        return False

def main():
    """Run all tests."""
    print("🕵️ ThreatAgent Real Data Only Mode Test Suite")
    print("=" * 50)
    
    # Test configuration
    config_test = test_configuration_values()
    
    # Test dataset generation
    dataset_test = test_real_data_only_mode()
    
    # Summary
    print("\n📋 Test Summary")
    print("=" * 20)
    print(f"Configuration Test: {'✅ PASS' if config_test else '❌ FAIL'}")
    print(f"Dataset Generation Test: {'✅ PASS' if dataset_test else '❌ FAIL'}")
    
    if config_test and dataset_test:
        print("\n🎉 All tests passed! Real data only mode is working correctly.")
        return True
    else:
        print("\n⚠️  Some tests failed. Please check the configuration.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
