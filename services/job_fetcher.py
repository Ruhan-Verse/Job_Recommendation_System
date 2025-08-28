import os
import requests
from dotenv import load_dotenv

load_dotenv()

def fetch_jobs():
    url = "https://example-job-api.com/search"  # Replace with RapidAPI endpoint
    headers = {
        "X-RapidAPI-Key": os.getenv("RAPIDAPI_KEY"),
        "X-RapidAPI-Host": "example-job-api.com"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    return {"error": "Failed to fetch jobs"}
