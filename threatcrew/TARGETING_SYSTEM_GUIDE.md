# ThreatAgent Targeting System Documentation

## Overview

The ThreatAgent Targeting System provides comprehensive capabilities for focused threat intelligence gathering. It allows security teams to create targeted campaigns that focus on specific companies, industries, geographic regions, and threat types.

## Key Features

### 🎯 **Targeting Capabilities**
- **Company Targeting**: Focus on specific organizations
- **Industry Targeting**: Target entire industry sectors with predefined profiles
- **Domain Targeting**: Monitor specific domains and their variations
- **URL Targeting**: Track specific URLs and endpoints
- **Geographic Targeting**: Focus on specific countries/regions
- **Threat Type Filtering**: Filter by threat categories (phishing, malware, APT, etc.)

### 📊 **Predefined Industry Profiles**
- **Financial Services**: Banking, insurance, fintech
- **Healthcare**: Hospitals, medical devices, pharma
- **Technology**: Software, cloud services, startups
- **Government**: Federal, state, local agencies
- **Energy**: Utilities, oil & gas, renewable energy
- **Retail**: E-commerce, POS systems, supply chain

### 🔍 **Smart Search Filtering**
- Automatic keyword generation based on targets
- Domain pattern matching
- Threat indicator correlation
- Priority-based filtering

## Quick Start

### 1. Basic Campaign Creation

```python
from threatcrew.config.threat_targeting import get_targeting_system

# Initialize targeting system
targeting_system = get_targeting_system()

# Create a new campaign
campaign_id = targeting_system.create_campaign(
    campaign_name="Financial Phishing Campaign",
    description="Monitor phishing attacks against financial institutions",
    priority=5
)
```

### 2. Adding Targets

```python
# Add company targets
targeting_system.add_company_target(campaign_id, "JPMorgan Chase", priority=5)
targeting_system.add_company_target(campaign_id, "Bank of America", priority=4)

# Add industry target (uses predefined profile)
targeting_system.add_industry_target(campaign_id, "financial_services", priority=5)

# Add domain targets
targeting_system.add_domain_target(campaign_id, "jpmorgan.com", priority=4)

# Add URL targets
targeting_system.add_url_target(campaign_id, "https://suspicious-bank-login.com", priority=5)
```

### 3. Configure Threat Types and Geography

```python
# Set threat types to focus on
targeting_system.set_threat_types(campaign_id, [
    "phishing", 
    "credential_harvesting", 
    "business_email_compromise"
])

# Set geographic focus
targeting_system.set_geographic_focus(campaign_id, [
    "United States", 
    "Canada", 
    "United Kingdom"
])
```

### 4. Generate Search Filters

```python
# Get campaign configuration
config = targeting_system.get_campaign_config(campaign_id)

# Generate search filters for agents
search_filters = config.generate_search_filters()

print(f"Keywords: {search_filters['keywords']}")
print(f"Domains: {search_filters['domains']}")
print(f"Threat indicators: {search_filters['threat_indicators']}")
```

### 5. Run Targeted Workflow

```python
from threatcrew.main import run

# Run threat intelligence workflow with targeting
result = run(targeting_config=config)

print(f"Status: {result['status']}")
print(f"Domains analyzed: {len(result.get('domains', []))}")
```

## Advanced Usage

### Campaign Management

```python
# List all campaigns
campaigns = targeting_system.list_campaigns()

# Get campaign summary
summary = targeting_system.get_campaign_summary(campaign_id)

# Export campaign configuration
targeting_system.export_campaign(campaign_id, "campaign_backup.yaml")

# Import campaign configuration
new_campaign_id = targeting_system.import_campaign("campaign_backup.yaml")
```

### Custom Targets

```python
# Add custom target with specific attributes
targeting_system.add_custom_target(
    campaign_id=campaign_id,
    target_type="custom",
    value="cryptocurrency_exchange",
    keywords=["bitcoin", "ethereum", "wallet", "exchange"],
    domains=["*.crypto", "*.blockchain"],
    priority=4
)
```

### Industry Profile Customization

Available industry profiles:
- `financial_services`: Banks, credit unions, payment processors
- `healthcare`: Hospitals, clinics, medical device manufacturers
- `technology`: Software companies, cloud providers, startups
- `government`: Federal agencies, state/local government
- `energy`: Power plants, oil refineries, renewable energy
- `retail`: E-commerce, brick-and-mortar stores, supply chain

Each profile includes:
- Industry-specific keywords
- Common domain patterns
- Typical threat vectors
- Regulatory considerations

## Integration with CrewAI Agents

The targeting system seamlessly integrates with ThreatAgent's CrewAI workflow:

### 🕵️ **Recon Agent Enhancement**
- Uses targeting keywords for focused OSINT collection
- Prioritizes domains matching target organizations
- Filters results based on geographic and threat type relevance

### 🔬 **Analyst Agent Enhancement**
- Applies target-aware risk scoring
- Considers industry-specific threat patterns
- Prioritizes analysis based on target relevance

### 📝 **Exporter Agent Enhancement**
- Generates target-specific reports
- Includes industry context and recommendations
- Customizes detection rules for target environment

## Configuration Files

### Campaign Configuration (YAML)
```yaml
campaign_name: "Financial Phishing Campaign"
description: "Monitor phishing attacks against financial institutions"
priority: 5
created_date: "2025-01-15T10:30:00Z"
targets:
  - target_type: "company"
    value: "JPMorgan Chase"
    priority: 5
  - target_type: "industry"
    value: "financial_services"
    priority: 5
threat_types:
  - "phishing"
  - "credential_harvesting"
geographic_focus:
  - "United States"
  - "Canada"
```

## Best Practices

### 1. **Priority Management**
- Use priority 5 for critical targets (major customers, high-value assets)
- Use priority 4 for important targets (key partners, strategic assets)
- Use priority 3 for standard targets (general monitoring)
- Use priority 1-2 for low-priority or experimental targets

### 2. **Campaign Design**
- Keep campaigns focused (3-7 primary targets)
- Align threat types with actual risk profile
- Review and update campaigns regularly
- Use descriptive names and documentation

### 3. **Geographic Targeting**
- Focus on regions where your organization operates
- Consider threat actor geographic patterns
- Include regions with relevant regulatory requirements

### 4. **Industry Profiles**
- Start with predefined profiles when available
- Customize based on specific organizational needs
- Regular update keywords based on emerging threats

## Troubleshooting

### Common Issues

1. **Campaign Creation Fails**
   - Check campaign name uniqueness
   - Verify priority is between 1-5
   - Ensure description is provided

2. **Search Filters Empty**
   - Verify targets are properly configured
   - Check industry profile availability
   - Ensure threat types are set

3. **Workflow Integration Issues**
   - Confirm targeting configuration is passed correctly
   - Check agent prompt modifications
   - Verify search filter generation

### Debugging

```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Check campaign configuration
config = targeting_system.get_campaign_config(campaign_id)
print(f"Campaign: {config.campaign_name}")
print(f"Targets: {len(config.targets)}")
print(f"Threat types: {config.threat_types}")

# Validate search filters
search_filters = config.generate_search_filters()
print(f"Generated filters: {search_filters}")
```

## API Reference

See the full API documentation in `src/threatcrew/config/threat_targeting.py` for detailed method signatures and parameters.

## Examples

See the following demo scripts for complete examples:
- `demo_targeting_system.py`: Comprehensive demonstration
- `test_targeting_integration.py`: Integration testing
- `simple_run.py`: Basic usage example

---

For more information about ThreatAgent's enhanced features, see:
- `ENHANCED_SYSTEM_IMPLEMENTATION.md`
- `MEMORY_FINETUNING_GUIDE.md`
- `DOCUMENTATION_UPDATE_SUMMARY.md`
