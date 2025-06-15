# 🛠️ ThreatAgent Tools Documentation

This directory contains the core tools that power ThreatAgent's intelligent threat analysis capabilities. Each tool has been enhanced with memory integration and custom AI model support.

## 🧠 Core Memory System

### `memory_system.py`
**Persistent Threat Intelligence Database**

The foundation of ThreatAgent's learning capabilities, providing:

- **SQLite Database**: Persistent storage for all threat analysis
- **Vector Embeddings**: Semantic similarity search using sentence-transformers
- **Historical Context**: Access to past analyses for enhanced decision-making
- **Pattern Recognition**: Automatic detection of similar threat indicators

#### Key Classes:
- `ThreatMemoryDB`: Main database interface
- `get_memory()`: Factory function for memory instance

#### Usage:
```python
from threatcrew.tools.memory_system import get_memory

memory = get_memory()
ioc_id = memory.store_ioc("malicious-site.tk", "domain", "high", "phishing", 0.9)
similar = memory.search_similar_iocs("banking-phish.tk", threshold=0.7)
```

---

## 🤖 Fine-tuning System

### `finetuning_system.py`
**Custom Model Training Pipeline**

Generates training datasets and creates custom fine-tuned models:

- **Dataset Generation**: Creates training examples from memory data
- **Ollama Integration**: Generates Modelfiles for custom models
- **Context Enhancement**: Uses historical data to improve prompts
- **Export Capabilities**: Supports multiple ML framework formats

#### Key Classes:
- `ThreatFineTuner`: Main fine-tuning orchestrator

#### Usage:
```python
from threatcrew.tools.finetuning_system import ThreatFineTuner

finetuner = ThreatFineTuner(memory)
dataset = finetuner.generate_training_dataset(num_examples=100)
modelfile = finetuner.create_ollama_modelfile()
```

---

## 🔍 Analysis Tools

### `llm_classifier.py`
**Memory-Enhanced IOC Classification**

Classifies indicators of compromise with historical context:

- **Memory Integration**: Uses similar past threats for context
- **Confidence Scoring**: Data-driven confidence based on historical accuracy
- **Custom Model**: Leverages fine-tuned threat-intelligence model
- **Automatic Storage**: Results automatically stored for learning

#### Enhanced Features:
- Historical pattern matching
- Confidence scoring based on similar threats
- Automatic learning from classifications

### `ttp_mapper.py`
**MITRE ATT&CK Mapping with Context**

Maps threats to MITRE ATT&CK techniques:

- **Memory-Aware**: Uses historical TTP mappings for context
- **Pattern Recognition**: Identifies recurring technique patterns
- **Confidence Assessment**: Scoring based on historical accuracy
- **Knowledge Building**: Builds organizational TTP knowledge base

#### Enhanced Features:
- Historical TTP pattern analysis
- Confidence scoring for technique mappings
- Automatic technique correlation

---

## 📊 Intelligence Generation

### `report_writer.py` 
**Memory-Enhanced Report Generation**

Creates comprehensive threat intelligence reports:

- **Historical Context**: Incorporates memory statistics and trends
- **Pattern Analysis**: References similar historical threats
- **Memory Insights**: Includes database analytics in reports
- **Professional Format**: Markdown reports with contextual information

#### Enhanced Features:
- Memory statistics integration
- Historical threat correlation
- Context-aware recommendations
- Trend analysis from memory

### `rule_generator.py`
**Context-Aware Detection Rules**

Generates Sigma detection rules with historical context:

- **Pattern-Based Rules**: Uses memory patterns for rule creation
- **Historical Validation**: Rules informed by past threat patterns
- **Context Integration**: Incorporates organizational threat history
- **Quality Assurance**: Rules validated against historical data

#### Enhanced Features:
- Memory-informed rule generation
- Historical pattern validation
- Context-aware rule parameters

---

## 🌐 Data Collection

### `osint_scraper.py`
**Pattern-Learning OSINT Collection**

Collects threat indicators with learning capabilities:

- **Pattern Learning**: Remembers successful OSINT sources
- **Historical Correlation**: Cross-references with memory database
- **Adaptive Collection**: Improves source selection over time
- **Context Awareness**: Uses past collection success for optimization

#### Enhanced Features:
- Source pattern learning
- Historical correlation checks
- Adaptive collection strategies

---

## 🔧 Configuration and Usage

### Environment Variables
```bash
# Memory System
MEMORY_ENABLED=true
MEMORY_DB_PATH=src/knowledge/threat_memory.db
VECTOR_SIMILARITY_THRESHOLD=0.7

# Custom Model
MODEL=threat-intelligence
OLLAMA_API_BASE=http://localhost:11434

# Fine-tuning
TRAINING_DATA_PATH=knowledge/threat_intelligence_training.jsonl
AUTO_RETRAIN=false
CONFIDENCE_THRESHOLD=0.8
```

### Memory Database Schema

#### Tables:
- **iocs**: Core indicator storage
  - `id`, `ioc`, `ioc_type`, `risk_level`, `category`
  - `confidence`, `source`, `metadata`
  - `first_seen`, `last_seen`, `times_seen`

- **ttp_mappings**: MITRE ATT&CK mappings
  - `id`, `ioc_id`, `ttp_id`, `ttp_name`
  - `confidence`, `context`, `created_at`

- **analysis_history**: Session tracking
  - `id`, `session_id`, `analysis_type`
  - `input_data`, `output_data`, `confidence`
  - `processing_time`, `created_at`

- **knowledge_patterns**: Learned patterns
  - `id`, `pattern_type`, `pattern_data`
  - `confidence`, `usage_count`, `last_used`

### Tool Integration Flow

```
Input IOCs → Memory Search → Historical Context → 
Custom AI Analysis → Confidence Scoring → Storage → Learning
```

## 🧪 Testing Tools

### Memory System Testing
```bash
# Test memory database functionality
python3 simple_memory_test.py

# Test memory-enhanced classification
PYTHONPATH=src python3 -c "
from threatcrew.tools.llm_classifier import run
result = run(['test-phishing.tk'])
print(result)
"
```

### Custom Model Testing
```bash
# Test fine-tuned model directly
ollama run threat-intelligence "Analyze: suspicious-bank.tk"

# Test fine-tuning pipeline
python3 -c "
from threatcrew.tools.finetuning_system import ThreatFineTuner
from threatcrew.tools.memory_system import get_memory
finetuner = ThreatFineTuner(get_memory())
dataset = finetuner.generate_training_dataset(5)
print(f'Generated {len(dataset)} examples')
"
```

## 🎯 Performance Considerations

### Memory System
- **Database Size**: Monitor SQLite file size growth
- **Vector Search**: Sentence-transformers model caching
- **Query Performance**: Index optimization for large datasets

### Custom Model
- **Model Size**: Fine-tuned models are larger than base models
- **Inference Speed**: Custom models may be slower than base models
- **Memory Usage**: Monitor Ollama memory consumption

### Optimization Tips
- Regular database maintenance (`VACUUM`)
- Vector cache management
- Batch processing for large datasets
- Model quantization for faster inference

## 🔮 Advanced Features

### Planned Enhancements
- **Graph Database**: Neo4j integration for complex threat relationships
- **Real-time Learning**: Streaming updates to memory system
- **Federated Memory**: Distributed memory across multiple instances
- **Advanced Analytics**: Time-series analysis and prediction

### Research Areas
- **Reinforcement Learning**: RLHF for improved classifications
- **Adversarial Detection**: AI-powered campaign attribution
- **Threat Prediction**: Proactive threat landscape forecasting

---

## 📚 Additional Resources

- **[Memory & Fine-tuning Guide](../MEMORY_FINETUNING_GUIDE.md)**: Detailed implementation guide
- **[Setup Documentation](../setup_memory_finetuning.py)**: Automated setup process
- **[Completion Report](../COMPLETION_REPORT.md)**: Feature implementation status
- **[Demo Scripts](../demo_complete_system.py)**: Interactive demonstrations

---

**Built with ❤️ for intelligent threat analysis**

*Each tool is designed to learn and improve, making ThreatAgent smarter with every analysis.*
