import os
import requests
import csv
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

# Load env vars
load_dotenv()
APP_ID = os.getenv("ADZUNA_APP_ID")
APP_KEY = os.getenv("ADZUNA_APP_KEY")

BASE_URL = "https://api.adzuna.com/v1/api/jobs/in/search/{}"
RESULTS_PER_PAGE = 50
MAX_PAGES = 10   # adjust if needed

# Time filter: last 7 days
now = datetime.now(timezone.utc)
time_cutoff = now - timedelta(days=7)

def fetch_jobs():
    all_jobs = []
    for page in range(1, MAX_PAGES + 1):
        url = BASE_URL.format(page)
        params = {
            "app_id": APP_ID,
            "app_key": APP_KEY,
            "results_per_page": RESULTS_PER_PAGE,
            "sort_by": "date",   # ensures newest jobs come first
        }
        resp = requests.get(url, params=params)
        if resp.status_code != 200:
            print(f"Error {resp.status_code} on page {page}")
            break

        data = resp.json()
        jobs = data.get("results", [])
        if not jobs:
            break

        for job in jobs:
            created = datetime.fromisoformat(job["created"].replace("Z", "+00:00"))
            if created >= time_cutoff:   # only last 7 days
                all_jobs.append({
                    "title": job.get("title"),
                    "company": job.get("company", {}).get("display_name"),
                    "location": job.get("location", {}).get("display_name"),
                    "created": created.strftime("%Y-%m-%d %H:%M"),
                    "category": job.get("category", {}).get("label"),
                    "salary_min": job.get("salary_min"),
                    "salary_max": job.get("salary_max"),
                    "redirect_url": job.get("redirect_url"),
                })

    return all_jobs

def save_to_csv(jobs, filename="adzuna_jobs_7days.csv"):
    if not jobs:
        print("⚠️ No jobs found in the last 7 days.")
        return

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=jobs[0].keys())
        writer.writeheader()
        writer.writerows(jobs)
    print(f"✅ Saved {len(jobs)} jobs to {filename}")

if __name__ == "__main__":
    jobs = fetch_jobs()
    save_to_csv(jobs)
