from crewai.tools import tool
import time
import uuid
from typing import List, Dict
from datetime import datetime

# Import memory system with fallback
try:
    from .memory_system import get_memory
    MEMORY_AVAILABLE = True
except ImportError:
    MEMORY_AVAILABLE = False

@tool("Report Writer")
def run(data: list) -> str:
    """
    Generate a Markdown report from enriched threat data with memory-enhanced context.

    Args:
        data (list): List of enriched IOCs with classifications and TTPs

    Returns:
        str: Markdown formatted threat intelligence report
    """
    session_id = str(uuid.uuid4())
    start_time = time.time()
    
    # Enhanced report generation with memory context
    report = _generate_enhanced_report(data, session_id)
    
    # Store report generation in memory if available
    if MEMORY_AVAILABLE:
        memory = get_memory()
        processing_time = time.time() - start_time
        memory.store_analysis(
            session_id=session_id,
            analysis_type="report_generation",
            input_data=data,
            output_data=report,
            confidence=0.8,
            processing_time=processing_time
        )
    
    return report

def _generate_enhanced_report(data: List[Dict], session_id: str) -> str:
    """Generate an enhanced threat intelligence report."""
    
    # Header with timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
    
    report = f"""# Threat Intelligence Report
**Report ID**: {session_id[:8]}  
**Generated**: {timestamp}  
**Analyst**: ThreatAgent AI System  

## Executive Summary
"""
    
    # Analyze data for executive summary
    total_iocs = len(data)
    high_risk_count = sum(1 for item in data if item.get('risk', '').lower() == 'high')
    medium_risk_count = sum(1 for item in data if item.get('risk', '').lower() == 'medium')
    low_risk_count = sum(1 for item in data if item.get('risk', '').lower() == 'low')
    
    # Get unique categories and TTPs
    categories = list(set(item.get('category', 'unknown') for item in data))
    ttps = list(set(item.get('ttp', '') for item in data if item.get('ttp')))
    
    # Executive summary with threat landscape analysis
    if high_risk_count > 0:
        threat_level = "HIGH"
        summary_text = f"Critical threat indicators identified requiring immediate attention. "
    elif medium_risk_count > 0:
        threat_level = "MEDIUM"
        summary_text = f"Moderate threat activity detected requiring monitoring and analysis. "
    else:
        threat_level = "LOW"
        summary_text = f"Minimal threat activity observed in current analysis period. "
    
    summary_text += f"Analysis of {total_iocs} indicators reveals threats primarily in {', '.join(categories[:3])} categories."
    
    report += f"""**Threat Level**: {threat_level}  
**Total Indicators**: {total_iocs}  
**Primary Categories**: {', '.join(categories[:3])}  

{summary_text}

## Threat Breakdown
- **High Risk**: {high_risk_count} indicators
- **Medium Risk**: {medium_risk_count} indicators  
- **Low Risk**: {low_risk_count} indicators

## Indicators of Compromise (IOCs)
"""
    
    # Group IOCs by risk level for better presentation
    risk_groups = {'high': [], 'medium': [], 'low': []}
    
    for item in data:
        risk = item.get('risk', 'medium').lower()
        if risk in risk_groups:
            risk_groups[risk].append(item)
        else:
            risk_groups['medium'].append(item)
    
    # Add IOCs by risk level
    for risk_level in ['high', 'medium', 'low']:
        if risk_groups[risk_level]:
            report += f"\n### {risk_level.upper()} Risk Indicators\n"
            for item in risk_groups[risk_level]:
                ioc = item.get('ioc', 'unknown')
                category = item.get('category', 'unknown')
                confidence = item.get('confidence', 0.0)
                
                # Add confidence indicator
                confidence_text = ""
                if isinstance(confidence, (int, float)):
                    if confidence >= 0.8:
                        confidence_text = " (High Confidence)"
                    elif confidence >= 0.6:
                        confidence_text = " (Medium Confidence)"
                    else:
                        confidence_text = " (Low Confidence)"
                
                report += f"- **{ioc}** - {category.title()}{confidence_text}\n"
                
                # Add reasoning if available
                reasoning = item.get('reasoning', '')
                if reasoning:
                    report += f"  - *Analysis*: {reasoning}\n"
    
    # MITRE ATT&CK TTPs section
    if ttps:
        report += f"\n## MITRE ATT&CK TTPs\n"
        unique_ttps = list(set(ttps))
        
        # TTP descriptions (basic mapping)
        ttp_descriptions = {
            "T1566.001": "Phishing: Spearphishing Attachment",
            "T1566.002": "Phishing: Spearphishing Link", 
            "T1566.003": "Phishing: Spearphishing via Service",
            "T1071.001": "Application Layer Protocol: Web Protocols",
            "T1071.004": "Application Layer Protocol: DNS",
            "T1204.001": "User Execution: Malicious Link",
            "T1204.002": "User Execution: Malicious File",
            "T1589.002": "Gather Victim Network Information: DNS"
        }
        
        for ttp in sorted(unique_ttps):
            description = ttp_descriptions.get(ttp, "Unknown TTP")
            report += f"- **{ttp}** - {description}\n"
    
    # Historical context if memory is available
    if MEMORY_AVAILABLE:
        try:
            memory = get_memory()
            stats = memory.get_statistics()
            
            if stats['total_iocs'] > len(data):
                report += f"\n## Historical Context\n"
                report += f"- **Total IOCs in Database**: {stats['total_iocs']}\n"
                report += f"- **Previous Analyses**: {stats['total_analyses']}\n"
                
                if stats['category_distribution']:
                    top_categories = sorted(stats['category_distribution'].items(), 
                                          key=lambda x: x[1], reverse=True)[:3]
                    report += f"- **Common Threat Categories**: {', '.join([cat for cat, _ in top_categories])}\n"
        except Exception:
            pass  # Skip historical context if there are issues
    
    # Recommendations section
    report += f"\n## Recommendations\n"
    
    if high_risk_count > 0:
        report += """
### Immediate Actions Required
1. **Block all high-risk indicators** at network perimeter (firewalls, DNS, proxy)
2. **Alert security team** for immediate investigation
3. **Hunt for related indicators** in network logs and SIEM systems
4. **Notify stakeholders** of potential compromise indicators
"""
    
    if medium_risk_count > 0:
        report += """
### Medium Priority Actions
1. **Monitor medium-risk indicators** for suspicious activity
2. **Enhance logging** for these indicators across security controls
3. **Schedule threat hunting** activities to investigate further
"""
    
    # General recommendations based on categories
    if 'phishing' in categories:
        report += """
### Phishing-Specific Recommendations
1. **Update email security filters** to block identified domains
2. **User awareness training** emphasizing phishing recognition
3. **Browser DNS filtering** to prevent access to malicious domains
4. **Monitor for similar domain registrations** using threat intelligence feeds
"""
    
    if 'malware' in categories:
        report += """
### Malware-Specific Recommendations  
1. **Update antivirus signatures** with new indicators
2. **Endpoint detection rules** for behavioral analysis
3. **Network segmentation** to limit malware spread
4. **Backup verification** to ensure recovery capabilities
"""
    
    # Footer with metadata
    report += f"""
---
**Report Generation Details**:
- Analysis Engine: ThreatAgent v1.0
- Processing Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}
- Confidence Level: Medium-High
- Data Sources: OSINT, Memory Database, MITRE ATT&CK Framework

*This report was generated automatically by AI analysis. Human verification recommended for critical decisions.*
"""
    
    return report
