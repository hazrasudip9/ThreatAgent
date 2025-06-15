# Real Data Configuration Guide

## Overview

The ThreatAgent system has been configured to support **real threat intelligence datasets only** mode, eliminating the use of synthetic or generated training data. This ensures that all threat intelligence training is based on actual, verified threat data.

## Key Changes Made

### 1. Configuration System
- **New Config File**: `src/threatcrew/config/data_source_config.py`
- **Real Data Only Mode**: `USE_REAL_DATA_ONLY = True`
- **Synthetic Data Disabled**: `DISABLE_SYNTHETIC_DATA = True`
- **Source Filtering**: Excludes synthetic, demo, test, and generated data sources

### 2. Enhanced Fine-tuning System
- **Modified**: `src/threatcrew/tools/finetuning_system.py`
- **Real Data Filtering**: Only uses IOCs and analysis data from verified real sources
- **Source Attribution**: All training examples include source metadata
- **Confidence Thresholding**: Minimum confidence level for training data inclusion

### 3. Data Source Validation
- **Excluded Sources**: `["synthetic", "generated", "example", "demo", "test"]`
- **Required Sources**: `["memory_database", "historical_analysis", "real_iocs", "actual_reports"]`
- **Confidence Threshold**: Minimum 0.5 confidence for training data inclusion

## Configuration Options

### Current Settings (Real Data Only Mode)
```python
DATA_SOURCE_CONFIG = {
    "USE_REAL_DATA_ONLY": True,           # ✅ ENABLED
    "DISABLE_SYNTHETIC_DATA": True,       # ✅ ENABLED
    "MIN_CONFIDENCE_THRESHOLD": 0.5,      # Real data confidence minimum
    "MAX_EXAMPLES_PER_CATEGORY": 1000,    # Limit per category
    "EXCLUDED_DATA_SOURCES": [
        "synthetic", "generated", "example", "demo", "test"
    ]
}
```

## Using the Configuration Tool

### Quick Configuration Commands

```bash
# Check current configuration
python threatcrew/configure_data_sources.py show

# Enable real data only mode (RECOMMENDED)
python threatcrew/configure_data_sources.py real-only

# Enable mixed data mode (if needed for testing)
python threatcrew/configure_data_sources.py mixed

# Validate available real data
python threatcrew/configure_data_sources.py validate
```

### Example Output (Real Data Only Mode)
```
🔧 Dataset Generation Configuration:
   ✅ Use Real Data Only: True
   ❌ Disable Synthetic Data: True
   📊 Min Confidence Threshold: 0.5
   🚫 Excluded Sources: ['synthetic', 'generated', 'example', 'demo', 'test']

📊 Generated 45 IOC classification examples (Real data only: True)
📊 Generated 23 TTP mapping examples (Real data only: True)
📊 Generated 12 report generation examples (Real data only: True)
📊 Generated 31 analysis examples (Real data only: True)

💾 Saved to: threat_intelligence_dataset_real_data_20250615_180000.jsonl
🔍 Data Source: Real threat intelligence only
```

## Data Quality Improvements

### 1. Real IOC Classification
- Sources actual IOCs from memory database
- Filters by confidence threshold (≥0.5)
- Excludes demo/synthetic entries
- Includes source attribution in training data

### 2. Real TTP Mapping
- Uses actual TTP mappings from analysis history
- Excludes framework-only mappings when in real-data mode
- Preserves actual threat intelligence relationships

### 3. Real Report Generation
- Uses actual generated reports from system history
- Filters out template/example reports
- Maintains real threat context and formatting

### 4. Real Analysis Examples
- Sources from actual threat analysis history
- Includes domain, IP, and general threat analysis
- Excludes synthetic analysis patterns

## Verification Steps

### 1. Check Configuration Status
```bash
python threatcrew/configure_data_sources.py show
```

### 2. Validate Real Data Availability
```bash
python threatcrew/configure_data_sources.py validate
```

### 3. Generate New Training Dataset
```bash
cd threatcrew
python -c "
from src.threatcrew.tools.finetuning_system import ThreatFineTuner
finetuner = ThreatFineTuner()
dataset_path = finetuner.generate_training_dataset()
print(f'Real data dataset generated: {dataset_path}')
"
```

### 4. Verify Dataset Contents
Check that generated datasets have filenames containing "real_data":
```bash
ls -la src/knowledge/training_data/threat_intelligence_dataset_real_data_*.jsonl
```

## Benefits of Real Data Only Mode

### ✅ Enhanced Accuracy
- Training based on actual threat intelligence
- No synthetic bias in model learning
- Real-world threat patterns and relationships

### ✅ Improved Relevance
- Current and actual threat landscape representation
- Organization-specific threat context
- Historical accuracy preservation

### ✅ Higher Confidence
- Verifiable data sources
- Traceable threat intelligence lineage
- Authentic threat analysis patterns

### ✅ Compliance Ready
- Auditable data sources
- Real threat intelligence attribution
- No synthetic data contamination

## Migration from Synthetic Data

### Existing Synthetic Datasets
The system now automatically excludes synthetic datasets when `USE_REAL_DATA_ONLY = True`. Existing synthetic datasets remain in the training_data directory but are not used for new training.

### Historical Data Preservation
All real threat intelligence and analysis data is preserved and enhanced with proper source attribution for training purposes.

## Troubleshooting

### Low Training Data Volume
If you see warnings about insufficient real data:

1. **Import More Real IOCs**: Add actual threat indicators to the memory database
2. **Perform More Analyses**: Run threat analysis on real indicators to build history
3. **Generate Real Reports**: Create actual threat intelligence reports
4. **Temporarily Use Mixed Mode**: If absolutely necessary for testing

### Configuration Issues
If configuration changes don't take effect:

1. **Restart the System**: Ensure configuration is reloaded
2. **Clear Cache**: Remove any cached training datasets
3. **Verify Paths**: Check that configuration file paths are correct

## Next Steps

1. **Enable Real Data Mode**: Run `python threatcrew/configure_data_sources.py real-only`
2. **Validate Data**: Run `python threatcrew/configure_data_sources.py validate`
3. **Generate New Dataset**: Create a new training dataset using only real data
4. **Monitor Quality**: Review generated datasets for real data composition
5. **Fine-tune Model**: Retrain the threat intelligence model with real data only

## Security Benefits

- **No Synthetic Contamination**: Eliminates artificial patterns that might not represent real threats
- **Authentic Learning**: Model learns from actual threat landscape
- **Traceable Intelligence**: All training data can be traced to real sources
- **Compliance Ready**: Meets requirements for using only verified threat intelligence
