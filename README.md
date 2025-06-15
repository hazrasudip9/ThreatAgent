# 🕵️ ThreatAgent - AI-Powered Threat Intelligence Automation

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Real Data Only](https://img.shields.io/badge/Training%20Data-Real%20Only-green.svg)](./REAL_DATA_CONFIGURATION_GUIDE.md)

**ThreatAgent** is an advanced AI-powered threat intelligence automation system that provides intelligent IOC analysis, threat correlation, and automated report generation using **real threat intelligence data only**. The system leverages custom fine-tuned models and persistent memory to deliver context-aware threat analysis.

## 🌟 Key Features

### 🧠 **Intelligent Memory System**
- **Persistent Knowledge**: SQLite database stores all threat analysis history
- **Vector Similarity Search**: Semantic matching for threat pattern recognition  
- **Historical Context**: Each analysis leverages past intelligence for better accuracy
- **Automatic Learning**: System gets smarter with every threat analyzed

### 🔄 **Automated Threat Feed Ingestion**
- **Multi-Source Collection**: Public feeds (OTX, MISP, ThreatFox, Bambenek, FireHOL)
- **Real-time Processing**: Continuous monitoring and IOC extraction
- **Smart Classification**: AI-powered risk assessment and categorization
- **Quality Assurance**: Validation, deduplication, and confidence scoring

### 🤖 **Custom Fine-tuned Models**
- **Real Data Training**: Uses **only actual threat intelligence** datasets
- **Domain Expertise**: Purpose-built for IOC classification and threat analysis
- **Consistent Output**: Structured JSON responses for reliable automation
- **No Synthetic Data**: Eliminates artificial patterns and bias

### 🔄 **Multi-Agent AI System**
- **Three Specialized Agents**: Recon, Analysis, and Export specialists
- **Memory-Enhanced Analysis**: Historical context improves classification accuracy
- **Collaborative Intelligence**: Agents work together with shared memory access
- **Confidence Scoring**: Data-driven threat assessment with historical validation

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- Ollama (for local AI models)
- Git

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/ThreatAgent.git
cd ThreatAgent

# Set up the environment
cd threatcrew
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure for real data only (default)
python configure_data_sources.py real-only

# Run setup and tests
python test_real_data_mode.py
```

### Basic Usage

```bash
# Analyze a single IOC
python -m threatcrew.main --ioc "suspicious-domain.com"

# Batch analysis
python -m threatcrew.main --file iocs.txt

# Generate threat intelligence report
python -m threatcrew.main --report --campaign "APT Analysis"

# Start automated threat feed ingestion
python -c "
from threatcrew.managers.threat_feed_manager import get_threat_feed_manager
import asyncio
tfm = get_threat_feed_manager()
asyncio.run(tfm.start_feed_monitoring())
"

# Web interface
cd ../ui
python main.py
```

## 📊 Real Data Configuration

ThreatAgent is configured to use **only real threat intelligence datasets** for training:

```python
# Current Configuration (Active)
USE_REAL_DATA_ONLY = True
DISABLE_SYNTHETIC_DATA = True
MIN_CONFIDENCE_THRESHOLD = 0.5
```

### Configuration Management

```bash
# Check current configuration
python configure_data_sources.py show

# Validate real data availability
python configure_data_sources.py validate

# Test system integrity
python test_real_data_mode.py
```

For detailed configuration instructions, see [Real Data Configuration Guide](./REAL_DATA_CONFIGURATION_GUIDE.md).

## 🏗️ System Architecture

```
Input IOCs → Memory Search → Similar Threats → Enhanced Context → 
Custom AI Analysis → Confidence Scoring → Storage → Learning → Output
```

### Core Components

1. **🧠 Memory System**: Persistent SQLite database with vector embeddings
2. **🤖 Custom AI Model**: Fine-tuned `threat-intelligence` model
3. **🕵️ Recon Specialist**: OSINT scanning with historical pattern learning
4. **🔬 Threat Analyst**: Memory-aware IOC classification with confidence scoring  
5. **📋 Intel Exporter**: Context-enhanced reports and detection rules

## 🎯 Use Cases

### Security Operations Centers (SOCs)
- **Automated Triage**: Real-time IOC classification and prioritization
- **Context Enhancement**: Historical threat intelligence for faster analysis
- **Report Generation**: Automated threat intelligence reports
- **Pattern Recognition**: Identify related threats across time

### Threat Intelligence Teams
- **IOC Enrichment**: Enhance indicators with historical context and analysis
- **Campaign Tracking**: Connect threats across different time periods
- **Confidence Assessment**: Data-driven threat assessment scoring
- **Knowledge Retention**: Persistent organizational threat intelligence

### Enterprise Security Teams
- **Custom Model Deployment**: Fine-tuned AI for organization-specific threats
- **Real Data Training**: Models trained exclusively on verified threat intelligence
- **Automated Learning**: System adapts to environment without manual tuning
- **Compliance Ready**: Auditable data sources and analysis history

## 📁 Project Structure

```
ThreatAgent/
├── threatcrew/                 # Main threat intelligence system
│   ├── src/threatcrew/        # Core modules
│   │   ├── agents/            # AI agents (Recon, Analysis, Export)
│   │   ├── tools/             # Analysis tools and fine-tuning
│   │   ├── managers/          # System managers
│   │   ├── config/            # Configuration files
│   │   └── knowledge/         # Memory database and training data
│   ├── tests/                 # Test suites and demos
│   ├── configure_data_sources.py  # Data configuration tool
│   └── test_real_data_mode.py     # Real data validation tests
├── ui/                        # Web interface
├── knowledge/                 # Training datasets
└── docs/                      # Documentation
```

## 🔧 Configuration Files

- **[Real Data Configuration Guide](./REAL_DATA_CONFIGURATION_GUIDE.md)**: Complete guide for real data setup
- **[Level 1 Ingestion Guide](./LEVEL_1_INGESTION_GUIDE.md)**: Comprehensive guide for public threat intel feeds
- **[User Guide](./USER_GUIDE.md)**: Comprehensive usage instructions
- **[System Implementation Summary](./IMPLEMENTATION_SUMMARY_REAL_DATA.md)**: Technical implementation details
- **[Quick Reference](./QUICK_REFERENCE.md)**: Common commands and workflows

## 🧪 Testing

```bash
# Test real data configuration
python test_real_data_mode.py

# Run full test suite
python test_threatcrew_all.py

# Validate system components
cd threatcrew/tests
python verify_system.py
```

## 📊 Data Sources

### Real Threat Intelligence Only
- ✅ Memory database IOCs (confidence ≥ 0.5)
- ✅ Historical analysis data
- ✅ Actual threat reports
- ✅ Verified TTP mappings
- ❌ Synthetic/generated examples (disabled)
- ❌ Demo/test data (excluded)

### Data Quality Assurance
- Source attribution required for all training data
- Confidence thresholding for data inclusion
- Automatic filtering of synthetic patterns
- Traceable intelligence lineage

## 🛡️ Security Features

- **Real Data Only**: No synthetic contamination in training
- **Source Attribution**: Complete data lineage tracking
- **Confidence Scoring**: Quantified assessment reliability
- **Memory Isolation**: Secure threat intelligence storage
- **Audit Trail**: Complete analysis history logging

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [CrewAI](https://github.com/joaomdmoura/crewAI) for multi-agent orchestration
- Powered by [Ollama](https://ollama.ai/) for local AI model deployment
- Uses real threat intelligence datasets for authentic learning
- Inspired by the need for trustworthy, transparent threat intelligence automation

## 📞 Support

- **Documentation**: Check the `/docs` directory for detailed guides
- **Issues**: Open an issue on GitHub for bug reports or feature requests
- **Configuration**: Use `python configure_data_sources.py --help` for setup assistance

---

**ThreatAgent**: Where artificial intelligence meets real threat intelligence. 🛡️🤖
