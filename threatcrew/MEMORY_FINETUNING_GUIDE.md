# 🧠 ThreatAgent Memory & Fine-tuning Implementation Guide

## Overview

This guide shows you how to implement persistent memory storage and fine-tuning capabilities for the ThreatAgent system. The system will learn from each analysis and improve over time.

## 🏗️ Architecture

```
ThreatAgent Memory & Fine-tuning System
├── Memory Database (SQLite)
│   ├── IOCs with embeddings
│   ├── TTP mappings
│   ├── Analysis history
│   └── Knowledge patterns
├── Vector Search (sentence-transformers)
│   ├── Semantic similarity
│   └── Context retrieval
├── Fine-tuning Pipeline
│   ├── Training data generation
│   ├── Ollama Modelfile creation
│   └── Context enhancement
└── Enhanced Tools
    ├── Memory-aware classification
    ├── Historical context reports
    └── Pattern recognition
```

## 🚀 Implementation Steps

### Step 1: Install Dependencies

```bash
cd /Users/noobita/Desktop/Github/ThreatAgent/threatcrew

# Install vector embeddings (optional but recommended)
pip3 install sentence-transformers

# Verify installation
python3 -c "import sentence_transformers; print('✅ Ready for semantic search')"
```

### Step 2: Memory System Usage

The memory system is already integrated. Here's how it works:

```python
# Memory system automatically stores data during analysis
from threatcrew.tools.memory_system import get_memory

memory = get_memory()

# Store IOCs manually
ioc_id = memory.store_ioc(
    ioc="malicious-site.com",
    ioc_type="domain",
    risk_level="high", 
    category="phishing",
    confidence=0.9,
    source="manual_analysis"
)

# Search for similar threats
similar = memory.search_similar_iocs("banking phishing", limit=5)
for threat in similar:
    print(f"{threat['ioc']} - {threat['risk_level']} ({threat['similarity']:.3f})")

# Get database statistics
stats = memory.get_statistics()
print(f"Total IOCs: {stats['total_iocs']}")
```

### Step 3: Generate Training Data

```python
from threatcrew.tools.finetuning_system import get_finetuner

finetuner = get_finetuner()

# Generate training dataset from memory
dataset_path = finetuner.generate_training_dataset()
print(f"Training data saved to: {dataset_path}")

# Create context-enhanced prompts
enhanced_prompt = finetuner.create_context_prompt(
    "Analyze this suspicious domain: fake-bank.tk"
)
```

### Step 4: Create Custom Ollama Model

```bash
# Generate Ollama Modelfile
python3 -c "
from threatcrew.tools.finetuning_system import get_finetuner
finetuner = get_finetuner()
config = finetuner.export_training_config()
with open('knowledge/ThreatAgent.Modelfile', 'w') as f:
    f.write(config['ollama_modelfile'])
print('✅ Modelfile created')
"

# Create custom model
ollama create threat-intelligence -f knowledge/ThreatAgent.Modelfile

# Test the custom model
ollama run threat-intelligence
```

### Step 5: Update ThreatAgent to Use Custom Model

```python
# Edit src/threatcrew/crew.py
def get_llm():
    return OllamaLLM(
        model='threat-intelligence',  # Use custom model
        base_url=os.getenv('OLLAMA_API_BASE', 'http://localhost:11434'),
        temperature=0.1,
        num_predict=512,
        stop=["\n\n", "Human:", "Assistant:"],
    )
```

## 🧪 Testing Memory Features

### Test Memory Storage

```python
# Create test script: test_memory_features.py
import sys, os
sys.path.insert(0, 'src')

from threatcrew.tools.memory_system import get_memory

memory = get_memory()

# Store test data
test_iocs = [
    ("phishing-bank.tk", "domain", "high", "phishing", 0.9),
    ("malware-c2.ru", "domain", "high", "c2", 0.95),
    ("192.168.1.100", "ip_address", "low", "internal", 0.1)
]

for ioc, ioc_type, risk, category, confidence in test_iocs:
    ioc_id = memory.store_ioc(ioc, ioc_type, risk, category, confidence)
    print(f"Stored: {ioc} (ID: {ioc_id})")

# Test search
results = memory.search_similar_iocs("banking", limit=3)
print(f"Found {len(results)} similar threats")

# Show statistics
stats = memory.get_statistics()
print(f"Database: {stats['total_iocs']} IOCs, {stats['total_analyses']} analyses")
```

### Test Enhanced Classification

```python
# Enhanced classification automatically uses memory
from threatcrew.tools.llm_classifier import run as classify_iocs

# These will benefit from memory context
test_iocs = [
    "another-bank-phish.tk",  # Should match known patterns
    "suspicious-paypal.ml",   # Should recognize PayPal phishing
    "192.168.1.50"           # Should classify as internal
]

results = classify_iocs(test_iocs)
for result in results:
    print(f"{result['ioc']}: {result['risk']} ({result.get('confidence', 0):.2f})")
    if 'similar_threats' in result:
        print(f"  Similar threats in memory: {result['similar_threats']}")
```

## 📊 Monitoring & Analytics

### View Memory Database

```bash
# Connect to SQLite database
sqlite3 src/knowledge/threat_memory.db

# Query IOCs
.mode column
.headers on
SELECT ioc, risk_level, category, confidence, times_seen FROM iocs LIMIT 10;

# Query analysis history
SELECT analysis_type, COUNT(*) as count FROM analysis_history GROUP BY analysis_type;

# Exit
.quit
```

### Memory Statistics Dashboard

```python
def show_memory_dashboard():
    memory = get_memory()
    stats = memory.get_statistics()
    
    print("🧠 ThreatAgent Memory Dashboard")
    print("=" * 40)
    print(f"📊 Total IOCs: {stats['total_iocs']}")
    print(f"📊 Total Analyses: {stats['total_analyses']}")
    
    if stats['risk_distribution']:
        print("\n🎯 Risk Distribution:")
        for risk, count in stats['risk_distribution'].items():
            print(f"   {risk.upper()}: {count}")
    
    if stats['category_distribution']:
        print("\n📂 Category Distribution:")
        for category, count in stats['category_distribution'].items():
            print(f"   {category}: {count}")
    
    print("\n📈 Recent Activity:")
    recent = memory.get_analysis_history(limit=5)
    for analysis in recent:
        print(f"   {analysis['analysis_type']}: {analysis['confidence']:.2f}")

# Run dashboard
show_memory_dashboard()
```

## 🎯 Advanced Features

### Continuous Learning

The system automatically learns from each analysis:

1. **IOC Storage**: Every classified IOC is stored with metadata
2. **Pattern Recognition**: Similar threats are identified using embeddings
3. **Context Enhancement**: Historical data improves new analyses
4. **Training Data**: Memory generates fine-tuning datasets

### Custom Training Datasets

```python
# Generate domain-specific training data
def generate_custom_training():
    finetuner = get_finetuner()
    
    # Add custom examples
    custom_examples = [
        {
            "instruction": "Classify cryptocurrency-related threat",
            "input": "crypto-exchange-security.tk",
            "output": '{"risk": "high", "category": "crypto_phishing", "confidence": 0.85}'
        }
    ]
    
    # Combine with memory-based examples
    dataset = finetuner.generate_training_dataset()
    
    # Append custom examples
    with open(dataset, 'a') as f:
        for example in custom_examples:
            f.write(json.dumps(example) + '\n')
    
    print("✅ Custom training data added")
```

### Integration with External Feeds

```python
# Bulk import from threat feeds
def import_threat_feed(feed_data):
    memory = get_memory()
    
    for item in feed_data:
        memory.store_ioc(
            ioc=item['indicator'],
            ioc_type=item['type'],
            risk_level=item['severity'],
            category=item['category'],
            confidence=item.get('confidence', 0.5),
            source="threat_feed",
            metadata=item.get('metadata', {})
        )
    
    print(f"✅ Imported {len(feed_data)} indicators")

# Example usage
sample_feed = [
    {
        "indicator": "evil-domain.com",
        "type": "domain",
        "severity": "high", 
        "category": "malware",
        "confidence": 0.9
    }
]

import_threat_feed(sample_feed)
```

## 🔧 Configuration Options

### Memory System Settings

```python
# Custom memory configuration
class CustomThreatMemory(ThreatMemoryDB):
    def __init__(self):
        super().__init__(db_path="custom_path/threat_memory.db")
        
        # Custom embedding model
        if EMBEDDINGS_AVAILABLE:
            self.embedding_model = SentenceTransformer('all-mpnet-base-v2')  # Better model
        
        # Custom similarity threshold
        self.similarity_threshold = 0.8
```

### Fine-tuning Parameters

```python
# Customize training configuration
config = {
    "model_name": "threat-intel-specialized",
    "training_parameters": {
        "learning_rate": 1e-5,
        "batch_size": 8,
        "epochs": 5,
        "max_seq_length": 4096,
        "warmup_steps": 200
    }
}
```

## 📈 Performance Optimization

### Database Indexing

```sql
-- Add indexes to SQLite database for better performance
CREATE INDEX IF NOT EXISTS idx_iocs_category ON iocs(category);
CREATE INDEX IF NOT EXISTS idx_iocs_risk ON iocs(risk_level);
CREATE INDEX IF NOT EXISTS idx_iocs_confidence ON iocs(confidence);
CREATE INDEX IF NOT EXISTS idx_analysis_type ON analysis_history(analysis_type);
```

### Embedding Caching

```python
# Cache embeddings for frequently accessed IOCs
import pickle

class CachedEmbeddingMemory(ThreatMemoryDB):
    def __init__(self):
        super().__init__()
        self.embedding_cache = {}
    
    def _get_embedding(self, text):
        if text in self.embedding_cache:
            return self.embedding_cache[text]
        
        embedding = super()._get_embedding(text)
        self.embedding_cache[text] = embedding
        return embedding
```

## 🚀 Production Deployment

### Backup Strategy

```bash
# Backup memory database
cp src/knowledge/threat_memory.db backups/threat_memory_$(date +%Y%m%d).db

# Automated backup script
cat > backup_memory.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="backups"
mkdir -p $BACKUP_DIR
cp src/knowledge/threat_memory.db $BACKUP_DIR/threat_memory_$(date +%Y%m%d_%H%M%S).db
echo "✅ Memory database backed up"
EOF

chmod +x backup_memory.sh
```

### Monitoring Script

```python
# monitor_memory.py - Production monitoring
import time
from threatcrew.tools.memory_system import get_memory

def monitor_memory_health():
    while True:
        try:
            memory = get_memory()
            stats = memory.get_statistics()
            
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] "
                  f"IOCs: {stats['total_iocs']}, "
                  f"Analyses: {stats['total_analyses']}")
            
            # Check for anomalies
            if stats['total_iocs'] > 10000:
                print("⚠️  Large IOC database - consider archiving")
            
        except Exception as e:
            print(f"❌ Memory health check failed: {e}")
        
        time.sleep(3600)  # Check every hour

if __name__ == "__main__":
    monitor_memory_health()
```

## 🎉 Next Steps

1. **Run ThreatAgent** with memory enabled (it's already integrated)
2. **Generate training data** from accumulated analyses
3. **Create custom model** using Ollama Modelfile
4. **Monitor performance** improvements over time
5. **Expand training data** with domain-specific examples

The memory system will automatically improve ThreatAgent's analysis accuracy as it learns from each threat intelligence workflow!

---

**Created**: June 14, 2025  
**Status**: Production Ready  
**Integration**: Automatic with existing ThreatAgent system
