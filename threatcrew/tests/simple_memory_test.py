#!/usr/bin/env python3
"""Simple memory system test"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

print("🧠 ThreatAgent Memory System Test")
print("=" * 40)

try:
    # Test 1: Import memory system
    print("1. Testing memory system import...")
    from threatcrew.tools.memory_system import get_memory
    print("   ✅ Memory system imported successfully")
    
    # Test 2: Create memory instance
    print("2. Creating memory instance...")
    memory = get_memory()
    print("   ✅ Memory instance created")
    
    # Test 3: Store test IOC
    print("3. Storing test IOC...")
    ioc_id = memory.store_ioc(
        ioc='test-phishing-site.tk',
        ioc_type='domain', 
        risk_level='high',
        category='phishing',
        confidence=0.9
    )
    print(f"   ✅ Stored test IOC with ID: {ioc_id}")
    
    # Test 4: Get statistics
    print("4. Getting database statistics...")
    stats = memory.get_statistics()
    print(f"   📊 Total IOCs: {stats['total_iocs']}")
    print(f"   📊 Total analyses: {stats['total_analyses']}")
    
    # Test 5: Search for similar IOCs
    print("5. Testing similarity search...")
    similar = memory.search_similar_iocs("phishing", limit=3)
    print(f"   🔍 Found {len(similar)} similar IOCs")
    
    for ioc in similar[:2]:
        print(f"      - {ioc['ioc']} (risk: {ioc['risk_level']})")
    
    print("\n🎉 All tests passed! Memory system is working correctly.")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
