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
MAX_PAGES = 5   # adjust if needed

def fetch_jobs():
    all_jobs = []
    for page in range(1, MAX_PAGES + 1):
        params = {
            "query": "India",        # fetch India-specific jobs
            "page": str(page),
            "num_pages": "1",
            "date_posted": "week",   # ✅ last 7 days only
        }
        resp = requests.get(BASE_URL, headers=HEADERS, params=params)
        if resp.status_code != 200:
            print(f"❌ Error {resp.status_code} on page {page}: {resp.text}")
            break

        data = resp.json()
        jobs = data.get("data", [])
        if not jobs:
            break

        for job in jobs:
            all_jobs.append({
                "title": job.get("job_title"),
                "company": job.get("employer_name"),
                "location": job.get("job_city") or job.get("job_country"),
                "created": job.get("job_posted_at_datetime_utc"),
                "category": job.get("job_employment_type"),
                "salary_min": job.get("job_min_salary"),
                "salary_max": job.get("job_max_salary"),
                "redirect_url": job.get("job_apply_link"),
            })

    return all_jobs

def save_to_csv(jobs, filename="jsearch_jobs_7days.csv"):
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
