import yaml
from datetime import datetime
from pathlib import Path

def generate_campaign_filename(company_name: str, timestamp: str = None) -> str:
    if not timestamp:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = company_name.replace(' ', '_')
    return f"threat_campaign_{safe_name}_{timestamp}.yaml"

def save_campaign_file(company_name: str, campaign_data: dict, folder: str = '.') -> str:
    filename = generate_campaign_filename(company_name)
    path = Path(folder) / filename
    with open(path, 'w') as f:
        yaml.dump(campaign_data, f)
    return str(path)
