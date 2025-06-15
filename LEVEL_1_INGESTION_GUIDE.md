# 🌐 Level 1 Threat Intelligence Ingestion Guide

## Overview

ThreatAgent's Level 1 ingestion system automatically collects, processes, and classifies threat intelligence from public and commercial feeds. The built-in `ThreatFeedManager` handles multiple feed formats (JSON, XML, CSV, text), extracts Indicators of Compromise (IOCs), and stores them in the memory database with AI-powered classification.

## 🏗️ System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Public Feeds  │    │  ThreatFeed     │    │   Memory DB     │
│                 │    │   Manager       │    │                 │
│ • AlienVault    │───▶│                 │───▶│ • Classified    │
│ • MISP          │    │ • Fetch         │    │   IOCs          │
│ • ThreatFox     │    │ • Parse         │    │ • Risk Levels   │
│ • CyberCrime    │    │ • Classify      │    │ • Source Track  │
│ • Bambenek      │    │ • Store         │    │ • Confidence    │
│ • FireHOL       │    │                 │    │   Scores        │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🚀 Quick Start

### 1. Initialize ThreatFeedManager

```python
from threatcrew.managers.threat_feed_manager import get_threat_feed_manager

# Get the manager instance
tfm = get_threat_feed_manager()

# Check default feeds
print("Default feeds:", [feed.name for feed in tfm.feeds])
```

### 2. Add Custom Feeds

```python
# AlienVault OTX
tfm.add_custom_feed(
    name="AlienVault OTX Domains",
    url="https://otx.alienvault.com/api/v1/indicators/export?type=domain",
    feed_type="json",
    update_interval=60,  # 1 hour
    headers={"X-OTX-API-KEY": "YOUR_OTX_API_KEY"}
)

# MISP OSINT Feed
tfm.add_custom_feed(
    name="MISP OSINT",
    url="https://your-misp-instance.com/events/restSearch",
    feed_type="json",
    update_interval=120,  # 2 hours
    headers={"Authorization": "Bearer YOUR_MISP_TOKEN"}
)

# ThreatFox (Abuse.ch)
tfm.add_custom_feed(
    name="ThreatFox IOCs",
    url="https://threatfox.abuse.ch/export/json/recent/",
    feed_type="json",
    update_interval=30  # 30 minutes
)
```

### 3. Start Ingestion

```python
import asyncio

async def start_ingestion():
    await tfm.start_feed_monitoring()

# Run the ingestion loop
asyncio.run(start_ingestion())
```

## 📋 Supported Feed Sources

### Public Intelligence Feeds

#### 1. **AlienVault OTX (Open Threat Exchange)**
```python
tfm.add_custom_feed(
    name="AlienVault OTX Domains",
    url="https://otx.alienvault.com/api/v1/indicators/export?type=domain",
    feed_type="json",
    update_interval=60,
    headers={"X-OTX-API-KEY": "YOUR_API_KEY"}
)

# Additional OTX feeds
tfm.add_custom_feed(
    name="AlienVault OTX IPs",
    url="https://otx.alienvault.com/api/v1/indicators/export?type=IPv4",
    feed_type="json",
    update_interval=60,
    headers={"X-OTX-API-KEY": "YOUR_API_KEY"}
)
```

#### 2. **MISP (Malware Information Sharing Platform)**
```python
tfm.add_custom_feed(
    name="MISP OSINT Feed",
    url="https://misp.circl.lu/events/restSearch",
    feed_type="json",
    update_interval=120,
    headers={
        "Authorization": "Bearer YOUR_MISP_TOKEN",
        "Accept": "application/json"
    }
)
```

#### 3. **ThreatFox (Abuse.ch)**
```python
tfm.add_custom_feed(
    name="ThreatFox Recent IOCs",
    url="https://threatfox.abuse.ch/export/json/recent/",
    feed_type="json",
    update_interval=30
)

tfm.add_custom_feed(
    name="ThreatFox Full Database",
    url="https://threatfox.abuse.ch/export/json/full/",
    feed_type="json",
    update_interval=1440  # Daily
)
```

#### 4. **CyberCrime Tracker**
```python
tfm.add_custom_feed(
    name="CyberCrime Tracker",
    url="http://cybercrime-tracker.net/rss.xml",
    feed_type="xml",
    update_interval=60
)
```

#### 5. **Bambenek Consulting Feeds**
```python
# C2 Domains
tfm.add_custom_feed(
    name="Bambenek C2 Domains",
    url="http://osint.bambenekconsulting.com/feeds/c2-dommasterlist.txt",
    feed_type="text",
    update_interval=120
)

# DGA Domains
tfm.add_custom_feed(
    name="Bambenek DGA Domains",
    url="http://osint.bambenekconsulting.com/feeds/dga-feed.txt",
    feed_type="text",
    update_interval=60
)
```

#### 6. **FireHOL IP Lists**
```python
# Malicious IPs
tfm.add_custom_feed(
    name="FireHOL Level 1",
    url="https://iplists.firehol.org/files/firehol_level1.netset",
    feed_type="text",
    update_interval=60
)

# Anonymous proxies
tfm.add_custom_feed(
    name="FireHOL Anonymous",
    url="https://iplists.firehol.org/files/anonymous.netset",
    feed_type="text",
    update_interval=120
)
```

#### 7. **URLhaus (Abuse.ch)**
```python
tfm.add_custom_feed(
    name="URLhaus Recent URLs",
    url="https://urlhaus.abuse.ch/downloads/json/",
    feed_type="json",
    update_interval=30
)
```

### Commercial/Premium Feeds

#### 8. **KELA DarkFeed**
```python
tfm.add_custom_feed(
    name="KELA DarkFeed",
    url="https://api.ke-la.com/feeds/darkfeed/json",
    feed_type="json",
    update_interval=180,  # 3 hours
    headers={"X-API-Key": "YOUR_KELA_API_KEY"}
)
```

## 🔧 Configuration Options

### Feed Types and Formats

| Feed Type | Description | Example Sources |
|-----------|-------------|-----------------|
| `json` | JSON API responses | OTX, MISP, ThreatFox |
| `xml` | XML/RSS feeds | CyberCrime Tracker, PhishTank |
| `csv` | Comma-separated values | Custom threat feeds |
| `text` | Plain text lists | Bambenek, FireHOL |

### Update Intervals

```python
# Update intervals in minutes
INTERVALS = {
    "real-time": 5,      # Every 5 minutes
    "frequent": 15,      # Every 15 minutes  
    "normal": 60,        # Every hour
    "slow": 240,         # Every 4 hours
    "daily": 1440        # Once per day
}
```

### Custom Headers

```python
# Common authentication methods
headers_examples = {
    # API Key in header
    "X-API-Key": "your_api_key",
    "X-OTX-API-KEY": "your_otx_key",
    
    # Bearer token
    "Authorization": "Bearer your_token",
    
    # Basic auth
    "Authorization": "Basic base64_credentials",
    
    # Content type
    "Accept": "application/json",
    "Content-Type": "application/json"
}
```

## 🎯 Advanced Usage

### 1. Feed Status Monitoring

```python
# Check feed statistics
stats = tfm.get_feed_stats()
for feed_name, stats in stats.items():
    print(f"{feed_name}: {stats['iocs_processed']} IOCs, "
          f"Last update: {stats['last_updated']}")

# Get specific feed info
feed_info = tfm.get_feed_info("AlienVault OTX")
print(f"Feed active: {feed_info['active']}")
print(f"Next update: {feed_info['next_update']}")
```

### 2. Manual Feed Processing

```python
# Process a specific feed immediately
await tfm.process_feed_by_name("ThreatFox Recent IOCs")

# Process all feeds once
await tfm.process_all_feeds_once()
```

### 3. Custom IOC Extraction

```python
class CustomThreatFeedManager(ThreatFeedManager):
    def _extract_from_custom_format(self, content: str, feed: ThreatFeed):
        """Custom extraction logic for proprietary formats."""
        iocs = []
        
        # Custom parsing logic here
        lines = content.strip().split('\n')
        for line in lines:
            if line.startswith('MALWARE:'):
                domain = line.split(':')[1].strip()
                iocs.append({
                    'ioc': domain,
                    'ioc_type': 'domain',
                    'metadata': {'source_line': line}
                })
        
        return iocs
```

### 4. Feed Filtering and Validation

```python
# Add validation rules
tfm.add_validation_rule("domain", lambda x: len(x.split('.')) >= 2)
tfm.add_validation_rule("ip", lambda x: all(0 <= int(part) <= 255 
                                          for part in x.split('.')))

# Filter by source quality
tfm.set_source_priority({
    "ThreatFox": 10,
    "AlienVault OTX": 9,
    "MISP": 8,
    "Bambenek": 7
})
```

## 🔄 Automated Processing Pipeline

### 1. IOC Classification

Every ingested IOC is automatically classified:

```python
# Automatic classification flow
classification_result = classify_iocs(ioc_data["ioc"])

# Result includes:
{
    "risk_level": "HIGH",      # LOW, MEDIUM, HIGH, CRITICAL
    "category": "malware",     # malware, phishing, c2, etc.
    "confidence": 0.85,        # 0.0 to 1.0
    "reasoning": "Domain shows characteristics of malware C2"
}
```

### 2. Memory Storage

```python
# Automatic storage with metadata
ioc_id = memory.store_ioc(
    ioc=ioc_data["ioc"],
    ioc_type=ioc_data["ioc_type"], 
    risk_level=classification_result["risk_level"],
    category=classification_result["category"],
    confidence=classification_result["confidence"],
    source=feed.name,
    metadata={
        "feed_url": feed.url,
        "ingestion_time": datetime.now().isoformat(),
        "classification_reasoning": classification_result["reasoning"]
    }
)
```

### 3. Analysis History

```python
# Automatic analysis logging
memory.store_analysis(
    analysis_type="feed_ingestion",
    input_data=ioc_data["ioc"],
    output_data=json.dumps(classification_result),
    confidence=classification_result["confidence"],
    metadata={
        "source_feed": feed.name,
        "processing_time": processing_time,
        "ioc_id": ioc_id
    }
)
```

## 📊 Monitoring and Metrics

### 1. Feed Performance Metrics

```python
# Get processing statistics
metrics = tfm.get_processing_metrics()
print(f"Total IOCs processed: {metrics['total_iocs']}")
print(f"Processing rate: {metrics['iocs_per_hour']}/hour")
print(f"Average confidence: {metrics['avg_confidence']:.2f}")
print(f"Feed uptime: {metrics['uptime_percentage']:.1f}%")
```

### 2. Quality Metrics

```python
# Quality assessment
quality = tfm.get_quality_metrics()
print(f"High confidence IOCs: {quality['high_confidence_pct']:.1f}%")
print(f"Unique IOCs: {quality['unique_iocs']}")
print(f"Duplicate rate: {quality['duplicate_rate']:.1f}%")
```

### 3. Real-time Monitoring

```python
# Set up monitoring callbacks
def on_ioc_processed(ioc_data, classification):
    if classification['risk_level'] == 'CRITICAL':
        send_alert(f"Critical IOC detected: {ioc_data['ioc']}")

def on_feed_error(feed_name, error):
    log_feed_error(feed_name, error)

tfm.add_callback('ioc_processed', on_ioc_processed)
tfm.add_callback('feed_error', on_feed_error)
```

## 🛡️ Security and Best Practices

### 1. API Key Management

```python
# Use environment variables for API keys
import os

tfm.add_custom_feed(
    name="AlienVault OTX",
    url="https://otx.alienvault.com/api/v1/indicators/export?type=domain",
    feed_type="json",
    update_interval=60,
    headers={"X-OTX-API-KEY": os.getenv("OTX_API_KEY")}
)
```

### 2. Rate Limiting

```python
# Configure rate limits
tfm.configure_rate_limits({
    "requests_per_minute": 30,
    "requests_per_hour": 1000,
    "concurrent_feeds": 5
})
```

### 3. Error Handling

```python
# Custom error handling
class FeedErrorHandler:
    def handle_network_error(self, feed, error):
        # Exponential backoff
        pass
    
    def handle_parsing_error(self, feed, content, error):
        # Log and skip malformed data
        pass
    
    def handle_auth_error(self, feed, error):
        # Refresh tokens
        pass

tfm.set_error_handler(FeedErrorHandler())
```

## 🔧 Integration with Recon Agent

### Using the Recon Agent for OSINT Collection

```python
from threatcrew.crew import ThreatCrew

# Initialize crew with recon agent
crew = ThreatCrew()

# Task the recon agent to scan specific feeds
recon_task = {
    "task": "scan_threat_feeds",
    "targets": [
        "otx.alienvault.com",
        "threatfox.abuse.ch", 
        "cybercrime-tracker.net"
    ],
    "keywords": ["banking", "malware", "phishing"],
    "scope": "public_feeds"
}

# Run recon and feed into pipeline
results = crew.run([recon_task])
```

### OSINT Scraper Integration

```python
from threatcrew.tools.osint_scraper import scrape_osint

# Enhanced OSINT collection
osint_results = scrape_osint(
    targets=["pastebin.com", "twitter.com", "github.com"],
    keywords=["malware", "leaked", "breach"],
    scope="public"
)

# Results automatically fed into memory system
```

## 📝 Configuration File Example

Create `threat_feeds_config.yaml`:

```yaml
threat_feeds:
  default_settings:
    timeout: 30
    retry_attempts: 3
    rate_limit: 60  # requests per hour
  
  feeds:
    - name: "AlienVault OTX"
      url: "https://otx.alienvault.com/api/v1/indicators/export?type=domain"
      type: "json"
      interval: 60
      priority: 9
      auth:
        type: "api_key"
        header: "X-OTX-API-KEY"
        key_env: "OTX_API_KEY"
    
    - name: "ThreatFox"
      url: "https://threatfox.abuse.ch/export/json/recent/"
      type: "json" 
      interval: 30
      priority: 10
      
    - name: "Bambenek C2"
      url: "http://osint.bambenekconsulting.com/feeds/c2-dommasterlist.txt"
      type: "text"
      interval: 120
      priority: 7
```

## 🚀 Production Deployment

### 1. Systemd Service

Create `/etc/systemd/system/threatagent-feeds.service`:

```ini
[Unit]
Description=ThreatAgent Feed Ingestion
After=network.target

[Service]
Type=simple
User=threatagent
WorkingDirectory=/opt/threatagent
ExecStart=/opt/threatagent/venv/bin/python -m threatcrew.feeds
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### 2. Docker Deployment

```dockerfile
FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "-m", "threatcrew.feeds", "--config", "/config/feeds.yaml"]
```

### 3. Monitoring Setup

```python
# Prometheus metrics
from prometheus_client import Counter, Histogram, start_http_server

iocs_processed = Counter('threatagent_iocs_processed_total', 
                        'Total IOCs processed', ['feed', 'type'])
processing_time = Histogram('threatagent_processing_seconds',
                           'Time spent processing feeds', ['feed'])

# Start metrics server
start_http_server(8000)
```

## 📈 Performance Optimization

### 1. Parallel Processing

```python
# Process multiple feeds concurrently
tfm.configure_concurrency({
    "max_concurrent_feeds": 10,
    "max_concurrent_iocs": 100,
    "worker_pool_size": 20
})
```

### 2. Caching

```python
# Enable response caching
tfm.enable_caching({
    "cache_ttl": 300,  # 5 minutes
    "max_cache_size": "100MB",
    "cache_backend": "redis"  # or "memory"
})
```

### 3. Database Optimization

```python
# Batch IOC storage
tfm.configure_storage({
    "batch_size": 1000,
    "batch_timeout": 30,  # seconds
    "enable_indexing": True
})
```

## 🔍 Troubleshooting

### Common Issues

1. **API Rate Limits**: Increase update intervals
2. **Authentication Errors**: Verify API keys and tokens
3. **Network Timeouts**: Adjust timeout settings
4. **Memory Issues**: Enable batch processing
5. **Feed Format Changes**: Update parsers

### Debug Mode

```python
# Enable debug logging
tfm.set_debug_mode(True)

# Get detailed feed status
debug_info = tfm.get_debug_info()
print(json.dumps(debug_info, indent=2))
```

## 📚 Summary

ThreatAgent's Level 1 ingestion provides:

- ✅ **Automated Collection**: 24/7 monitoring of multiple threat feeds
- ✅ **AI Classification**: Automatic risk assessment and categorization  
- ✅ **Real Data Integration**: Direct integration with the real-data-only training system
- ✅ **Scalable Architecture**: Handle dozens of feeds simultaneously
- ✅ **Quality Assurance**: Validation, deduplication, and confidence scoring
- ✅ **Production Ready**: Monitoring, alerting, and error handling

The system automatically transforms raw threat intelligence feeds into actionable, classified IOCs stored in the memory database for enhanced threat analysis and model training.
