from crewai.tools import tool

@tool("MITRE TTP Mapper")
def run(iocs: list) -> list:
    """
    Map IOCs to MITRE ATT&CK TTPs.

    Args:
        iocs (list): List of classified IOCs to map to TTPs

    Returns:
        list: IOCs enriched with MITRE ATT&CK TTPs
    """
    for i in iocs:
        i["ttp"] = "T1566.001"  # Spearphishing Link
    return iocs
