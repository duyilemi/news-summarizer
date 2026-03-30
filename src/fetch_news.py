import os
import requests
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
BASE_URL = "https://newsapi.org/v2/top-headlines"

def fetch_top_headlines(country="us", page_size=10):
    """Fetch top headlines from NewsAPI."""
    params = {
        "country": country,
        "pageSize": page_size,
        "apiKey": NEWS_API_KEY
    }
    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()
    data = response.json()
    return data

def save_raw_data(data, filename=None):
    """Save raw JSON to data/raw/ with timestamp."""
    if filename is None:
        filename = f"raw_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    os.makedirs("data/raw", exist_ok=True)
    filepath = f"data/raw/{filename}"
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)
    return filepath