from crewai.tools import tool

@tool("Sigma Rule Generator")
def run(data: list) -> list:
    """
    Generate Sigma detection rules from enriched IOCs.

    Args:
        data (list): List of enriched IOCs with classifications and TTPs

    Returns:
        list: List of Sigma rules for detecting the threats
    """
    return [
        {
            "title": f"Detect {i['ioc']}",
            "sigma": {
                "detection": {"selection": {"url": i["ioc"]}},
                "condition": "selection",
                "level": i["risk"]
            }
        } for i in data
    ]
