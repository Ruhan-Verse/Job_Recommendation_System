import os
import requests
import csv
from datetime import datetime
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")

URL = "https://jobs-search-api.p.rapidapi.com/getjobs"
HEADERS = {
    "x-rapidapi-key": RAPIDAPI_KEY,
    "x-rapidapi-host": "jobs-search-api.p.rapidapi.com",
    "Content-Type": "application/json"
}

# Categories we want (you can expand this list)
CATEGORIES = [
    "software engineer",
    "data analyst",
    "marketing manager",
    "sales executive",
    "graphic designer",
    "chef",
    "sports coach",
    "gaming",
    "film production",
    "cryptocurrency analyst",
    "management",
    "politics research",
    "electronics engineer"
]

def fetch_jobs(search_term, location="India", results=20, hours_old=168):
    payload = {
        "search_term": search_term,
        "location": location,
        "results_wanted": results,
        "site_name": ["indeed", "linkedin", "glassdoor", "zip_recruiter"],
        "distance": 100,
        "job_type": "fulltime",
        "is_remote": False,
        "linkedin_fetch_description": False,
        "hours_old": hours_old
    }

    response = requests.post(URL, json=payload, headers=HEADERS)
    if response.status_code != 200:
        print(f"❌ API Error {response.status_code} - {response.text}")
        return []

    data = response.json()
    jobs = data.get("jobs", [])
    results = []
    for job in jobs:
        results.append({
            "category": search_term,
            "title": job.get("title"),
            "company": job.get("company"),
            "location": job.get("location"),
            "date_posted": job.get("date_posted"),
            "via": job.get("site"),
            "url": job.get("url"),
        })
    return results

def save_to_csv(jobs, filename="jobs_api_allcategories.csv"):
    if not jobs:
        print("⚠️ No jobs found")
        return
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=jobs[0].keys())
        writer.writeheader()
        writer.writerows(jobs)
    print(f"✅ Saved {len(jobs)} jobs to {filename}")

if __name__ == "__main__":
    all_jobs = []
    for cat in CATEGORIES:
        print(f"🔍 Fetching jobs for category: {cat}")
        jobs = fetch_jobs(cat, "India", results=30, hours_old=168)  # last 7 days
        all_jobs.extend(jobs)

    save_to_csv(all_jobs, "jobs_api_allcategories.csv")
    print(f"🎉 Total {len(all_jobs)} jobs fetched across {len(CATEGORIES)} categories.")
