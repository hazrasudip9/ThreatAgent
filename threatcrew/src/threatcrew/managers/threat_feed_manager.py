"""
ThreatFeedManager
================

Manages real-time threat intelligence feeds and automated data ingestion.
Processes feeds from multiple sources and stores in memory system.
"""

import asyncio
import json
import logging
import time
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import aiohttp
import xml.etree.ElementTree as ET

from ..tools.memory_system import get_memory
from ..tools.llm_classifier import run as classify_iocs

logger = logging.getLogger(__name__)

@dataclass
class ThreatFeed:
    name: str
    url: str
    feed_type: str  # 'json', 'xml', 'csv', 'text'
    update_interval: int  # minutes
    last_updated: Optional[datetime] = None
    active: bool = True
    headers: Optional[Dict[str, str]] = None

class ThreatFeedManager:
    """
    Manages multiple threat intelligence feeds and processes them automatically.
    """
    
    def __init__(self):
        self.memory = get_memory()
        self.feeds = self._initialize_default_feeds()
        self.session_id = f"feed_manager_{int(time.time())}"
        self.running = False
    
    def _initialize_default_feeds(self) -> List[ThreatFeed]:
        """Initialize default threat intelligence feeds."""
        return [
            ThreatFeed(
                name="VirusTotal Intelligence",
                url="https://www.virustotal.com/api/v3/intelligence/hunting_notification_files",
                feed_type="json",
                update_interval=60,  # 1 hour
                headers={"x-apikey": "YOUR_VT_API_KEY"}
            ),
            ThreatFeed(
                name="PhishTank",
                url="http://data.phishtank.com/data/online-valid.xml",
                feed_type="xml",
                update_interval=30,  # 30 minutes
            ),
            ThreatFeed(
                name="Malware Domain List",
                url="https://www.malwaredomainlist.com/hostslist/hosts.txt",
                feed_type="text",
                update_interval=60,  # 1 hour
            ),
            ThreatFeed(
                name="Abuse.ch URLhaus",
                url="https://urlhaus.abuse.ch/downloads/json/",
                feed_type="json",
                update_interval=30,  # 30 minutes
            ),
            ThreatFeed(
                name="MISP Feed",
                url="https://misp.example.com/events/restSearch",
                feed_type="json",
                update_interval=120,  # 2 hours
                headers={"Authorization": "Bearer YOUR_MISP_TOKEN"}
            ),
        ]
    
    async def start_feed_monitoring(self):
        """Start monitoring all active threat feeds."""
        self.running = True
        logger.info("🚀 Starting threat feed monitoring...")
        
        tasks = []
        for feed in self.feeds:
            if feed.active:
                task = asyncio.create_task(self._monitor_feed(feed))
                tasks.append(task)
        
        try:
            await asyncio.gather(*tasks)
        except KeyboardInterrupt:
            logger.info("⏹️  Stopping threat feed monitoring...")
            self.running = False
    
    async def _monitor_feed(self, feed: ThreatFeed):
        """Monitor a single threat feed."""
        while self.running:
            try:
                if self._should_update_feed(feed):
                    logger.info(f"📡 Updating feed: {feed.name}")
                    await self._process_feed(feed)
                    feed.last_updated = datetime.now()
                
                # Wait for next update interval
                await asyncio.sleep(feed.update_interval * 60)
                
            except Exception as e:
                logger.error(f"❌ Error processing feed {feed.name}: {e}")
                # Wait before retrying
                await asyncio.sleep(60)
    
    def _should_update_feed(self, feed: ThreatFeed) -> bool:
        """Check if a feed should be updated."""
        if feed.last_updated is None:
            return True
        
        time_since_update = datetime.now() - feed.last_updated
        return time_since_update >= timedelta(minutes=feed.update_interval)
    
    async def _process_feed(self, feed: ThreatFeed):
        """Process a single threat feed and extract IOCs."""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(feed.url, headers=feed.headers) as response:
                    if response.status == 200:
                        content = await response.text()
                        iocs = self._extract_iocs_from_content(content, feed)
                        await self._process_extracted_iocs(iocs, feed.name)
                    else:
                        logger.warning(f"⚠️  Feed {feed.name} returned status {response.status}")
        
        except Exception as e:
            logger.error(f"❌ Failed to process feed {feed.name}: {e}")
    
    def _extract_iocs_from_content(self, content: str, feed: ThreatFeed) -> List[Dict[str, Any]]:
        """Extract IOCs from feed content based on feed type."""
        iocs = []
        
        try:
            if feed.feed_type == "json":
                iocs = self._extract_from_json(content, feed)
            elif feed.feed_type == "xml":
                iocs = self._extract_from_xml(content, feed)
            elif feed.feed_type == "text":
                iocs = self._extract_from_text(content, feed)
            elif feed.feed_type == "csv":
                iocs = self._extract_from_csv(content, feed)
        
        except Exception as e:
            logger.error(f"❌ Failed to extract IOCs from {feed.name}: {e}")
        
        return iocs
    
    def _extract_from_json(self, content: str, feed: ThreatFeed) -> List[Dict[str, Any]]:
        """Extract IOCs from JSON feed."""
        iocs = []
        data = json.loads(content)
        
        if feed.name == "Abuse.ch URLhaus":
            for item in data.get("urlhaus", []):
                if item.get("url_status") == "online":
                    iocs.append({
                        "ioc": item.get("url"),
                        "ioc_type": "url",
                        "source": feed.name,
                        "threat_type": item.get("threat", "unknown"),
                        "tags": item.get("tags", [])
                    })
        
        elif feed.name == "MISP Feed":
            for event in data.get("response", {}).get("Event", []):
                for attribute in event.get("Attribute", []):
                    if attribute.get("to_ids") and not attribute.get("deleted"):
                        iocs.append({
                            "ioc": attribute.get("value"),
                            "ioc_type": attribute.get("type"),
                            "source": feed.name,
                            "category": attribute.get("category"),
                            "comment": attribute.get("comment")
                        })
        
        return iocs
    
    def _extract_from_xml(self, content: str, feed: ThreatFeed) -> List[Dict[str, Any]]:
        """Extract IOCs from XML feed."""
        iocs = []
        
        if feed.name == "PhishTank":
            root = ET.fromstring(content)
            for entry in root.findall(".//entry"):
                url = entry.find("url")
                if url is not None:
                    iocs.append({
                        "ioc": url.text,
                        "ioc_type": "url",
                        "source": feed.name,
                        "threat_type": "phishing"
                    })
        
        return iocs
    
    def _extract_from_text(self, content: str, feed: ThreatFeed) -> List[Dict[str, Any]]:
        """Extract IOCs from text feed."""
        iocs = []
        
        if feed.name == "Malware Domain List":
            lines = content.split('\n')
            for line in lines:
                line = line.strip()
                if line and not line.startswith('#'):
                    # Format: 127.0.0.1 malicious.domain.com
                    parts = line.split()
                    if len(parts) >= 2 and parts[0] == "127.0.0.1":
                        domain = parts[1]
                        iocs.append({
                            "ioc": domain,
                            "ioc_type": "domain",
                            "source": feed.name,
                            "threat_type": "malware"
                        })
        
        return iocs
    
    def _extract_from_csv(self, content: str, feed: ThreatFeed) -> List[Dict[str, Any]]:
        """Extract IOCs from CSV feed."""
        # Implement CSV parsing logic based on feed format
        return []
    
    async def _process_extracted_iocs(self, iocs: List[Dict[str, Any]], source: str):
        """Process extracted IOCs through classification and storage."""
        logger.info(f"📊 Processing {len(iocs)} IOCs from {source}")
        
        for ioc_data in iocs:
            try:
                # Classify the IOC using the LLM classifier
                classification_result = classify_iocs(ioc_data["ioc"])
                
                # Store in memory system
                ioc_id = self.memory.store_ioc(
                    ioc=ioc_data["ioc"],
                    ioc_type=ioc_data["ioc_type"],
                    risk_level=classification_result.get("risk_level", "UNKNOWN"),
                    category=classification_result.get("category", "unknown"),
                    confidence=classification_result.get("confidence", 0.5),
                    source=source,
                    metadata={
                        "feed_source": source,
                        "original_data": ioc_data,
                        "auto_classified": True,
                        "classification_result": classification_result
                    }
                )
                
                # Store analysis history
                self.memory.store_analysis(
                    session_id=self.session_id,
                    analysis_type="feed_processing",
                    input_data=ioc_data,
                    output_data=classification_result,
                    confidence=classification_result.get("confidence", 0.5)
                )
                
            except Exception as e:
                logger.error(f"❌ Failed to process IOC {ioc_data.get('ioc')}: {e}")
    
    def add_custom_feed(self, name: str, url: str, feed_type: str, 
                       update_interval: int, headers: Dict[str, str] = None):
        """Add a custom threat feed."""
        feed = ThreatFeed(
            name=name,
            url=url,
            feed_type=feed_type,
            update_interval=update_interval,
            headers=headers
        )
        self.feeds.append(feed)
        logger.info(f"➕ Added custom feed: {name}")
    
    def get_feed_stats(self) -> Dict[str, Any]:
        """Get statistics about threat feeds."""
        stats = {
            "total_feeds": len(self.feeds),
            "active_feeds": len([f for f in self.feeds if f.active]),
            "feeds": []
        }
        
        for feed in self.feeds:
            feed_stats = {
                "name": feed.name,
                "active": feed.active,
                "last_updated": feed.last_updated.isoformat() if feed.last_updated else None,
                "update_interval": feed.update_interval
            }
            stats["feeds"].append(feed_stats)
        
        return stats

# Global threat feed manager instance
_threat_feed_manager = None

def get_threat_feed_manager() -> ThreatFeedManager:
    """Get the global threat feed manager instance."""
    global _threat_feed_manager
    if _threat_feed_manager is None:
        _threat_feed_manager = ThreatFeedManager()
    return _threat_feed_manager
