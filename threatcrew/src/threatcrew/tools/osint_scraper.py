from crewai.tools import tool

@tool("OSINT Scraper")
def run():
    """
    Scrape OSINT sources for suspicious indicators and domains.
    
    Returns:
        list: A list of suspicious domains from OSINT sources.
    """
    return [
        "login-hdfcbank.in",
        "secure-paypal-alert.net",
        "gov-rbi-alert.org"
    ]
