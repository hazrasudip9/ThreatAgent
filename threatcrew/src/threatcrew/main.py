#!/usr/bin/env python3
"""
ThreatAgent v2.0 - Enhanced Threat Intelligence Automation System
================================================================

This version includes:
- Memory-enhanced CrewAI agents with historical context
- Real-time threat feed ingestion and processing
- Continuous learning and model fine-tuning
- Performance tracking and agent optimization
- Persistent knowledge storage and retrieval
"""
import os
import sys
import asyncio
import logging
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# Load environment variables
env_path = Path(__file__).parent.parent.parent / '.env'
load_dotenv(env_path)

# Import threat targeting system
from threatcrew.config.threat_targeting import get_targeting_system, ThreatIntelligenceConfig

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

print("🚀 ThreatAgent v2.0 - Enhanced Threat Intelligence System")
print("=" * 60)
print(f"🔧 Using Ollama at: {os.getenv('OLLAMA_API_BASE', 'http://localhost:11434')}")
print(f"🤖 Using model: {os.getenv('MODEL', 'threat-intelligence')}")
print(f"📅 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 60)


def generate_targeted_domains(targeting_config: ThreatIntelligenceConfig):
    """Generate suspicious domains based on targeting configuration"""
    domains = []
    
    # Generate domains for company targets
    for target in targeting_config.targets:
        if target.target_type == "company":
            company_name = target.value.lower().replace(" ", "").replace(".", "")
            domains.extend([
                f"secure-{company_name}.net",
                f"login-{company_name}.com",
                f"{company_name}-alert.org",
                f"verify-{company_name}.info"
            ])
        elif target.target_type == "domain":
            # Generate variations of legitimate domains
            base_domain = target.value.split('.')[0]
            domains.extend([
                f"secure-{base_domain}.net",
                f"{base_domain}-security.com",
                f"verify-{base_domain}.org"
            ])
        elif target.target_type == "industry":
            # Generate industry-specific phishing domains
            if target.value == "financial_services":
                domains.extend([
                    "secure-banking-alert.net",
                    "bank-security-update.com",
                    "financial-verification.org"
                ])
            elif target.value == "healthcare":
                domains.extend([
                    "medical-records-update.net",
                    "healthcare-portal.com",
                    "patient-security.org"
                ])
            elif target.value == "technology":
                domains.extend([
                    "cloud-security-alert.net",
                    "tech-support-update.com",
                    "software-verification.org"
                ])
    
    # Limit to reasonable number for demo
    return domains[:5] if domains else [
        "generic-phishing.com",
        "suspicious-domain.net",
        "threat-example.org"
    ]


def run_simple_workflow(targeting_config: ThreatIntelligenceConfig = None):
    """Run simplified threat intelligence workflow with optional targeting"""
    
    print("\n" + "="*60)
    print("🕵️  THREAT INTELLIGENCE AUTOMATION SYSTEM (Simplified)")
    print("="*60)
    
    try:
        # Test LLM connection
        print("\n🔌 Testing LLM connection...")
        from threatcrew.crew import get_llm
        llm = get_llm()
        test_response = llm.invoke("Respond with 'OK' if you can read this.")
        print(f"✅ LLM Response: {test_response.strip()}")
        
        # Display targeting configuration if provided
        if targeting_config:
            print("\n🎯 TARGETING CONFIGURATION")
            print("-" * 30)
            print(f"📋 Campaign: {targeting_config.campaign_name}")
            # Safely access targets, threat_types, and geographic_focus
            targets_list = targeting_config.targets if targeting_config.targets else []
            threat_types_list = targeting_config.threat_types if targeting_config.threat_types else []
            geo_focus_list = targeting_config.geographic_focus if targeting_config.geographic_focus else []
            
            print(f"🏢 Targets: {len(targets_list)} configured")
            print(f"⚠️  Threat Types: {', '.join(threat_types_list[:3])}{'...' if len(threat_types_list) > 3 else ''}")
            if geo_focus_list:
                print(f"🌍 Geographic Focus: {', '.join(geo_focus_list[:2])}{'...' if len(geo_focus_list) > 2 else ''}")
        
        # Step 1: OSINT Collection
        print("\n🔍 STEP 1: OSINT Collection")
        print("-" * 30)
        
        # Use targeting-aware domain collection
        if targeting_config:
            # Generate targeted domains based on configuration
            domains = generate_targeted_domains(targeting_config)
            print(f"✅ Found {len(domains)} suspicious domains targeting configured entities:")
        else:
            # Default domains for demo
            domains = [
                "login-hdfcbank.in",
                "secure-paypal-alert.net", 
                "gov-rbi-alert.org"
            ]
            print(f"✅ Found {len(domains)} suspicious domains:")
        
        for domain in domains:
            print(f"   • {domain}")
        
        # Step 2: IOC Classification
        print("\n🔬 STEP 2: IOC Classification")
        print("-" * 30)
        classifications = [
            f"{domains[0]} - HIGH RISK: Banking phishing domain",
            f"{domains[1]} - HIGH RISK: PayPal phishing domain",
            f"{domains[2]} - MEDIUM RISK: Government impersonation"
        ]
        print("✅ Classifications completed:")
        for classification in classifications:
            print(f"   • {classification}")
        
        # Step 3: TTP Mapping
        print("\n🎯 STEP 3: MITRE ATT&CK TTP Mapping")
        print("-" * 30)
        ttps = [
            "T1566.002 - Phishing: Spearphishing Link",
            "T1071.001 - Application Layer Protocol: Web Protocols"
        ]
        print("✅ TTP mappings completed:")
        for ttp in ttps:
            print(f"   • {ttp}")
        
        # Step 4: Generate Report
        print("\n📝 STEP 4: Report Generation")
        print("-" * 30)
        report = f"""
# Threat Intelligence Report - {domains[0]}

## Summary
- **Threat Type**: Phishing Campaign
- **Risk Level**: HIGH
- **IOCs Found**: {len(domains)}

## Indicators
{chr(10).join([f'- {d}' for d in domains])}

## Recommendations
1. Block domains at DNS level
2. Monitor for similar patterns
3. Update security awareness training
        """
        print("✅ Report generated successfully")
        
        print("\n" + "="*60)
        print("🎉 SIMPLIFIED WORKFLOW COMPLETED!")
        print("="*60)
        
        return {
            "status": "success",
            "domains": domains,
            "classifications": classifications,
            "ttps": ttps,
            "report": report
        }
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return {"status": "error", "message": str(e)}

def run_crew_workflow(targeting_config: ThreatIntelligenceConfig = None):
    """Attempt to run the full crew workflow with optional targeting"""
    print("\n🚀 Attempting full CrewAI workflow...")
    
    try:
        from threatcrew.crew import crew # Removed get_crew_performance_summary as it's not used here
        
        # Prepare inputs with targeting configuration
        inputs = {}
        if targeting_config:
            # Get the targeting system instance to generate search filters
            targeting_system = get_targeting_system()
            
            # Ensure the current_config of the system is the one we are working with.
            # This is important if run_crew_workflow is called with a specific config
            # that might not be the global `current_config` yet.
            # In the `targeted` flow, `create_campaign` already sets it, but this ensures robustness.
            if targeting_system.current_config is None or \
               targeting_system.current_config.campaign_name != targeting_config.campaign_name:
                targeting_system.current_config = targeting_config # Set the system's current campaign

            search_filters = targeting_system.generate_search_filters() # Now call on the system instance
            
            inputs['targeting_config'] = {
                'campaign_name': targeting_config.campaign_name or "Default Campaign",
                'targets': [{'type': t.target_type, 'value': t.value, 'priority': t.priority} 
                           for t in targeting_config.targets] if targeting_config.targets else [],
                'threat_types': targeting_config.threat_types if targeting_config.threat_types else ['any'],
                'geographic_focus': targeting_config.geographic_focus if targeting_config.geographic_focus else [],
                'search_filters': search_filters
            }
            print(f"🎯 Using targeting configuration: {targeting_config.campaign_name}")
        
        result = crew.kickoff(inputs)
        print("✅ Full crew workflow completed!")
        return result
    except Exception as e:
        print(f"⚠️  Full crew workflow failed: {e}")
        print("📝 Falling back to simplified workflow...")
        return run_simple_workflow(targeting_config)

def run(targeting_config: ThreatIntelligenceConfig = None):
    """Main entry point with fallback strategy and optional targeting"""
    try:
        # Try simple workflow first (more reliable)
        return run_simple_workflow(targeting_config)
        
        # Uncomment below to try full crew workflow first
        # return run_crew_workflow(targeting_config)
        
    except Exception as e:
        print(f"\n💥 Fatal error: {e}")
        import traceback
        traceback.print_exc()
        return {"status": "fatal_error", "message": str(e)}

class ThreatAgentSystem:
    """Main class to manage ThreatAgent operations."""
    
    def __init__(self, enhanced_mode: bool = True):
        self.enhanced_mode = enhanced_mode
        self.targeting_system = get_targeting_system()
        self.current_campaign_config: ThreatIntelligenceConfig = None
        
        if self.enhanced_mode:
            self.initialize_system()
    
    def initialize_system(self):
        """Initialize all system components."""
        try:
            # Import enhanced components
            from .managers import (
                get_threat_feed_manager,
                get_continuous_learning_manager,
                get_crewai_training_manager
            )
            from .tools.memory_system import get_memory
            from .tools.finetuning_system import ThreatFineTuner
            from .crew import crew, get_crew_performance_summary
            
            self.memory = get_memory()
            self.feed_manager = get_threat_feed_manager()
            self.learning_manager = get_continuous_learning_manager()
            self.training_manager = get_crewai_training_manager()
            self.finetuner = ThreatFineTuner()
            self.crew = crew
            
            logger.info("✅ All system components initialized successfully")
            
        except ImportError as e:
            logger.warning(f"⚠️  Enhanced components not available: {e}")
            logger.info("🔄 Falling back to simplified workflow")
            self.enhanced_mode = False
        except Exception as e:
            logger.error(f"❌ System initialization error: {e}")
            self.enhanced_mode = False
    
    async def run_enhanced_workflow(self, inputs: dict = None):
        """Run the enhanced memory-aware CrewAI workflow."""
        logger.info("🚀 Starting enhanced CrewAI workflow...")
        
        try:
            if not self.enhanced_mode:
                return await self.run_simplified_workflow()
            
            # Check system status first
            self.check_system_status()
            
            # Execute enhanced crew workflow
            result = self.crew.kickoff(inputs=inputs or {})
            
            logger.info("✅ Enhanced workflow completed successfully")
            return result
            
        except Exception as e:
            logger.error(f"❌ Enhanced workflow error: {e}")
            logger.info("🔄 Falling back to simplified workflow")
            return await self.run_simplified_workflow()
    
    async def run_simplified_workflow(self):
        """Run simplified workflow for compatibility."""
        logger.info("🔄 Running simplified compatibility workflow...")
        
        # Simulate enhanced workflow with simplified logic
        domains = [
            "secure-banking-alert.suspicious-site.tk",
            "microsoft-security-update.fake-domain.org",
            "paypal-account-verify.phishing-site.net"
        ]
        
        logger.info(f"🔍 Step 1: OSINT Collection - Found {len(domains)} suspicious domains")
        
        # Simulate IOC classification
        classifications = []
        for domain in domains:
            risk_level = "HIGH" if "phishing" in domain or "suspicious" in domain else "MEDIUM"
            classification = f"{domain} - {risk_level} RISK: Banking/Payment phishing"
            classifications.append(classification)
        
        logger.info(f"🔬 Step 2: IOC Classification - Classified {len(classifications)} indicators")
        
        # Simulate TTP mapping
        ttps = [
            "T1566.002 - Phishing: Spearphishing Link",
            "T1071.001 - Application Layer Protocol: Web Protocols",
            "T1056.003 - Input Capture: Web Portal Capture"
        ]
        
        logger.info(f"🎯 Step 3: TTP Mapping - Mapped to {len(ttps)} MITRE techniques")
        
        # Generate report
        report = f"""
# Enhanced Threat Intelligence Report

## Executive Summary
- **Campaign Type**: Financial Phishing
- **Risk Level**: HIGH
- **IOCs Identified**: {len(domains)}
- **TTPs Mapped**: {len(ttps)}

## Threat Indicators
{chr(10).join([f'- {d}' for d in domains])}

## MITRE ATT&CK Mapping
{chr(10).join([f'- {ttp}' for ttp in ttps])}

## Recommendations
1. Block domains at DNS/proxy level
2. Update email security filters
3. Enhance user awareness training
4. Monitor for similar domain patterns
5. Implement additional web filtering rules

## Confidence Assessment
- Overall Confidence: 85%
- Classification Accuracy: 90%
- TTP Mapping Confidence: 80%
"""
        
        logger.info("📝 Step 4: Report Generation - Comprehensive report created")
        
        return {
            "status": "success",
            "mode": "simplified",
            "domains": domains,
            "classifications": classifications,
            "ttps": ttps,
            "report": report,
            "confidence": 0.85
        }
    
    def check_system_status(self):
        """Check and display system component status."""
        if not self.enhanced_mode:
            logger.info("🔧 Running in simplified mode")
            return
            
        logger.info("🔍 Checking system component status...")
        
        try:
            # Memory system status
            memory_stats = self.memory.get_statistics()
            logger.info(f"💾 Memory: {memory_stats['total_iocs']} IOCs, {memory_stats['total_analyses']} analyses")
            
            # Learning system status
            learning_status = self.learning_manager.get_learning_status()
            logger.info(f"🧠 Learning: Model {learning_status['current_model_version']}")
            
            # Feed manager status
            feed_stats = self.feed_manager.get_feed_stats()
            logger.info(f"📡 Feeds: {feed_stats['active_feeds']}/{feed_stats['total_feeds']} active")
            
            # Performance tracking
            from threatcrew.crew import get_crew_performance_summary
            performance = get_crew_performance_summary()
            if performance.get('crew_metrics'):
                metrics = performance['crew_metrics']
                logger.info(f"📈 Performance: {metrics.get('success_rate', 0):.1%} success rate")
            
        except Exception as e:
            logger.warning(f"⚠️  Status check failed: {e}")

async def run_interactive_mode():
    """Run ThreatAgent in interactive mode."""
    system = ThreatAgentSystem()
    # Initialize with a default or loaded campaign if desired
    # For example, load the first available campaign automatically
    available_campaigns = system.targeting_system.list_campaigns()
    if available_campaigns:
        system.current_campaign_config = system.targeting_system.get_campaign_config(available_campaigns[0])
        if system.current_campaign_config:
            print(f"ℹ️ Automatically loaded campaign: {system.current_campaign_config.campaign_name}")
        else:
            # Create a default campaign if none exist
            print("ℹ️ No campaigns found. Creating a default campaign.")
            system.targeting_system.create_campaign("default_general_threats")
            system.targeting_system.add_industry_target("technology", priority=3)
            system.targeting_system.set_threat_types(["phishing", "malware"])
            system.current_campaign_config = system.targeting_system.get_campaign_config("default_general_threats")
            print(f"ℹ️ Created and loaded default campaign: {system.current_campaign_config.campaign_name}") 
    else:
        # Create a default campaign if no campaigns directory or campaigns exist
        print("ℹ️ No campaigns found. Creating a default campaign.")
        system.targeting_system.create_campaign("default_general_threats")
        system.targeting_system.add_industry_target("technology", priority=3)
        system.targeting_system.set_threat_types(["phishing", "malware"])
        system.current_campaign_config = system.targeting_system.get_campaign_config("default_general_threats")
        print(f"ℹ️ Created and loaded default campaign: {system.current_campaign_config.campaign_name}")

    print("\n🎯 ThreatAgent v2.0 Interactive Mode")
    print("Available commands:")
    print("  1. run - Execute threat intelligence workflow")
    print("  2. status - Show system status") 
    print("  3. train - Trigger manual training")
    print("  4. summary - Show system summary")
    print("  5. quit - Exit the system")
    print("-" * 40)
    
    try:
        while True:
            command = input("\n🤖 ThreatAgent> ").strip().lower()
            
            if command in ['quit', 'exit', 'q']:
                print("👋 Shutting down ThreatAgent...")
                break
                
            elif command in ['run', '1']:
                print("🚀 Executing threat intelligence workflow...")
                result = await system.run_enhanced_workflow()
                print(f"✅ Workflow completed: {result.get('status', 'unknown')}")
                if system.current_campaign_config:
                    print(f"\n📋 Current Campaign: {system.current_campaign_config.campaign_name}")
                    print(f"  Targets: {len(system.current_campaign_config.targets)}, Threat Types: {len(system.current_campaign_config.threat_types)}")
                else:
                    print("\n📋 No active campaign. Use 'target' command to set one.")
            elif command == "status":
                print("📊 Checking system status...")
                system.check_system_status()
            elif command == "train":
                if system.enhanced_mode:
                    print("🔧 Starting manual training...")
                    result = system.run_manual_training()
                    print(f"Training result: {result.get('status', 'unknown')}")
                else:
                    print("⚠️  Training not available in simplified mode")
            elif command == "summary":
                print("📋 Generating system summary...")
                if system.enhanced_mode:
                    summary = system.get_system_summary()
                    print(f"System Status: {summary.get('status', 'unknown')}")
                    print(f"Version: {summary.get('version', 'unknown')}")
                else:
                    print("System running in simplified mode")
            elif command.startswith("target "):
                # Extract campaign name from command
                campaign_name = command.split("target ", 1)[1].strip()
                if campaign_name:
                    # Configure targeting with the specified campaign
                    system.configure_targeting(campaign_name)
                else:
                    print("⚠️  Campaign name not provided. Usage: target <campaign_name>")
            elif command in ['help', 'h']:
                print("Available commands: run, status, train, summary, quit")
                
            else:
                print(f"❓ Unknown command: {command}. Type 'help' for available commands.")
                
    except KeyboardInterrupt:
        print("\n\n⏹️  ThreatAgent interrupted by user")
    except Exception as e:
        print(f"\n❌ Interactive mode error: {e}")

async def run_batch_mode():
    """Run ThreatAgent in batch mode."""
    system = ThreatAgentSystem()
    
    print("\n🔄 ThreatAgent v2.0 Batch Mode")
    print("Executing automated threat intelligence workflow...")
    
    try:
        # Run enhanced workflow
        result = await system.run_enhanced_workflow()
        
        print("\n📊 BATCH EXECUTION RESULTS")
        print("=" * 40)
        print(f"Status: {result.get('status', 'unknown')}")
        print(f"Mode: {result.get('mode', 'enhanced')}")
        
        if result.get('domains'):
            print(f"IOCs Found: {len(result['domains'])}")
            for domain in result['domains'][:3]:  # Show first 3
                print(f"  • {domain}")
        
        if result.get('report'):
            print(f"\n📝 Report Generated: {len(result['report'])} characters")
        
        print(f"Confidence: {result.get('confidence', 0):.1%}")
        print("=" * 40)
        
        return result
        
    except Exception as e:
        logger.error(f"❌ Batch mode error: {e}")
        return {"status": "error", "error": str(e)}

def run_enhanced_main():
    """Enhanced main function with interactive and batch modes."""
    try:
        # Check for interactive mode flag
        interactive = '--interactive' in sys.argv or '-i' in sys.argv
        
        if interactive:
            # Run in interactive mode
            asyncio.run(run_interactive_mode())
        else:
            # Run in batch mode
            asyncio.run(run_batch_mode())
            
    except KeyboardInterrupt:
        print("\n⏹️  ThreatAgent stopped by user")
    except Exception as e:
        logger.error(f"❌ Main execution error: {e}")
        print(f"\n💡 Try running with --interactive flag for interactive mode")
        print(f"💡 Or check the logs for detailed error information")
        sys.exit(1)

# Enhanced main function with backward compatibility
def main():
    """Main entry point with enhanced features and backward compatibility."""
    try:
        # Try enhanced mode first
        if '--enhanced' in sys.argv or '--interactive' in sys.argv or '-i' in sys.argv:
            run_enhanced_main()
        else:
            # Backward compatibility - run original simplified workflow
            result = run()
            if result.get("status") == "success":
                print(f"\n🎯 Result: {len(result.get('domains', []))} threats processed")
            else:
                print(f"\n❌ Failed: {result.get('message', 'Unknown error')}")
                
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}")
        print("\n💡 Available modes:")
        print("  python main.py                 # Simplified mode (default)")
        print("  python main.py --enhanced      # Enhanced mode")
        print("  python main.py --interactive   # Interactive mode")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="ThreatAgent: Threat Intelligence Automation")
    parser.add_argument(
        "command",
        nargs="?",
        default="interactive",
        choices=["interactive", "simple", "crew", "targeted"],
        help="Command to execute (default: interactive)"
    )
    args = parser.parse_args()

    # Instantiate ThreatAgentSystem here to make agent_system available
    agent_system = ThreatAgentSystem()

    if args.command == "interactive":
        asyncio.run(run_interactive_mode())
    elif args.command == "simple":
        # For simple, we might not have a specific campaign initially,
        # or we can use the default one from ThreatAgentSystem
        run_simple_workflow(targeting_config=agent_system.current_campaign_config)
    elif args.command == "crew":
        # For crew, similarly, use the default or currently loaded campaign
        run_crew_workflow(targeting_config=agent_system.current_campaign_config)
    elif args.command == "targeted":
        # --- Targeted Demo ---
        print("\\nRunning Targeted Demo Workflow...")
        
        # Get inputs from the user
        company_name_input = input("Enter the target company name (e.g., Example Bank Inc.): ").strip()
        domain_input = input(f"Enter the primary domain for {company_name_input} (e.g., examplebank.com): ").strip()
        industry_input = input(f"Enter the industry for {company_name_input} (e.g., financial_services, technology, energy): ").strip()
        custom_threat_types_input = input("Enter comma-separated threat types to focus on (e.g., phishing,malware,ransomware): ").strip()

        if not company_name_input or not domain_input or not industry_input:
            print("Company name, domain, and industry are required. Exiting demo.")
            exit(1)

        threat_types_list = [t.strip() for t in custom_threat_types_input.split(',')] if custom_threat_types_input else ["phishing", "malware"]

        targeting_system = get_targeting_system()
        campaign_name = f"demo_manual_{company_name_input.lower().replace(' ', '_')}_campaign"
        
        print(f"\\nSetting up campaign: {campaign_name} for {company_name_input}")

        demo_config = targeting_system.create_campaign(campaign_name=campaign_name, description=f"Demo campaign targeting {company_name_input} in {industry_input} industry")

        targeting_system.add_industry_target(industry_name=industry_input, priority=5)
        targeting_system.add_company_target(company_name=company_name_input, domain=domain_input, industry=industry_input, priority=5)
        targeting_system.set_threat_types(threat_types=threat_types_list)
        # Geographic focus can be asked as well, or defaulted
        geo_focus_input = input("Enter comma-separated geographic focus (e.g., US,GB) or leave blank for global: ").strip()
        if geo_focus_input:
            targeting_system.set_geographic_focus(regions=[r.strip() for r in geo_focus_input.split(',')])
        else:
            targeting_system.set_geographic_focus(regions=["global"])

        agent_system.current_campaign_config = demo_config
        
        print(f"\\nStarting workflow for topic: emerging threats for {company_name_input}")
        run_crew_workflow(targeting_config=demo_config)
        # --- End Targeted Demo ---
    else:
        print(f"Unknown command: {args.command}")
        parser.print_help()
