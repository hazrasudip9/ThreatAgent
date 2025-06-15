# 📖 ThreatAgent Examples

This directory contains practical examples and demonstrations of ThreatAgent's threat intelligence capabilities.

## 🚀 Quick Start Examples

### 1. Quick Ingestion Demo (`quick_ingestion_demo.py`)

A comprehensive demonstration of Level 1 threat intelligence ingestion:

```bash
cd examples
python quick_ingestion_demo.py
```

**What it demonstrates:**
- ✅ Setting up popular threat intelligence feeds (ThreatFox, URLhaus, Bambenek, FireHOL)
- ✅ Automated IOC collection and classification  
- ✅ Real-time feed monitoring
- ✅ Memory database integration
- ✅ Production deployment patterns

**Example output:**
```
🕵️ ThreatAgent - Level 1 Threat Feed Ingestion Demo
============================================================
🔧 Adding popular threat intelligence feeds...
✅ Added 4 high-quality threat intelligence feeds

🔍 THREAT FEED STATUS
============================================================
Total Feeds: 8
Active Feeds: 8

📡 ThreatFox Recent IOCs
   Status: 🟢 ACTIVE
   Last Update: Never
   Interval: 30 minutes

📡 URLhaus Recent URLs  
   Status: 🟢 ACTIVE
   Last Update: Never
   Interval: 30 minutes
```

## 📊 Available Feed Sources

The examples demonstrate integration with these public threat intelligence feeds:

| Feed Source | Type | Update Frequency | IOC Types |
|-------------|------|-----------------|-----------|
| **ThreatFox** | JSON | 30 min | Malware IOCs, C2s |
| **URLhaus** | JSON | 30 min | Malicious URLs |
| **Bambenek** | Text | 2 hours | C2 Domains |
| **FireHOL** | Text | 1 hour | Malicious IPs |
| **PhishTank** | XML | 30 min | Phishing URLs |
| **Malware Domain List** | Text | 1 hour | Malware Domains |

## 🔧 Configuration Examples

### Basic Feed Setup

```python
from threatcrew.managers.threat_feed_manager import get_threat_feed_manager

tfm = get_threat_feed_manager()

# Add a custom feed
tfm.add_custom_feed(
    name="Custom Threat Feed",
    url="https://your-feed-url.com/data.json",
    feed_type="json", 
    update_interval=60,  # minutes
    headers={"Authorization": "Bearer YOUR_API_KEY"}
)
```

### Automated Monitoring

```python
import asyncio

async def start_monitoring():
    tfm = get_threat_feed_manager()
    
    # This runs indefinitely, collecting and classifying IOCs
    await tfm.start_feed_monitoring()

# Run in production
asyncio.run(start_monitoring())
```

### Accessing Collected IOCs

```python
from threatcrew.tools.memory_system import get_memory

memory = get_memory()

# Search for IOCs by type
domains = memory.search_iocs('domain')
ips = memory.search_iocs('ip')
urls = memory.search_iocs('url')

# Get high-confidence IOCs
high_confidence = memory.search_iocs_by_confidence(min_confidence=0.8)

# Search by source
threatfox_iocs = memory.search_iocs_by_source('ThreatFox')
```

## 🚀 Running the Examples

### Prerequisites

1. **Install ThreatAgent:**
   ```bash
   cd threatcrew
   pip install -r requirements.txt
   ```

2. **Configure real data mode:**
   ```bash
   python configure_data_sources.py real-only
   ```

3. **Run examples:**
   ```bash
   cd examples
   python quick_ingestion_demo.py
   ```

### Optional: API Keys for Enhanced Feeds

While the examples work with public feeds, you can enhance them with API-based feeds:

```bash
# Set environment variables for API keys
export OTX_API_KEY="your_otx_api_key"
export VT_API_KEY="your_virustotal_key"  
export MISP_TOKEN="your_misp_token"
```

Then modify the examples to include API-based feeds:

```python
# AlienVault OTX (requires free API key)
tfm.add_custom_feed(
    name="AlienVault OTX",
    url="https://otx.alienvault.com/api/v1/indicators/export?type=domain",
    feed_type="json",
    update_interval=60,
    headers={"X-OTX-API-KEY": os.getenv("OTX_API_KEY")}
)
```

## 📊 Output Examples

### Feed Processing Output

```
📡 Updating feed: ThreatFox Recent IOCs
📊 Processing 1,247 IOCs from ThreatFox Recent IOCs
✅ Classified: malware.banking.trojan (confidence: 0.92)
✅ Classified: c2.communication (confidence: 0.87)
✅ Classified: phishing.credential_theft (confidence: 0.95)
```

### Memory Storage

```python
# Example IOC stored in memory
{
    "ioc": "malicious-banking-site.com",
    "ioc_type": "domain",
    "risk_level": "HIGH",
    "category": "malware.banking",
    "confidence": 0.92,
    "source": "ThreatFox Recent IOCs",
    "metadata": {
        "classification_reasoning": "Domain exhibits banking trojan C2 patterns",
        "feed_source": "ThreatFox Recent IOCs", 
        "ingestion_time": "2024-01-15T14:30:00Z"
    }
}
```

## 🔍 Next Steps

1. **Read the full guide:** [LEVEL_1_INGESTION_GUIDE.md](../LEVEL_1_INGESTION_GUIDE.md)
2. **Configure production deployment:** See production sections in the guide
3. **Add commercial feeds:** Configure API keys for premium threat intelligence
4. **Monitor and tune:** Use the monitoring examples to track feed performance
5. **Integrate with SIEM:** Export IOCs to your security infrastructure

## 🤝 Contributing Examples

Have a useful example? Contribute it:

1. Create a new Python file with clear documentation
2. Follow the existing example structure
3. Include error handling and logging
4. Add usage instructions to this README
5. Submit a pull request

## 📞 Support

- **Documentation:** See [LEVEL_1_INGESTION_GUIDE.md](../LEVEL_1_INGESTION_GUIDE.md)
- **Issues:** Open an issue on GitHub
- **Configuration:** Use `python configure_data_sources.py --help`
