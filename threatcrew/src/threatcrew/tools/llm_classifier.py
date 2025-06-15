from crewai.tools import tool
import time
import uuid
from typing import List, Dict
from .memory_system import get_memory
from .finetuning_system import get_finetuner

@tool("IOC Classifier")
def run(indicators: list) -> list:
    """
    Classify a list of indicators using LLM analysis with memory-enhanced context.

    Args:
        indicators (list): List of indicators to classify

    Returns:
        list: List of classified indicators with risk levels and categories
    """
    memory = get_memory()
    finetuner = get_finetuner()
    session_id = str(uuid.uuid4())
    
    results = []
    start_time = time.time()
    
    for indicator in indicators:
        # Check if we've seen this IOC before
        similar_iocs = memory.search_similar_iocs(indicator, limit=3)
        
        if similar_iocs and similar_iocs[0]['similarity'] > 0.9:
            # Use known classification with high confidence
            known_ioc = similar_iocs[0]
            result = {
                "ioc": indicator,
                "risk": known_ioc['risk_level'],
                "category": known_ioc['category'],
                "confidence": known_ioc['confidence'],
                "source": "memory",
                "similar_threats": len(similar_iocs)
            }
        else:
            # Perform new classification with context
            result = _classify_with_context(indicator, similar_iocs)
            
            # Store new classification in memory
            ioc_id = memory.store_ioc(
                ioc=indicator,
                ioc_type=_detect_ioc_type(indicator),
                risk_level=result['risk'],
                category=result['category'],
                confidence=result.get('confidence', 0.7),
                source="llm_analysis",
                metadata={
                    "session_id": session_id,
                    "reasoning": result.get('reasoning', ''),
                    "similar_count": len(similar_iocs)
                }
            )
        
        results.append(result)
    
    # Store analysis session
    processing_time = time.time() - start_time
    memory.store_analysis(
        session_id=session_id,
        analysis_type="ioc_classification",
        input_data=indicators,
        output_data=results,
        confidence=sum(r.get('confidence', 0.7) for r in results) / len(results),
        processing_time=processing_time
    )
    
    return results

def _classify_with_context(indicator: str, similar_iocs: List[Dict]) -> Dict:
    """Classify an indicator with historical context."""
    
    # Enhanced classification logic based on patterns
    risk_level = "medium"
    category = "unknown"
    confidence = 0.5
    reasoning = ""
    
    indicator_lower = indicator.lower()
    
    # Domain analysis
    if "." in indicator and not indicator.replace(".", "").replace("-", "").isdigit():
        category = "domain"
        
        # Banking/financial keywords
        banking_keywords = ["bank", "banking", "login", "secure", "account", "paypal", "visa", "mastercard"]
        if any(keyword in indicator_lower for keyword in banking_keywords):
            risk_level = "high"
            category = "phishing"
            confidence = 0.8
            reasoning = "Domain contains banking/financial keywords commonly used in phishing"
        
        # Suspicious TLDs
        suspicious_tlds = [".tk", ".ml", ".cf", ".ga", ".ru", ".cc"]
        if any(indicator_lower.endswith(tld) for tld in suspicious_tlds):
            risk_level = "high"
            confidence = min(confidence + 0.2, 0.9)
            reasoning += " | Suspicious TLD commonly used in malicious campaigns"
        
        # Government impersonation
        gov_keywords = ["gov", "government", "official", "rbi", "irs", "federal"]
        if any(keyword in indicator_lower for keyword in gov_keywords):
            if not indicator_lower.endswith(".gov"):
                risk_level = "medium" if risk_level == "low" else "high"
                category = "phishing"
                confidence = 0.7
                reasoning += " | Government impersonation attempt"
    
    # IP address analysis
    elif indicator.replace(".", "").isdigit():
        category = "ip_address"
        parts = indicator.split(".")
        
        if len(parts) == 4 and all(0 <= int(part) <= 255 for part in parts):
            # Private IP ranges
            if (parts[0] == "192" and parts[1] == "168") or \
               (parts[0] == "10") or \
               (parts[0] == "172" and 16 <= int(parts[1]) <= 31):
                risk_level = "low"
                confidence = 0.1
                reasoning = "Private IP address range"
            else:
                risk_level = "medium"
                confidence = 0.6
                reasoning = "Public IP address requires investigation"
    
    # Use similar IOCs to adjust classification
    if similar_iocs:
        similar_risks = [ioc['risk_level'] for ioc in similar_iocs[:2]]
        similar_categories = [ioc['category'] for ioc in similar_iocs[:2]]
        
        # If similar IOCs have consistent high risk, increase confidence
        if all(risk == "high" for risk in similar_risks):
            risk_level = "high"
            confidence = min(confidence + 0.2, 0.9)
            reasoning += " | Similar indicators previously classified as high risk"
        
        # Use most common category from similar IOCs
        if similar_categories and similar_categories[0] != "unknown":
            category = similar_categories[0]
    
    return {
        "ioc": indicator,
        "risk": risk_level,
        "category": category,
        "confidence": round(confidence, 2),
        "reasoning": reasoning.strip(" |"),
        "source": "enhanced_analysis"
    }

def _detect_ioc_type(indicator: str) -> str:
    """Detect the type of IOC."""
    if "." in indicator and not indicator.replace(".", "").replace("-", "").isdigit():
        return "domain"
    elif indicator.replace(".", "").isdigit():
        return "ip_address"
    elif "@" in indicator:
        return "email"
    elif len(indicator) == 32 or len(indicator) == 40 or len(indicator) == 64:
        return "hash"
    else:
        return "unknown"
