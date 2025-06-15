#!/usr/bin/env python3
"""
Quick Threat Feed Ingestion Demo
===============================

This script demonstrates how to quickly set up and run threat feed ingestion
using ThreatAgent's Level 1 ingestion system.

Usage:
    python quick_ingestion_demo.py
"""

import asyncio
import json
import logging
import sys
import os
from datetime import datetime

# Add threatcrew to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'threatcrew', 'src'))

from threatcrew.managers.threat_feed_manager import get_threat_feed_manager

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def add_popular_feeds(tfm):
    """Add popular public threat intelligence feeds."""
    
    logger.info("🔧 Adding popular threat intelligence feeds...")
    
    # ThreatFox (Abuse.ch) - High quality IOCs
    tfm.add_custom_feed(
        name="ThreatFox Recent IOCs",
        url="https://threatfox.abuse.ch/export/json/recent/",
        feed_type="json",
        update_interval=30  # 30 minutes
    )
    
    # URLhaus (Abuse.ch) - Malicious URLs
    tfm.add_custom_feed(
        name="URLhaus Recent URLs",
        url="https://urlhaus.abuse.ch/downloads/json/",
        feed_type="json", 
        update_interval=30  # 30 minutes
    )
    
    # Bambenek C2 Domains - Command & Control domains
    tfm.add_custom_feed(
        name="Bambenek C2 Domains",
        url="http://osint.bambenekconsulting.com/feeds/c2-dommasterlist.txt",
        feed_type="text",
        update_interval=120  # 2 hours
    )
    
    # FireHOL Level 1 - Malicious IPs
    tfm.add_custom_feed(
        name="FireHOL Level 1",
        url="https://iplists.firehol.org/files/firehol_level1.netset",
        feed_type="text",
        update_interval=60  # 1 hour
    )
    
    logger.info("✅ Added 4 high-quality threat intelligence feeds")

def print_feed_status(tfm):
    """Print status of all configured feeds."""
    stats = tfm.get_feed_stats()
    
    print("\n" + "="*60)
    print("🔍 THREAT FEED STATUS")
    print("="*60)
    print(f"Total Feeds: {stats['total_feeds']}")
    print(f"Active Feeds: {stats['active_feeds']}")
    print()
    
    for feed_info in stats['feeds']:
        status = "🟢 ACTIVE" if feed_info['active'] else "🔴 INACTIVE"
        last_update = feed_info['last_updated'] or "Never"
        if last_update != "Never":
            # Parse ISO format and make it readable
            dt = datetime.fromisoformat(last_update.replace('Z', '+00:00'))
            last_update = dt.strftime("%Y-%m-%d %H:%M:%S")
        
        print(f"📡 {feed_info['name']}")
        print(f"   Status: {status}")
        print(f"   Last Update: {last_update}")
        print(f"   Interval: {feed_info['update_interval']} minutes")
        print()

async def demo_single_feed_processing(tfm):
    """Demonstrate processing a single feed manually."""
    logger.info("🔬 Demonstrating single feed processing...")
    
    # Find a feed to process
    active_feeds = [f for f in tfm.feeds if f.active]
    if not active_feeds:
        logger.warning("No active feeds available for demo")
        return
    
    demo_feed = active_feeds[0]
    logger.info(f"Processing feed: {demo_feed.name}")
    
    try:
        await tfm._process_feed(demo_feed)
        logger.info(f"✅ Successfully processed {demo_feed.name}")
    except Exception as e:
        logger.error(f"❌ Error processing {demo_feed.name}: {e}")

async def run_limited_monitoring(tfm, duration_minutes=2):
    """Run threat feed monitoring for a limited time (demo purposes)."""
    logger.info(f"🚀 Starting threat feed monitoring for {duration_minutes} minutes...")
    logger.info("📊 This will collect and classify IOCs from configured feeds")
    logger.info("⏱️  In production, this would run continuously")
    
    # Start monitoring task
    monitoring_task = asyncio.create_task(tfm.start_feed_monitoring())
    
    try:
        # Wait for specified duration
        await asyncio.wait_for(monitoring_task, timeout=duration_minutes * 60)
    except asyncio.TimeoutError:
        logger.info(f"⏹️  Demo completed after {duration_minutes} minutes")
        tfm.running = False
        monitoring_task.cancel()
        
        try:
            await monitoring_task
        except asyncio.CancelledError:
            pass

def print_usage_instructions():
    """Print usage instructions for users."""
    print("\n" + "="*60)
    print("📚 NEXT STEPS")
    print("="*60)
    print("1. For full documentation, see: LEVEL_1_INGESTION_GUIDE.md")
    print("2. To add API-based feeds, you'll need API keys:")
    print("   - AlienVault OTX: Get free API key at otx.alienvault.com")
    print("   - VirusTotal: Get API key at virustotal.com")
    print("   - MISP: Contact your MISP instance administrator")
    print()
    print("3. For continuous production monitoring:")
    print("   tfm = get_threat_feed_manager()")
    print("   await tfm.start_feed_monitoring()  # Runs indefinitely")
    print()
    print("4. To check memory database for collected IOCs:")
    print("   from threatcrew.tools.memory_system import get_memory")
    print("   memory = get_memory()")
    print("   iocs = memory.search_iocs('domain')")
    print("="*60)

async def main():
    """Main demonstration function."""
    print("🕵️ ThreatAgent - Level 1 Threat Feed Ingestion Demo")
    print("="*60)
    print("This demo shows how to set up and run automated threat intelligence")
    print("collection from public feeds using ThreatAgent's ingestion system.")
    print()
    
    # Initialize ThreatFeedManager
    logger.info("🚀 Initializing ThreatFeedManager...")
    tfm = get_threat_feed_manager()
    
    # Add popular public feeds
    add_popular_feeds(tfm)
    
    # Show feed status
    print_feed_status(tfm)
    
    # Demo single feed processing
    await demo_single_feed_processing(tfm)
    
    # Ask user if they want to run limited monitoring
    try:
        response = input("Run 2-minute live monitoring demo? (y/n): ").strip().lower()
        if response in ['y', 'yes']:
            await run_limited_monitoring(tfm, duration_minutes=2)
        else:
            logger.info("Skipping live monitoring demo")
    except KeyboardInterrupt:
        logger.info("\n👋 Demo interrupted by user")
    
    # Print usage instructions
    print_usage_instructions()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Demo stopped by user")
    except Exception as e:
        logger.error(f"❌ Demo failed: {e}")
        sys.exit(1)
