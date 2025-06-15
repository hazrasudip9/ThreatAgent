# ⚙️ Configuration Guide

This directory contains configuration files for ThreatAgent's multi-agent system.

## 📁 Configuration Files

### `agents.yaml`
**Agent Definitions and Roles**

Defines the three specialized AI agents that power ThreatAgent:

```yaml
recon_specialist:
  role: "Recon Specialist"
  goal: "Scan OSINT sources for suspicious indicators with memory-enhanced pattern recognition"
  backstory: |
    You are a cyber threat intelligence analyst specializing in gathering phishing 
    and threat domains from open sources. You have access to a comprehensive memory 
    database of historical threats and can identify patterns across campaigns.
  max_iter: 3
  verbose: true
  memory_enabled: true
  tools:
    - osint_scraper

threat_analyst:
  role: "Threat Analyst"
  goal: "Classify IOCs and map to MITRE TTPs using historical context"
  backstory: |
    You are an experienced cyber analyst who enriches threat data with context 
    and classification. You leverage a memory database of past analyses to 
    improve accuracy and provide confidence scores based on historical patterns.
  max_iter: 3
  verbose: true
  memory_enabled: true
  tools:
    - llm_classifier
    - ttp_mapper

intel_exporter:
  role: "Intel Exporter"
  goal: "Generate comprehensive reports and detection rules with memory insights"
  backstory: |
    You are a threat intelligence report writer who creates actionable intelligence 
    products. You incorporate historical analysis data and memory statistics to 
    provide context-aware reports and detection rules.
  max_iter: 3
  verbose: true
  memory_enabled: true
  tools:
    - report_writer
    - rule_generator
```

### `tasks.yaml`
**Task Definitions and Workflows**

Defines the workflow tasks with memory integration:

```yaml
recon_task:
  description: |
    Scan OSINT sources for suspicious domains and IOCs. Use memory database to:
    - Correlate with historical threat patterns
    - Identify campaign relationships
    - Prioritize based on past threat intelligence
    
    Expected output: List of suspicious domains with memory correlation data
  expected_output: "List of domains with risk assessment and historical context"
  agent: recon_specialist
  tools:
    - osint_scraper

analysis_task:
  description: |
    Classify the discovered IOCs using memory-enhanced analysis:
    - Search for similar historical threats
    - Apply confidence scoring based on past accuracy
    - Map to MITRE ATT&CK TTPs with historical context
    - Store results for continuous learning
    
    Expected output: Classified IOCs with confidence scores and TTP mappings
  expected_output: "IOC classifications with risk levels, categories, and MITRE TTPs"
  agent: threat_analyst
  tools:
    - llm_classifier
    - ttp_mapper
  context: [recon_task]

export_task:
  description: |
    Generate comprehensive threat intelligence products:
    - Create memory-enhanced markdown reports
    - Include historical statistics and trends
    - Generate Sigma detection rules
    - Provide context-aware recommendations
    
    Expected output: Professional threat intelligence report and detection rules
  expected_output: "Markdown report and Sigma rules with memory insights"
  agent: intel_exporter
  tools:
    - report_writer
    - rule_generator
  context: [recon_task, analysis_task]
```

---

## 🎯 Memory-Enhanced Configuration

### Agent Memory Integration

Each agent now has access to the memory system for:

#### Recon Specialist
- **Historical Source Analysis**: Tracks successful OSINT sources
- **Pattern Recognition**: Identifies recurring threat infrastructure
- **Campaign Correlation**: Links new threats to historical campaigns

#### Threat Analyst  
- **Similarity Matching**: Finds similar historical threats
- **Confidence Scoring**: Uses past accuracy for confidence assessment
- **Learning Integration**: Stores classifications for future reference

#### Intel Exporter
- **Context Enhancement**: Incorporates memory statistics in reports
- **Trend Analysis**: Identifies patterns from historical data
- **Recommendation Tuning**: Uses past mitigation success data

---

## 🔧 Customization Options

### Agent Behavior Modification

#### Risk Assessment Thresholds
```yaml
threat_analyst:
  config:
    confidence_threshold: 0.7      # Minimum confidence for high-risk classification
    similarity_threshold: 0.8      # Memory similarity matching threshold
    historical_weight: 0.3         # Weight given to historical context
```

#### Memory Integration Settings
```yaml
global_config:
  memory:
    enabled: true
    similarity_search: true
    auto_store: true              # Automatically store analysis results
    vector_threshold: 0.7         # Semantic similarity threshold
    max_similar_results: 5        # Maximum similar threats to consider
```

#### Tool Configuration
```yaml
tools:
  llm_classifier:
    model: "threat-intelligence"   # Use custom fine-tuned model
    temperature: 0.1              # Low temperature for consistent output
    memory_context: true          # Include memory context in prompts
    
  report_writer:
    include_memory_stats: true    # Add memory statistics to reports
    historical_context: true     # Include similar threat references
    confidence_display: true     # Show confidence scores
```

---

## 🎨 Output Customization

### Report Formatting
```yaml
intel_exporter:
  config:
    report_format:
      include_executive_summary: true
      include_memory_insights: true
      include_confidence_scores: true
      include_historical_correlation: true
      markdown_style: "professional"
      
    rule_generation:
      sigma_format: true
      include_confidence: true
      historical_validation: true
```

### Analysis Detail Levels
```yaml
analysis_levels:
  basic:
    memory_correlation: false
    confidence_scoring: false
    historical_context: false
    
  standard:
    memory_correlation: true
    confidence_scoring: true
    historical_context: false
    
  comprehensive:
    memory_correlation: true
    confidence_scoring: true
    historical_context: true
    trend_analysis: true
```

---

## 🔄 Workflow Customization

### Custom Task Sequences

#### Rapid Analysis Mode
```yaml
rapid_mode:
  tasks:
    - quick_recon
    - basic_classification
    - summary_report
  memory_usage: minimal
  confidence_threshold: 0.6
```

#### Deep Analysis Mode
```yaml
deep_mode:
  tasks:
    - comprehensive_recon
    - memory_enhanced_classification
    - ttp_deep_mapping
    - detailed_report
    - advanced_rules
  memory_usage: full
  confidence_threshold: 0.8
```

#### Campaign Analysis Mode
```yaml
campaign_mode:
  tasks:
    - historical_correlation
    - pattern_analysis
    - attribution_analysis
    - campaign_report
  memory_usage: historical_focus
  time_range: "90_days"
```

---

## 📊 Performance Configuration

### Memory System Tuning
```yaml
memory_config:
  database:
    connection_pool_size: 5
    query_timeout: 30
    vacuum_interval: "weekly"
    
  vector_search:
    model: "sentence-transformers/all-MiniLM-L6-v2"
    cache_size: 1000
    similarity_metric: "cosine"
    
  performance:
    batch_size: 100
    async_processing: true
    cache_results: true
```

### Model Configuration
```yaml
llm_config:
  custom_model:
    name: "threat-intelligence"
    temperature: 0.1
    max_tokens: 512
    timeout: 30
    
  fallback_model:
    name: "llama3"
    temperature: 0.2
    max_tokens: 256
```

---

## 🎯 Environment-Specific Configurations

### Development Environment
```yaml
development:
  agents:
    verbose: true
    max_iter: 5
  memory:
    debug_mode: true
    store_intermediate_results: true
  logging:
    level: "DEBUG"
    include_memory_queries: true
```

### Production Environment
```yaml
production:
  agents:
    verbose: false
    max_iter: 3
  memory:
    debug_mode: false
    optimize_queries: true
  logging:
    level: "INFO"
    performance_monitoring: true
```

### Testing Environment
```yaml
testing:
  agents:
    mock_tools: true
    deterministic_output: true
  memory:
    use_test_database: true
    reset_after_test: true
  validation:
    strict_output_format: true
```

---

## 🔧 Configuration Management

### Loading Custom Configurations
```python
# In crew.py
import yaml
from pathlib import Path

def load_config(config_name="default"):
    config_path = Path(f"src/threatcrew/config/{config_name}.yaml")
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

# Usage
config = load_config("production")
```

### Dynamic Configuration Updates
```python
# Runtime configuration updates
def update_agent_config(agent_name, updates):
    """Update agent configuration at runtime"""
    config = load_config()
    config[agent_name].update(updates)
    save_config(config)
```

### Configuration Validation
```python
# Validate configuration before deployment
def validate_config(config):
    """Validate configuration completeness and correctness"""
    required_sections = ['agents', 'tasks', 'memory']
    for section in required_sections:
        if section not in config:
            raise ValueError(f"Missing required section: {section}")
```

---

## 📚 Configuration Templates

### Minimal Configuration
```yaml
# For basic threat analysis
agents:
  recon_specialist: {role: "Recon", tools: ["osint_scraper"]}
  threat_analyst: {role: "Analyst", tools: ["llm_classifier"]}
  intel_exporter: {role: "Exporter", tools: ["report_writer"]}

memory:
  enabled: false
```

### Full-Featured Configuration
```yaml
# For comprehensive threat intelligence
agents:
  recon_specialist:
    role: "Advanced Recon Specialist"
    memory_enabled: true
    pattern_learning: true
    source_optimization: true
    
  threat_analyst:
    role: "Memory-Enhanced Threat Analyst"
    similarity_search: true
    confidence_modeling: true
    historical_correlation: true
    
  intel_exporter:
    role: "Context-Aware Intelligence Exporter"
    memory_statistics: true
    trend_analysis: true
    comparative_reporting: true

memory:
  enabled: true
  vector_search: true
  continuous_learning: true
  pattern_recognition: true
```

---

## 🔗 Related Documentation

- **[Main README](../README.md)**: System overview
- **[Tools Documentation](../src/threatcrew/tools/README.md)**: Tool details
- **[Memory Guide](../MEMORY_FINETUNING_GUIDE.md)**: Memory implementation
- **[Setup Guide](../setup_memory_finetuning.py)**: Configuration automation

---

**⚙️ Proper configuration unlocks ThreatAgent's full potential for intelligent, memory-enhanced threat analysis.**
