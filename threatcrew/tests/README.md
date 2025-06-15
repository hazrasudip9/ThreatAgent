# 🧪 ThreatAgent Testing Suite

This directory contains all test scripts and demos for ThreatAgent's memory-enhanced threat intelligence system.

## 📋 Test Organization

**Main Test Suite:** `../../test_threatcrew_all.py` (root directory)
**Test Scripts:** All scripts in this `tests/` directory
**Test Results:** 11/11 tests passing (100% success rate)

## 🧪 Test Files & Scripts

### System Validation

#### `verify_system.py`
**Comprehensive System Health Check**

Validates all system components and dependencies:

```bash
# Test coverage:
- File system checks (7 components)
- Python module validation
- Environment configuration
- Ollama model availability
- Memory database integrity
- Training data validation

# Run test:
python3 verify_system.py
```

#### `simple_memory_test.py`
**Memory System Testing**

Tests database operations and memory functionality:

```bash
# Test coverage:
- Memory system imports
- Database connections
- IOC storage and retrieval
- Similarity search
- Statistics generation

# Run test:
python3 simple_memory_test.py
```

**Expected Output:**
```
🔍 ThreatCrew System Test
==================================================
=== Testing LLM Connection ===
✅ LLM Response: Custom threat intelligence model ready

=== Testing Individual Tools ===
1. Testing OSINT Scraper...
   ✅ Found domains: ['login-hdfcbank.in', 'secure-paypal-alert.net']

2. Testing IOC Classifier...  
   ✅ Classifications: [{'ioc': 'login-hdfcbank.in', 'risk': 'high', 'category': 'phishing'}]

3. Testing TTP Mapper...
   ✅ TTPs: [{'ttp': 'T1566.002', 'confidence': 0.9}]

4. Testing Report Writer...
   ✅ Report generated: 245 characters

5. Testing Rule Generator...
   ✅ Rules generated: 512 characters

==================================================
✅ ALL TESTS PASSED!
```

---

### Memory System Tests

#### `test_memory_system.py`
**Comprehensive Memory Database Testing**

Tests all memory system capabilities:

```python
# Test coverage:
- Database initialization and schema validation
- IOC storage and retrieval operations
- Vector similarity search functionality
- Analysis history tracking
- TTP mapping storage and queries
- Statistical analysis and reporting
- Error handling and edge cases

# Run test:
python3 test_memory_system.py
```

#### `simple_memory_test.py`
**Quick Memory Validation**

Lightweight test for memory system basics:

```python
# Test coverage:
- Memory system import and initialization
- Basic IOC storage operation
- Simple similarity search
- Database statistics retrieval

# Run test:
python3 simple_memory_test.py
```

**Expected Output:**
```
🧠 ThreatAgent Memory System Test
========================================
1. Testing memory system import...
   ✅ Memory system imported successfully

2. Creating memory instance...
   ✅ Memory instance created

3. Storing test IOC...
   ✅ Stored test IOC with ID: 1

4. Getting database statistics...
   📊 Total IOCs: 7
   📊 Total analyses: 0

5. Testing similarity search...
   🔍 Found 3 similar IOCs
      - suspicious-gov-alert.org (risk: medium)
      - fake-paypal-secure.ml (risk: high)

🎉 All tests passed! Memory system is working correctly.
```

---

### System Verification Tests

#### `verify_system.py`
**Complete System Health Check**

Validates entire ThreatAgent installation:

```python
# Verification checklist:
- Memory database existence and population
- Custom model availability and functionality
- Training dataset generation and quality
- Configuration file completeness
- Tool integration status
- Performance benchmarks

# Run verification:
python3 verify_system.py
```

**Expected Output:**
```
🕵️ ThreatAgent System Verification
==================================================
✅ Memory database exists (7 IOCs stored)
✅ Custom threat-intelligence model installed
✅ Training dataset generated (6 examples)
✅ Setup scripts created and executable
🚀 System ready for production use!
```

---

## 🎯 Specialized Tests

### Custom Model Testing

#### Direct Model Testing
```bash
# Test custom model directly
ollama run threat-intelligence "Analyze domain: test-phishing.tk" --format json

# Expected: Structured JSON response with threat analysis
```

#### Model Performance Testing
```python
# Performance benchmarks
import time
from threatcrew.tools.llm_classifier import run

start_time = time.time()
result = run(['suspicious-site.tk'])
end_time = time.time()

print(f"Classification time: {end_time - start_time:.2f}s")
print(f"Result quality: {len(result[0].get('reasoning', ''))}")
```

### Memory System Stress Testing

#### Large Dataset Testing
```python
# Test with large numbers of IOCs
from threatcrew.tools.memory_system import get_memory

memory = get_memory()

# Store 1000 test IOCs
for i in range(1000):
    memory.store_ioc(
        ioc=f"test-{i}.example.com",
        ioc_type="domain",
        risk_level="medium",
        category="test",
        confidence=0.5
    )

# Test similarity search performance
import time
start = time.time()
similar = memory.search_similar_iocs("test-query", threshold=0.7)
end = time.time()

print(f"Search time for 1000 IOCs: {end - start:.3f}s")
```

#### Vector Search Performance
```python
# Test vector embedding performance
from threatcrew.tools.memory_system import get_memory

memory = get_memory()

# Test batch similarity searches
test_queries = [
    "banking-phish.tk",
    "paypal-secure.ml", 
    "government-alert.org",
    "malware-c2.ru"
]

for query in test_queries:
    start = time.time()
    results = memory.search_similar_iocs(query, threshold=0.6)
    end = time.time()
    print(f"Query '{query}': {len(results)} results in {end-start:.3f}s")
```

---

## 🔄 Automated Testing

### Continuous Integration Tests

#### `run_tests.sh`
**Complete Test Suite Runner**

Automated script that runs all tests:

```bash
#!/bin/bash
echo "🧪 Running ThreatAgent Test Suite"
echo "================================="

# Set Python path
export PYTHONPATH="$(pwd)/src"

# Run basic tests
echo "1. Running basic component tests..."
python3 test_simple.py

# Run memory tests
echo "2. Running memory system tests..."
python3 simple_memory_test.py

# Run system verification
echo "3. Running system verification..."
python3 verify_system.py

# Test custom model if available
echo "4. Testing custom model..."
if ollama list | grep -q "threat-intelligence"; then
    echo "Testing custom model response..."
    ollama run threat-intelligence "Test: example.com" >/dev/null 2>&1
    if [ $? -eq 0 ]; then
        echo "✅ Custom model working"
    else
        echo "❌ Custom model test failed"
    fi
else
    echo "⚠️ Custom model not found"
fi

echo "✅ Test suite completed!"
```

### Performance Benchmarking

#### Memory Performance Tests
```python
def benchmark_memory_operations():
    """Benchmark key memory operations"""
    from threatcrew.tools.memory_system import get_memory
    import time
    
    memory = get_memory()
    
    # Benchmark IOC storage
    start = time.time()
    for i in range(100):
        memory.store_ioc(f"bench-{i}.com", "domain", "low", "test", 0.5)
    storage_time = time.time() - start
    
    # Benchmark similarity search
    start = time.time()
    results = memory.search_similar_iocs("banking", threshold=0.7)
    search_time = time.time() - start
    
    # Benchmark statistics
    start = time.time()
    stats = memory.get_statistics()
    stats_time = time.time() - start
    
    print(f"Storage (100 IOCs): {storage_time:.3f}s")
    print(f"Similarity search: {search_time:.3f}s") 
    print(f"Statistics query: {stats_time:.3f}s")
```

---

## 🎯 Test Data Management

### Test Database Setup
```python
def setup_test_database():
    """Create isolated test database"""
    import tempfile
    import os
    
    # Create temporary database for testing
    test_db = tempfile.NamedTemporaryFile(suffix='.db', delete=False)
    os.environ['TEST_MEMORY_DB'] = test_db.name
    
    # Initialize with test data
    from threatcrew.tools.memory_system import ThreatMemoryDB
    memory = ThreatMemoryDB(test_db.name)
    
    # Add sample test data
    test_iocs = [
        ("test-phishing.tk", "domain", "high", "phishing", 0.9),
        ("test-malware.ml", "domain", "high", "malware", 0.85),
        ("192.168.1.100", "ip_address", "low", "internal", 0.1)
    ]
    
    for ioc, ioc_type, risk, category, confidence in test_iocs:
        memory.store_ioc(ioc, ioc_type, risk, category, confidence)
    
    return test_db.name
```

### Test Data Cleanup
```python
def cleanup_test_data():
    """Clean up test database and temporary files"""
    import os
    
    test_db = os.environ.get('TEST_MEMORY_DB')
    if test_db and os.path.exists(test_db):
        os.unlink(test_db)
        del os.environ['TEST_MEMORY_DB']
```

---

## 🚀 Advanced Testing

### Integration Testing

#### End-to-End Workflow Test
```python
def test_complete_workflow():
    """Test complete threat analysis workflow"""
    
    # 1. Setup test environment
    test_db = setup_test_database()
    
    try:
        # 2. Run OSINT collection
        from threatcrew.tools.osint_scraper import run as osint_run
        domains = osint_run()
        
        # 3. Run classification with memory
        from threatcrew.tools.llm_classifier import run as classify_run
        classifications = classify_run(domains)
        
        # 4. Run TTP mapping
        from threatcrew.tools.ttp_mapper import run as ttp_run
        ttps = ttp_run(classifications)
        
        # 5. Generate reports
        from threatcrew.tools.report_writer import run as report_run
        report = report_run(ttps)
        
        # 6. Validate memory storage
        from threatcrew.tools.memory_system import get_memory
        memory = get_memory()
        stats = memory.get_statistics()
        
        # Assertions
        assert len(domains) > 0, "OSINT should find domains"
        assert len(classifications) > 0, "Classification should process domains"
        assert len(report) > 100, "Report should be substantial"
        assert stats['total_iocs'] > 0, "Memory should store results"
        
        print("✅ Complete workflow test passed")
        
    finally:
        cleanup_test_data()
```

### Load Testing

#### High-Volume IOC Processing
```python
def test_high_volume_processing():
    """Test system performance with high IOC volumes"""
    import concurrent.futures
    import time
    
    # Generate large test dataset
    test_iocs = [f"test-{i}.example.com" for i in range(1000)]
    
    # Test concurrent processing
    start_time = time.time()
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = []
        for batch in batch_split(test_iocs, 100):
            future = executor.submit(process_ioc_batch, batch)
            futures.append(future)
        
        # Wait for completion
        concurrent.futures.wait(futures)
    
    end_time = time.time()
    
    print(f"Processed 1000 IOCs in {end_time - start_time:.2f}s")
    print(f"Throughput: {1000 / (end_time - start_time):.1f} IOCs/sec")
```

---

## 📊 Test Reporting

### Test Results Dashboard

#### Coverage Report
```python
def generate_coverage_report():
    """Generate test coverage report"""
    
    components = {
        'Memory System': test_memory_system(),
        'Custom Model': test_custom_model(),
        'Tool Integration': test_tool_integration(),
        'End-to-End Workflow': test_complete_workflow()
    }
    
    print("📊 ThreatAgent Test Coverage Report")
    print("=" * 40)
    
    for component, status in components.items():
        status_icon = "✅" if status else "❌"
        print(f"{status_icon} {component}")
    
    coverage_percent = (sum(components.values()) / len(components)) * 100
    print(f"\n🎯 Overall Coverage: {coverage_percent:.1f}%")
```

### Performance Metrics
```python
def collect_performance_metrics():
    """Collect and report performance metrics"""
    
    metrics = {
        'Memory Operations': benchmark_memory_operations(),
        'Model Inference': benchmark_model_inference(),
        'Tool Performance': benchmark_tool_performance(),
        'System Throughput': benchmark_system_throughput()
    }
    
    print("📈 Performance Metrics Report")
    print("=" * 30)
    
    for metric, value in metrics.items():
        print(f"{metric}: {value}")
```

---

## 🔧 Test Configuration

### Environment Variables for Testing
```bash
# Test configuration
export TEST_MODE=true
export TEST_MEMORY_DB=test_threat_memory.db
export TEST_MODEL=threat-intelligence
export VERBOSE_TESTING=true
export PERFORMANCE_TESTING=true
```

### Test-Specific Settings
```python
# test_config.py
TEST_CONFIG = {
    'memory': {
        'use_test_db': True,
        'enable_logging': True,
        'reset_after_test': True
    },
    'model': {
        'use_mock': False,
        'timeout': 10,
        'max_retries': 2
    },
    'performance': {
        'benchmark_enabled': True,
        'collect_metrics': True,
        'report_threshold': 1.0  # seconds
    }
}
```

---

## 📚 Testing Best Practices

### 1. **Isolation**: Each test should be independent
### 2. **Cleanup**: Always clean up test data and resources
### 3. **Mocking**: Use mocks for external dependencies when needed
### 4. **Coverage**: Aim for comprehensive component coverage
### 5. **Performance**: Include performance benchmarks
### 6. **Documentation**: Document test purposes and expected outcomes

---

## 🔗 Related Documentation

- **[Main README](../README.md)**: System overview and setup
- **[Tools Documentation](../src/threatcrew/tools/README.md)**: Component details
- **[Memory Guide](../MEMORY_FINETUNING_GUIDE.md)**: Memory system implementation
- **[Configuration Guide](../src/threatcrew/config/README.md)**: System configuration

---

**🧪 Comprehensive testing ensures ThreatAgent's reliability and performance in production threat intelligence environments.**
