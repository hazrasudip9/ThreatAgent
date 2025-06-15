"""
ThreatAgent Target Configuration System
======================================

This module provides comprehensive targeting capabilities for focused threat intelligence gathering.
Users can specify URLs, companies, industries, threat types, and custom parameters.
"""

import json
import yaml
import os
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from pathlib import Path
from ..utils.campaign_file import save_campaign_file

@dataclass
class ThreatTarget:
    """Individual threat target configuration."""
    name: str
    target_type: str  # 'company', 'industry', 'url', 'domain', 'custom'
    value: str
    priority: int = 1  # 1-5, where 5 is highest
    active: bool = True
    tags: List[str] = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []
        if self.metadata is None:
            self.metadata = {}

@dataclass
class IndustryTarget:
    """Industry-specific targeting configuration."""
    industry: str
    keywords: List[str]
    common_domains: List[str]
    threat_vectors: List[str]
    regulatory_focus: List[str] = None
    
    def __post_init__(self):
        if self.regulatory_focus is None:
            self.regulatory_focus = []

@dataclass
class ThreatIntelligenceConfig:
    """Complete threat intelligence targeting configuration."""
    campaign_name: str
    targets: List[ThreatTarget]
    industries: List[IndustryTarget]
    threat_types: List[str]
    geographic_focus: List[str]
    time_range: Dict[str, str]
    confidence_threshold: float = 0.7
    active: bool = True
    created_at: str = None
    updated_at: str = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()
        if self.updated_at is None:
            self.updated_at = self.created_at
    
    def generate_search_filters(self) -> Dict[str, Any]:
        """Generate search filters based on the campaign configuration."""
        keywords = set()
        domains = set()
        
        # Extract keywords and domains from targets
        for target in self.targets:
            if target.target_type == "company":
                keywords.add(target.name.lower())
                keywords.add(target.value.lower())
                if target.metadata.get("domain"):
                    domains.add(target.metadata["domain"])
            elif target.target_type == "industry":
                industry_keywords = target.metadata.get("keywords", [])
                keywords.update([kw.lower() for kw in industry_keywords])
            elif target.target_type == "domain":
                domains.add(target.value)
            elif target.target_type in ["url"]:
                keywords.add(target.value.lower())
                
        return {
            "keywords": list(keywords),
            "domains": list(domains), 
            "threat_types": self.threat_types,
            "geographic_focus": self.geographic_focus,
            "confidence_threshold": self.confidence_threshold,
            "high_priority_targets": [t.value for t in self.targets if t.priority >= 4 and t.active]
        }

class ThreatTargetingSystem:
    """Manages threat intelligence targeting and configuration."""
    
    def __init__(self, config_dir: str = None):
        if config_dir is None:
            config_dir = os.path.join(os.path.dirname(__file__), "..", "..", "config")
        
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        self.targets_file = self.config_dir / "threat_targets.yaml"
        self.industries_file = self.config_dir / "industry_profiles.yaml"
        self.campaigns_file = self.config_dir / "campaigns.yaml"
        
        # Initialize predefined industry profiles
        self._initialize_industry_profiles()
        
        # Load existing configurations
        self.current_config = self._load_current_config()
    
    def _initialize_industry_profiles(self):
        """Initialize predefined industry threat profiles."""
        
        industry_profiles = {
            "financial_services": IndustryTarget(
                industry="Financial Services",
                keywords=[
                    "bank", "banking", "finance", "credit", "loan", "mortgage",
                    "investment", "trading", "insurance", "fintech", "paypal",
                    "visa", "mastercard", "amex", "crypto", "blockchain"
                ],
                common_domains=[
                    "bank.com", "bankofamerica.com", "chase.com", "wellsfargo.com",
                    "paypal.com", "stripe.com", "visa.com", "mastercard.com"
                ],
                threat_vectors=[
                    "phishing", "business_email_compromise", "credential_harvesting",
                    "fake_banking_sites", "payment_fraud", "crypto_scams"
                ],
                regulatory_focus=["PCI-DSS", "SOX", "GDPR", "PSD2"]
            ),
            
            "healthcare": IndustryTarget(
                industry="Healthcare",
                keywords=[
                    "hospital", "medical", "health", "patient", "clinic", "pharmacy",
                    "medicare", "medicaid", "insurance", "hipaa", "ehr", "emr"
                ],
                common_domains=[
                    "mayo.edu", "clevelandclinic.org", "johnshopkins.edu",
                    "cdc.gov", "nih.gov", "who.int"
                ],
                threat_vectors=[
                    "ransomware", "data_theft", "patient_data_breach",
                    "medical_device_attacks", "supply_chain_attacks"
                ],
                regulatory_focus=["HIPAA", "HITECH", "FDA", "GDPR"]
            ),
            
            "technology": IndustryTarget(
                industry="Technology",
                keywords=[
                    "tech", "software", "cloud", "saas", "api", "developer",
                    "github", "aws", "azure", "google", "microsoft", "apple"
                ],
                common_domains=[
                    "microsoft.com", "google.com", "amazon.com", "apple.com",
                    "github.com", "stackoverflow.com", "docker.com"
                ],
                threat_vectors=[
                    "supply_chain_attacks", "code_injection", "api_abuse",
                    "insider_threats", "intellectual_property_theft"
                ],
                regulatory_focus=["SOC2", "ISO27001", "GDPR", "CCPA"]
            ),
            
            "government": IndustryTarget(
                industry="Government",
                keywords=[
                    "gov", "government", "federal", "state", "local", "military",
                    "defense", "embassy", "congress", "senate", "court"
                ],
                common_domains=[
                    "whitehouse.gov", "defense.gov", "state.gov", "treasury.gov",
                    "dhs.gov", "fbi.gov", "cia.gov", "nsa.gov"
                ],
                threat_vectors=[
                    "nation_state_attacks", "espionage", "election_interference",
                    "critical_infrastructure", "classified_data_theft"
                ],
                regulatory_focus=["FISMA", "NIST", "CISA", "FedRAMP"]
            ),
            
            "energy": IndustryTarget(
                industry="Energy & Utilities",
                keywords=[
                    "energy", "electric", "power", "utility", "grid", "oil",
                    "gas", "nuclear", "solar", "wind", "renewable", "scada"
                ],
                common_domains=[
                    "exxonmobil.com", "chevron.com", "bp.com", "shell.com",
                    "ge.com", "siemens.com", "schneider-electric.com"
                ],
                threat_vectors=[
                    "critical_infrastructure_attacks", "scada_attacks",
                    "industrial_espionage", "supply_chain_compromise"
                ],
                regulatory_focus=["NERC-CIP", "TSA", "CISA", "ICS-CERT"]
            ),
            
            "retail": IndustryTarget(
                industry="Retail & E-commerce",
                keywords=[
                    "retail", "shopping", "ecommerce", "store", "mall", "amazon",
                    "walmart", "target", "costco", "payment", "pos", "checkout"
                ],
                common_domains=[
                    "amazon.com", "walmart.com", "target.com", "costco.com",
                    "ebay.com", "etsy.com", "shopify.com", "stripe.com"
                ],
                threat_vectors=[
                    "pos_malware", "e-skimming", "payment_fraud",
                    "customer_data_theft", "inventory_manipulation"
                ],
                regulatory_focus=["PCI-DSS", "CCPA", "GDPR", "PIPEDA"]
            )
        }
        
        # Save industry profiles if file doesn't exist
        if not self.industries_file.exists():
            with open(self.industries_file, 'w') as f:
                yaml.dump({k: asdict(v) for k, v in industry_profiles.items()}, f, default_flow_style=False)
    
    def _load_current_config(self) -> Optional[ThreatIntelligenceConfig]:
        """Load current threat intelligence configuration."""
        if self.campaigns_file.exists():
            with open(self.campaigns_file, 'r') as f:
                data = yaml.safe_load(f)
                if data and 'current_campaign' in data:
                    campaign_data = data['current_campaign']
                    # Fix: convert dicts to ThreatTarget/IndustryTarget objects
                    targets = [ThreatTarget(**t) if not isinstance(t, ThreatTarget) else t for t in campaign_data.get('targets', [])]
                    industries = [IndustryTarget(**i) if not isinstance(i, IndustryTarget) else i for i in campaign_data.get('industries', [])]
                    campaign_data['targets'] = targets
                    campaign_data['industries'] = industries
                    return ThreatIntelligenceConfig(**campaign_data)
        return None
    
    def create_campaign(self, campaign_name: str, description: str = "") -> ThreatIntelligenceConfig:
        """Create a new threat intelligence campaign."""
        
        config = ThreatIntelligenceConfig(
            campaign_name=campaign_name,
            targets=[],
            industries=[],
            threat_types=["phishing", "malware", "credential_theft", "data_breach"],
            geographic_focus=["global"],
            time_range={
                "start": datetime.now().isoformat(),
                "end": None
            },
            confidence_threshold=0.7
        )
        
        self.current_config = config
        self._save_campaign(config)
        
        return config
    
    def add_company_target(self, company_name: str, domain: str = None, 
                          industry: str = None, priority: int = 3,
                          tags: List[str] = None) -> ThreatTarget:
        """Add a company as a threat intelligence target."""
        
        target = ThreatTarget(
            name=company_name,
            target_type="company",
            value=domain or f"{company_name.lower().replace(' ', '')}.com",
            priority=priority,
            tags=tags or [],
            metadata={
                "industry": industry,
                "domain": domain,
                "added_date": datetime.now().isoformat()
            }
        )
        
        if self.current_config:
            self.current_config.targets.append(target)
            self.current_config.updated_at = datetime.now().isoformat()
            self._save_campaign(self.current_config)
        
        return target
    
    def add_industry_target(self, industry_name: str, priority: int = 3,
                          custom_keywords: List[str] = None) -> ThreatTarget:
        """Add an industry as a threat intelligence target."""
        
        # Load industry profile if it exists
        industry_profile = self._get_industry_profile(industry_name)
        
        target = ThreatTarget(
            name=f"{industry_name} Industry",
            target_type="industry",
            value=industry_name,
            priority=priority,
            tags=["industry"],
            metadata={
                "keywords": custom_keywords or (industry_profile.keywords if industry_profile else []),
                "threat_vectors": industry_profile.threat_vectors if industry_profile else [],
                "regulatory_focus": industry_profile.regulatory_focus if industry_profile else [],
                "added_date": datetime.now().isoformat()
            }
        )
        
        if self.current_config:
            self.current_config.targets.append(target)
            self.current_config.updated_at = datetime.now().isoformat()
            self._save_campaign(self.current_config)
        
        return target
    
    def add_url_target(self, url: str, name: str = None, priority: int = 3,
                      tags: List[str] = None) -> ThreatTarget:
        """Add a specific URL as a threat intelligence target."""
        
        target = ThreatTarget(
            name=name or f"URL Target: {url}",
            target_type="url",
            value=url,
            priority=priority,
            tags=tags or ["url"],
            metadata={
                "url": url,
                "added_date": datetime.now().isoformat()
            }
        )
        
        if self.current_config:
            self.current_config.targets.append(target)
            self.current_config.updated_at = datetime.now().isoformat()
            self._save_campaign(self.current_config)
        
        return target
    
    def add_domain_target(self, domain: str, name: str = None, priority: int = 3,
                         tags: List[str] = None) -> ThreatTarget:
        """Add a domain as a threat intelligence target."""
        
        target = ThreatTarget(
            name=name or f"Domain: {domain}",
            target_type="domain",
            value=domain,
            priority=priority,
            tags=tags or ["domain"],
            metadata={
                "domain": domain,
                "added_date": datetime.now().isoformat()
            }
        )
        
        if self.current_config:
            self.current_config.targets.append(target)
            self.current_config.updated_at = datetime.now().isoformat()
            self._save_campaign(self.current_config)
        
        return target
    
    def add_custom_target(self, name: str, value: str, target_type: str = "custom",
                         priority: int = 3, tags: List[str] = None,
                         metadata: Dict[str, Any] = None) -> ThreatTarget:
        """Add a custom threat intelligence target."""
        
        target = ThreatTarget(
            name=name,
            target_type=target_type,
            value=value,
            priority=priority,
            tags=tags or [],
            metadata={
                **(metadata or {}),
                "added_date": datetime.now().isoformat()
            }
        )
        
        if self.current_config:
            self.current_config.targets.append(target)
            self.current_config.updated_at = datetime.now().isoformat()
            self._save_campaign(self.current_config)
        
        return target
    
    def set_threat_types(self, threat_types: List[str]):
        """Set the threat types to focus on."""
        if self.current_config:
            self.current_config.threat_types = threat_types
            self.current_config.updated_at = datetime.now().isoformat()
            self._save_campaign(self.current_config)
    
    def set_geographic_focus(self, regions: List[str]):
        """Set geographic regions to focus on."""
        if self.current_config:
            self.current_config.geographic_focus = regions
            self.current_config.updated_at = datetime.now().isoformat()
            self._save_campaign(self.current_config)
    
    def set_confidence_threshold(self, threshold: float):
        """Set minimum confidence threshold for threat intelligence."""
        if self.current_config:
            self.current_config.confidence_threshold = threshold
            self.current_config.updated_at = datetime.now().isoformat()
            self._save_campaign(self.current_config)
    
    def get_target_keywords(self) -> List[str]:
        """Get all keywords for current targets."""
        keywords = set()
        
        if not self.current_config:
            return []
        
        for target in self.current_config.targets:
            if target.target_type == "company":
                keywords.add(target.name.lower())
                keywords.add(target.value.lower())
            elif target.target_type == "industry":
                industry_keywords = target.metadata.get("keywords", [])
                keywords.update([kw.lower() for kw in industry_keywords])
            elif target.target_type in ["url", "domain"]:
                keywords.add(target.value.lower())
        
        return list(keywords)
    
    def get_target_domains(self) -> List[str]:
        """Get all domains for current targets."""
        domains = set()
        
        if not self.current_config:
            return []
        
        for target in self.current_config.targets:
            if target.target_type == "company" and target.metadata.get("domain"):
                domains.add(target.metadata["domain"])
            elif target.target_type == "domain":
                domains.add(target.value)
            elif target.target_type == "url":
                from urllib.parse import urlparse
                domain = urlparse(target.value).netloc
                if domain:
                    domains.add(domain)
        
        return list(domains)
    
    def get_high_priority_targets(self) -> List[ThreatTarget]:
        """Get targets with priority 4 or 5."""
        if not self.current_config:
            return []
        
        return [t for t in self.current_config.targets if t.priority >= 4 and t.active]
    
    def get_targets_by_type(self, target_type: str) -> List[ThreatTarget]:
        """Get targets by type (company, industry, url, domain, custom)."""
        if not self.current_config:
            return []
        
        return [t for t in self.current_config.targets if t.target_type == target_type and t.active]
    
    def get_targets_by_tag(self, tag: str) -> List[ThreatTarget]:
        """Get targets by tag."""
        if not self.current_config:
            return []
        
        return [t for t in self.current_config.targets if tag in t.tags and t.active]
    
    def generate_search_filters(self) -> Dict[str, Any]:
        """Generate search filters for threat intelligence gathering."""
        if not self.current_config:
            return {}
        
        return {
            "keywords": self.get_target_keywords(),
            "domains": self.get_target_domains(),
            "threat_types": self.current_config.threat_types,
            "geographic_focus": self.current_config.geographic_focus,
            "confidence_threshold": self.current_config.confidence_threshold,
            "high_priority_targets": [t.value for t in self.get_high_priority_targets()]
        }
    
    def _get_industry_profile(self, industry_name: str) -> Optional[IndustryTarget]:
        """Get industry profile by name."""
        try:
            with open(self.industries_file, 'r') as f:
                data = yaml.safe_load(f)
                if industry_name.lower() in data:
                    return IndustryTarget(**data[industry_name.lower()])
        except FileNotFoundError:
            pass
        return None
    
    def _save_campaign(self, config: ThreatIntelligenceConfig):
        """Save campaign configuration to file."""
        campaign_data = {
            "current_campaign": asdict(config),
            "last_updated": datetime.now().isoformat()
        }
        
        with open(self.campaigns_file, 'w') as f:
            yaml.dump(campaign_data, f, default_flow_style=False)
    
    def export_config(self, filepath: str = None) -> str:
        """Export current configuration to JSON/YAML file."""
        if not self.current_config:
            raise ValueError("No active campaign to export")
        
        campaign_data = asdict(self.current_config)
        if filepath is None:
            filepath = save_campaign_file(self.current_config.campaign_name, campaign_data)
        else:
            with open(filepath, 'w') as f:
                yaml.dump(campaign_data, f, default_flow_style=False)
        
        return filepath
    
    def import_config(self, filepath: str) -> ThreatIntelligenceConfig:
        """Import configuration from file."""
        with open(filepath, 'r') as f:
            if filepath.endswith('.json'):
                data = json.load(f)
            else:
                data = yaml.safe_load(f)
        
        config = ThreatIntelligenceConfig(**data)
        self.current_config = config
        self._save_campaign(config)
        
        return config
    
    def get_campaign_summary(self) -> Dict[str, Any]:
        """Get summary of current campaign."""
        if not self.current_config:
            return {"status": "no_active_campaign"}
        
        return {
            "campaign_name": self.current_config.campaign_name,
            "total_targets": len(self.current_config.targets),
            "active_targets": len([t for t in self.current_config.targets if t.active]),
            "target_breakdown": {
                "companies": len(self.get_targets_by_type("company")),
                "industries": len(self.get_targets_by_type("industry")),
                "urls": len(self.get_targets_by_type("url")),
                "domains": len(self.get_targets_by_type("domain")),
                "custom": len(self.get_targets_by_type("custom"))
            },
            "high_priority_targets": len(self.get_high_priority_targets()),
            "threat_types": self.current_config.threat_types,
            "geographic_focus": self.current_config.geographic_focus,
            "confidence_threshold": self.current_config.confidence_threshold,
            "created_at": self.current_config.created_at,
            "updated_at": self.current_config.updated_at
        }
    
    def list_campaigns(self) -> dict:
        """List all campaigns with summary info."""
        if not self.campaigns_file.exists():
            return {}
        with open(self.campaigns_file, 'r') as f:
            data = yaml.safe_load(f)
            if not data or 'campaigns' not in data:
                return {}
            return data['campaigns']

    def get_campaign_config(self, campaign_id: str) -> ThreatIntelligenceConfig:
        """Get the configuration for a specific campaign by ID."""
        if not self.campaigns_file.exists():
            raise ValueError("No campaigns file found.")
        with open(self.campaigns_file, 'r') as f:
            data = yaml.safe_load(f)
            if not data or 'campaigns' not in data:
                raise ValueError("No campaigns found.")
            campaign = data['campaigns'].get(campaign_id)
            if not campaign:
                raise ValueError(f"Campaign {campaign_id} not found.")
            targets = [ThreatTarget(**t) if not isinstance(t, ThreatTarget) else t for t in campaign.get('targets', [])]
            industries = [IndustryTarget(**i) if not isinstance(i, IndustryTarget) else i for i in campaign.get('industries', [])]
            campaign['targets'] = targets
            campaign['industries'] = industries
            return ThreatIntelligenceConfig(**campaign)

# Global targeting system instance
_targeting_system = None

def get_targeting_system() -> ThreatTargetingSystem:
    """Get the global threat targeting system instance."""
    global _targeting_system
    if _targeting_system is None:
        _targeting_system = ThreatTargetingSystem()
    return _targeting_system

# Predefined threat type categories
THREAT_TYPES = {
    "phishing": "Phishing campaigns and credential harvesting",
    "malware": "Malware distribution and C2 infrastructure",
    "ransomware": "Ransomware campaigns and payment infrastructure",
    "data_breach": "Data exfiltration and insider threats",
    "supply_chain": "Supply chain compromise and third-party risks",
    "nation_state": "Advanced persistent threats and espionage",
    "fraud": "Financial fraud and business email compromise",
    "ddos": "Distributed denial of service attacks",
    "insider_threat": "Malicious insider activities",
    "iot_attacks": "Internet of Things device compromise"
}

# Predefined geographic regions
GEOGRAPHIC_REGIONS = {
    "north_america": ["US", "CA", "MX"],
    "europe": ["UK", "DE", "FR", "IT", "ES", "NL", "CH"],
    "asia_pacific": ["JP", "CN", "KR", "AU", "IN", "SG"],
    "middle_east": ["AE", "SA", "IL", "TR"],
    "south_america": ["BR", "AR", "CL", "CO"],
    "africa": ["ZA", "NG", "EG", "KE"],
    "global": ["*"]
}

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="ThreatAgent Campaign Enrichment Tool")
    parser.add_argument("enrich", nargs="?", help="Enrich a minimal campaign YAML file")
    parser.add_argument("campaign_file", nargs="?", help="Path to the minimal campaign YAML file")
    args = parser.parse_args()

    if args.enrich and args.campaign_file:
        # Load minimal campaign
        with open(args.campaign_file, 'r') as f:
            data = yaml.safe_load(f)
        # Get targeting system
        targeting = get_targeting_system()
        # Create enriched config
        config = targeting.create_campaign(data.get("company_name") or data.get("campaign_name", "Untitled Campaign"))
        # Optionally add domains, industry, threat_types from minimal file
        if "domains" in data:
            for domain in data["domains"]:
                targeting.add_domain_target(domain)
        if "industry" in data and data["industry"]:
            targeting.add_industry_target(data["industry"])
        if "threat_types" in data and data["threat_types"]:
            targeting.set_threat_types(data["threat_types"])
        # Save enriched config to same file
        with open(args.campaign_file, 'w') as f:
            yaml.dump(asdict(targeting.current_config), f, default_flow_style=False)
        print(f"✅ Enriched campaign file: {args.campaign_file}")
