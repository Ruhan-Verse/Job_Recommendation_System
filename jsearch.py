import os
import requests
import csv
from dotenv import load_dotenv

# Load env vars
load_dotenv()
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")

BASE_URL = "https://jsearch.p.rapidapi.com/search"
HEADERS = {
    "x-rapidapi-host": "jsearch.p.rapidapi.com",
    "x-rapidapi-key": RAPIDAPI_KEY
}

RESULTS_PER_PAGE = 50
MAX_PAGES = 3   # to save credits; increase if needed

# Diverse job categories
categories = [
    "software engineer",
    "data analyst",
    "sales executive",
    "graphic designer",
    "chef",
    "sports coach",
    "gaming",
    "film production",
    "marketing manager",
    "cryptocurrency analyst"
]

def fetch_jobs():
    all_jobs = []
    for cat in categories:
        print(f"\n🔍 Fetching jobs for: {cat}")
        for page in range(1, MAX_PAGES + 1):
            params = {
                "query": f"{cat} India",
                "page": str(page),
                "num_pages": "1",
                "date_posted": "week",   # ✅ only last 7 days
            }
            resp = requests.get(BASE_URL, headers=HEADERS, params=params)
            if resp.status_code != 200:
                print(f"❌ Error {resp.status_code} for {cat} on page {page}: {resp.text}")
                break

            data = resp.json()
            jobs = data.get("data", [])
            if not jobs:
                break

            for job in jobs:
                all_jobs.append({
                    "category_query": cat,
                    "title": job.get("job_title"),
                    "company": job.get("employer_name"),
                    "location": job.get("job_city") or job.get("job_country"),
                    "created": job.get("job_posted_at_datetime_utc"),
                    "employment_type": job.get("job_employment_type"),
                    "salary_min": job.get("job_min_salary"),
                    "salary_max": job.get("job_max_salary"),
                    "redirect_url": job.get("job_apply_link"),
                })
            print(f"✅ Got {len(jobs)} jobs for {cat} (page {page})")

    return all_jobs

def save_to_csv(jobs, filename="jsearch_jobs_india_7days.csv"):
    if not jobs:
        print("⚠️ No jobs found in the last 7 days.")
        return

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=jobs[0].keys())
        writer.writeheader()
        writer.writerows(jobs)
    print(f"\n🎉 Saved {len(jobs)} jobs across {len(categories)} categories into {filename}")

if __name__ == "__main__":
    jobs = fetch_jobs()
    save_to_csv(jobs)
