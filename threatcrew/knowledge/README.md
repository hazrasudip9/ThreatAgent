# 📚 Knowledge Directory

This directory contains the core knowledge assets for ThreatAgent's memory and fine-tuning capabilities.

## 📁 Directory Contents

### 🤖 Custom Model Files

#### `ThreatAgent.Modelfile`
**Ollama Custom Model Configuration**

Defines the custom fine-tuned model for threat intelligence analysis:

```dockerfile
FROM llama3

SYSTEM """You are an expert cybersecurity threat intelligence analyst specializing in:

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
- Use consistent JSON formatting for structured output
- Include historical context when available
- Reference similar past threats for validation
"""

PARAMETER temperature 0.1
PARAMETER top_p 0.9
PARAMETER num_predict 512
```

**Features:**
- Specialized system prompts for cybersecurity analysis
- Optimized parameters for consistent threat intelligence output
- JSON-structured responses for automation
- Historical context awareness

#### `setup_custom_model.sh`
**Model Deployment Script**

Automated script to create and deploy the custom model:

```bash
#!/bin/bash
echo "🤖 Setting up ThreatAgent Custom Model"

# Check Ollama availability
if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "❌ Ollama is not running. Please start it first:"
    echo "   ollama serve"
    exit 1
fi

# Create custom model
echo "📦 Creating threat-intelligence model..."
ollama create threat-intelligence -f knowledge/ThreatAgent.Modelfile

if [ $? -eq 0 ]; then
    echo "✅ Custom model created successfully!"
    echo "🎯 Test the model: ollama run threat-intelligence"
else
    echo "❌ Failed to create custom model"
    exit 1
fi
```

**Usage:**
```bash
# Make executable and run
chmod +x knowledge/setup_custom_model.sh
./knowledge/setup_custom_model.sh
```

---

### 📚 Training Data

#### `threat_intelligence_training.jsonl`
**Fine-tuning Training Dataset**

JSONL format training data generated from memory database:

```jsonl
{"instruction": "Classify this domain for cybersecurity threats", "input": "secure-bank-login.tk", "output": "{\n  \"ioc\": \"secure-bank-login.tk\",\n  \"type\": \"domain\",\n  \"risk_level\": \"high\",\n  \"category\": \"phishing\",\n  \"confidence\": 0.9,\n  \"reasoning\": \"Banking-related keywords with suspicious .tk TLD\"\n}"}
```

**Features:**
- Automatically generated from memory database
- Instruction-following format for fine-tuning
- Real threat intelligence examples
- Structured JSON outputs
- Cybersecurity domain expertise

**Dataset Statistics:**
- Example count: Dynamically generated from memory
- Categories: IOC classification, TTP mapping, report generation
- Format: JSONL (JSON Lines) for easy processing
- Updates: Automatically refreshed from memory database

---

### 🗂️ Configuration Files

#### `user_preference.txt`
**User Preferences and Settings**

Stores user-specific configuration and preferences:
- Analysis preferences
- Output format settings
- Custom thresholds
- Model selection preferences

---

## 🔄 File Generation Workflow

### Automatic Generation Process

1. **Memory Analysis**: System analyzes stored threat data
2. **Pattern Extraction**: Identifies successful analysis patterns
3. **Dataset Creation**: Generates training examples from memory
4. **Model Configuration**: Creates optimized Modelfile
5. **Deployment Scripts**: Generates setup automation

### Manual Regeneration

```bash
# Regenerate all knowledge files
python3 setup_memory_finetuning.py

# This will:
# ✅ Update training dataset from latest memory data
# ✅ Refresh Modelfile with latest parameters
# ✅ Generate new setup scripts
# ✅ Validate all configurations
```

---

## 🎯 Usage Guidelines

### Custom Model Usage

```bash
# Test the custom model
ollama run threat-intelligence "Analyze domain: suspicious-site.tk"

# Use in ThreatAgent (automatically configured)
./run_threatcrew.sh
```

### Training Data Usage

```python
# Load training data for analysis
import json

with open('knowledge/threat_intelligence_training.jsonl', 'r') as f:
    training_data = [json.loads(line) for line in f]

print(f"Loaded {len(training_data)} training examples")
```

### Advanced Fine-tuning

```python
# Export to other formats for advanced training
from threatcrew.tools.finetuning_system import ThreatFineTuner
from threatcrew.tools.memory_system import get_memory

finetuner = ThreatFineTuner(get_memory())

# Export for Unsloth/LoRA training
finetuner.export_for_unsloth('knowledge/unsloth_dataset.json')

# Export for HuggingFace
finetuner.export_for_huggingface('knowledge/hf_dataset.json')
```

---

## 📊 Quality Metrics

### Training Data Quality
- **Coverage**: Examples span all major threat categories
- **Balance**: Proportional representation of risk levels
- **Accuracy**: Generated from validated memory data
- **Freshness**: Updated with each memory database change

### Model Performance
- **Consistency**: Structured JSON output format
- **Accuracy**: Improved threat classification over base model
- **Speed**: Optimized parameters for fast inference
- **Specialization**: Domain-specific cybersecurity knowledge

---

## 🔧 Maintenance

### Regular Updates

```bash
# Update training data (monthly recommended)
python3 -c "
from threatcrew.tools.finetuning_system import ThreatFineTuner
from threatcrew.tools.memory_system import get_memory
finetuner = ThreatFineTuner(get_memory())
dataset = finetuner.generate_training_dataset(num_examples=100)
finetuner.save_training_dataset(dataset, 'knowledge/threat_intelligence_training.jsonl')
print('Training data updated')
"

# Recreate custom model with updated data
./knowledge/setup_custom_model.sh
```

### Performance Monitoring

```bash
# Check model performance
ollama run threat-intelligence "Classify: test-phishing-site.tk" --format json

# Monitor training data size
wc -l knowledge/threat_intelligence_training.jsonl

# Check model disk usage
ollama list | grep threat-intelligence
```

---

## 🚀 Advanced Configuration

### Custom System Prompts
Edit `ThreatAgent.Modelfile` to customize the model's behavior:

```dockerfile
SYSTEM """Your custom system prompt here...
- Custom analysis requirements
- Organization-specific threat focus
- Specialized output formats
"""
```

### Parameter Tuning
Adjust model parameters in the Modelfile:

```dockerfile
PARAMETER temperature 0.1      # Lower = more focused
PARAMETER top_p 0.9           # Nucleus sampling
PARAMETER num_predict 512     # Max response length
PARAMETER stop "Human:"       # Stop sequences
```

### Advanced Training
For specialized deployments:

1. **Domain-Specific Training**: Focus on specific threat types
2. **Organization Training**: Train on internal threat data
3. **Language Adaptation**: Multi-language threat analysis
4. **Real-time Learning**: Continuous model updates

---

## 📚 Related Documentation

- **[Memory System Guide](../src/threatcrew/tools/README.md)**: Tool documentation
- **[Setup Guide](../setup_memory_finetuning.py)**: Complete system setup
- **[Fine-tuning Guide](../MEMORY_FINETUNING_GUIDE.md)**: Detailed implementation
- **[Main README](../README.md)**: System overview

---

**🎯 The knowledge directory is the brain of ThreatAgent - containing all the specialized intelligence that makes the system a cybersecurity expert.**
