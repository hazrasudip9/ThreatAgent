#!/usr/bin/env python3
"""
ThreatAgent Targeting System Demo
=================================

This demo showcases the comprehensive threat targeting system that allows users to:
1. Create targeted threat intelligence campaigns
2. Configure company, industry, and geographic targets
3. Set threat types and priorities
4. Generate search filters for focused intelligence gathering
5. Run targeted threat intelligence workflows
"""

import os
import sys
import time
from pathlib import Path
from datetime import datetime

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent / "src"))

print("🎯 ThreatAgent Targeting System Demo")
print("=" * 50)
print(f"📅 Demo started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 50)

def demo_targeting_configuration():
    """Demonstrate various targeting configurations"""
    print("\n🎯 DEMO 1: Targeting System Configuration")
    print("=" * 50)
    
    try:
        from threatcrew.config.threat_targeting import get_targeting_system, ThreatIntelligenceConfig
        
        # Get the targeting system
        targeting_system = get_targeting_system()
        
        # Demo 1: Financial Services Campaign
        print("\n📊 Creating Financial Services Campaign...")
        config = targeting_system.create_campaign(
            campaign_name="Financial Services Phishing Campaign",
            description="Monitor for phishing attacks targeting major financial institutions"
        )
        print(f"✅ Created campaign: {config.campaign_name}")
        
        # Add company targets
        print("\n🏢 Adding company targets...")
        companies = ["JPMorgan Chase", "Bank of America", "Wells Fargo", "Citibank"]
        for company in companies:
            targeting_system.add_company_target(company, priority=4)
            print(f"   • Added target: {company}")
        
        # Add industry target
        print("\n🏭 Adding industry target...")
        targeting_system.add_industry_target("financial_services", priority=5)
        print("   • Added industry: Financial Services")
        
        # Add domain targets
        print("\n🌐 Adding domain targets...")
        domains = ["jpmorgan.com", "bankofamerica.com", "wellsfargo.com"]
        for domain in domains:
            targeting_system.add_domain_target(domain, priority=3)
            print(f"   • Added domain: {domain}")
        
        # Set threat types
        print("\n⚠️  Setting threat types...")
        threat_types = ["phishing", "credential_harvesting", "business_email_compromise"]
        targeting_system.set_threat_types(threat_types)
        print(f"   • Configured {len(threat_types)} threat types")
        
        # Set geographic focus
        print("\n🌍 Setting geographic focus...")
        regions = ["United States", "Canada", "United Kingdom"]
        targeting_system.set_geographic_focus(regions)
        print(f"   • Configured {len(regions)} geographic regions")
        
        # Generate search filters
        print("\n🔍 Generating search filters...")
        search_filters = targeting_system.generate_search_filters()
        
        print("✅ Generated search filters:")
        print(f"   • Keywords: {len(search_filters.get('keywords', []))} terms")
        print(f"   • Domains: {len(search_filters.get('domains', []))} patterns")
        print(f"   • Threat indicators: {len(search_filters.get('threat_types', []))} patterns")
        
        return config
        
    except Exception as e:
        print(f"❌ Error in targeting configuration: {e}")
        return None

def demo_industry_profiles():
    """Demonstrate predefined industry profiles"""
    print("\n🏭 DEMO 2: Industry Profile Demonstration")
    print("=" * 50)
    
    try:
        from threatcrew.config.threat_targeting import get_targeting_system
        
        targeting_system = get_targeting_system()
        
        # Demo different industry profiles
        industries = [
            ("healthcare", "Healthcare Ransomware Campaign"),
            ("technology", "Tech Company APT Campaign"),
            ("government", "Government Sector Monitoring"),
            ("energy", "Critical Infrastructure Protection")
        ]
        
        for industry_key, campaign_name in industries:
            print(f"\n🎯 Creating {industry_key.title()} Campaign...")
            
            config = targeting_system.create_campaign(
                campaign_name=campaign_name,
                description=f"Threat intelligence campaign focused on {industry_key} sector"
            )
            
            # Add industry target (this will use predefined profile)
            targeting_system.add_industry_target(industry_key, priority=5)
            
            # Get search filters from the current config
            search_filters = config.generate_search_filters()
            
            print(f"   ✅ Campaign created: {config.campaign_name}")
            print(f"   📊 Keywords: {len(search_filters['keywords'])} terms")
            print(f"   🌐 Domain patterns: {len(search_filters['domains'])} patterns")
            print(f"   ⚠️  Threat indicators: {len(search_filters['threat_indicators'])} patterns")
            
            # Show some example keywords
            if search_filters['keywords']:
                print(f"   🔍 Sample keywords: {', '.join(search_filters['keywords'][:5])}")
            
    except Exception as e:
        print(f"❌ Error in industry profiles demo: {e}")

def demo_targeted_workflow():
    """Demonstrate running threat intelligence workflow with targeting and explicit agent checks"""
    print("\n🚀 DEMO 3: Targeted Threat Intelligence Workflow (with Agent Checks)")
    print("=" * 50)
    try:
        from threatcrew.config.threat_targeting import get_targeting_system
        from threatcrew.main import run

        targeting_system = get_targeting_system()

        # Create a focused campaign
        print("\n🎯 [Recon Specialist] Creating targeted campaign and collecting OSINT...")
        targeting_config = targeting_system.create_campaign(
            campaign_name="Demo Healthcare Phishing Campaign",
            description="Demonstration of targeted threat intelligence gathering"
        )
        targeting_system.add_company_target("Kaiser Permanente", priority=5)
        targeting_system.add_company_target("Anthem Inc", priority=4)
        targeting_system.add_industry_target("healthcare", priority=5)
        targeting_system.add_url_target("https://fake-kaiser-login.com", priority=5)
        targeting_system.set_threat_types(["phishing", "ransomware", "data_breach"])
        targeting_system.set_geographic_focus(["United States"])
        print(f"✅ [Recon Specialist] Campaign configured: {targeting_config.campaign_name}")
        print(f"   Targets: {len(targeting_config.targets)} | Threat types: {len(targeting_config.threat_types)}")

        # Run the threat intelligence workflow with targeting
        print("\n🤖 [Threat Analyst] Running targeted threat intelligence workflow...")
        start_time = time.time()
        result = run(targeting_config=targeting_config)
        execution_time = time.time() - start_time
        print(f"✅ [Threat Analyst] Workflow completed in {execution_time:.2f} seconds")
        print(f"   Status: {result.get('status', 'unknown')}")

        # Explicit check: Did the analyst produce classified IOCs?
        classified_iocs = result.get('classified_iocs', [])
        if classified_iocs:
            print(f"   [CHECK] Threat Analyst classified {len(classified_iocs)} IOCs.")
        else:
            print(f"   [CHECK] No classified IOCs found! (Check Threat Analyst logic)")

        # Explicit check: Did the exporter generate a report?
        report = result.get('report', None)
        print("\n📝 [Intel Exporter] Generating threat intelligence report...")
        if report:
            print("   [CHECK] Intel Exporter produced a report. (First 10 lines):")
            for line in report.splitlines()[:10]:
                print(f"      {line}")
        else:
            print("   [CHECK] No report found! (Check Intel Exporter logic)")

        # Summary of agent contributions
        print("\n=== Agent Workflow Summary ===")
        print("[Recon Specialist] - OSINT/target collection: SUCCESS")
        print(f"[Threat Analyst]   - IOC classification: {'SUCCESS' if classified_iocs else 'FAIL'}")
        print(f"[Intel Exporter]   - Report generation: {'SUCCESS' if report else 'FAIL'}")
        print("=============================")
        return result
    except Exception as e:
        print(f"❌ Error in targeted workflow demo: {e}")
        import traceback
        traceback.print_exc()
        return None

def demo_campaign_management():
    """Demonstrate campaign management features"""
    print("\n📋 DEMO 4: Campaign Management")
    print("=" * 50)
    
    try:
        from threatcrew.config.threat_targeting import get_targeting_system
        
        targeting_system = get_targeting_system()
        
        # List all campaigns
        print("\n📊 Current campaigns:")
        campaigns = targeting_system.list_campaigns()
        
        if campaigns:
            for campaign_id, info in campaigns.items():
                print(f"   🎯 {campaign_id}: {info.get('name', 'Unknown')}")
                print(f"      📅 Created: {info.get('created_date', 'Unknown')}")
                print(f"      📊 Priority: {info.get('priority', 'Unknown')}")
                print(f"      🎯 Targets: {info.get('target_count', 0)}")
        else:
            print("   📝 No campaigns found")
        
        # Show campaign statistics
        print("\n📈 Campaign Statistics:")
        for campaign_id in campaigns.keys():
            try:
                config = targeting_system.get_campaign_config(campaign_id)
                summary = targeting_system.get_campaign_summary(campaign_id)
                
                print(f"\n🎯 Campaign: {config.campaign_name}")
                print(f"   📊 Total targets: {summary.get('total_targets', 0)}")
                print(f"   🏢 Companies: {summary.get('company_targets', 0)}")
                print(f"   🏭 Industries: {summary.get('industry_targets', 0)}")
                print(f"   🌐 Domains: {summary.get('domain_targets', 0)}")
                print(f"   🔗 URLs: {summary.get('url_targets', 0)}")
                print(f"   ⚠️  Threat types: {len(config.threat_types)}")
                print(f"   🌍 Geographic focus: {len(config.geographic_focus)}")
                
            except Exception as e:
                print(f"   ❌ Error getting summary for {campaign_id}: {e}")
        
    except Exception as e:
        print(f"❌ Error in campaign management demo: {e}")

def demo_export_import():
    """Demonstrate campaign export/import functionality"""
    print("\n💾 DEMO 5: Campaign Export/Import")
    print("=" * 50)
    
    try:
        from threatcrew.config.threat_targeting import get_targeting_system
        import tempfile
        
        targeting_system = get_targeting_system()
        
        # Get a campaign to export
        campaigns = targeting_system.list_campaigns()
        if not campaigns:
            print("📝 No campaigns available for export demo")
            return
        
        campaign_id = list(campaigns.keys())[0]
        config = targeting_system.get_campaign_config(campaign_id)
        
        print(f"📤 Exporting campaign: {config.campaign_name}")
        
        # Export to temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            export_path = f.name
        
        targeting_system.export_campaign(campaign_id, export_path)
        print(f"✅ Exported to: {export_path}")
        
        # Show file contents
        print("\n📄 Export file contents (first 20 lines):")
        try:
            with open(export_path, 'r') as f:
                lines = f.readlines()
                for i, line in enumerate(lines[:20], 1):
                    print(f"   {i:2d}: {line.rstrip()}")
                if len(lines) > 20:
                    print(f"   ... ({len(lines) - 20} more lines)")
        except Exception as e:
            print(f"   ❌ Error reading export file: {e}")
        
        # Clean up
        try:
            os.unlink(export_path)
            print(f"🗑️  Cleaned up temporary file")
        except:
            pass
        
    except Exception as e:
        print(f"❌ Error in export/import demo: {e}")

def main():
    """Run all demonstrations"""
    try:
        print("🚀 Starting ThreatAgent Targeting System Demo")
        print("   This demo showcases the comprehensive targeting capabilities")
        print("   for focused threat intelligence gathering.\n")
        
        # Run all demos
        demos = [
            demo_targeting_configuration,
            demo_industry_profiles,
            demo_campaign_management,
            demo_export_import,
            demo_targeted_workflow  # Run this last as it's most resource intensive
        ]
        
        for i, demo_func in enumerate(demos, 1):
            print(f"\n{'='*60}")
            print(f"Running Demo {i}/{len(demos)}: {demo_func.__name__}")
            print(f"{'='*60}")
            
            try:
                demo_func()
                print(f"\n✅ Demo {i} completed successfully!")
            except Exception as e:
                print(f"\n❌ Demo {i} failed: {e}")
                import traceback
                traceback.print_exc()
            
            # Small delay between demos
            if i < len(demos):
                time.sleep(2)
        
        print(f"\n{'='*60}")
        print("🎉 ThreatAgent Targeting System Demo Completed!")
        print(f"📅 Demo finished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}")
        
    except Exception as e:
        print(f"\n💥 Fatal error in demo: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
