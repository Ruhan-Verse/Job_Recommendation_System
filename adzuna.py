import os
import requests
import pandas as pd
from dotenv import load_dotenv

# Load credentials
load_dotenv()
APP_ID = os.getenv("ADZUNA_APP_ID")
APP_KEY = os.getenv("ADZUNA_APP_KEY")

BASE_URL = "https://api.adzuna.com/v1/api/jobs/in/search/1"

categories = [
    "software engineer", "data analyst", "marketing manager",
    "graphic designer", "chef", "sales executive",
    "sports coach", "finance analyst", "gaming", "film production"
]

cities = ["Bangalore", "Mumbai", "Delhi", "Hyderabad"]

all_jobs = []

for cat in categories:
    for city in cities:
        params = {
            "app_id": APP_ID,
            "app_key": APP_KEY,
            "results_per_page": 10,
            "what": cat,
            "where": city
        }
        try:
            response = requests.get(BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()
            jobs = data.get("results", [])

            if jobs:
                all_jobs.extend(jobs)
                print(f"✅ Found {len(jobs)} jobs for '{cat}' in {city}")
            else:
                print(f"⚠️ No jobs for '{cat}' in {city}")

        except Exception as e:
            print(f"❌ Error for {cat} in {city}: {e}")

# Save results
if all_jobs:
    df = pd.DataFrame(all_jobs)
    df.to_csv("adzuna_india_jobs.csv", index=False, encoding="utf-8")
    print(f"\n🎉 Saved {len(df)} jobs into adzuna_india_jobs.csv")
else:
    print("⚠️ Still no jobs found at all.")
