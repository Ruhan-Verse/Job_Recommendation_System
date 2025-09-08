import requests
import pandas as pd

BASE_URL = "https://jobdataapi.com/api"

# Step 1: Fetch industries (to know categories available)
industries_url = f"{BASE_URL}/industries/"
industries_resp = requests.get(industries_url)

if industries_resp.status_code != 200:
    print("❌ Error fetching industries:", industries_resp.text)
    exit()

industries_data = industries_resp.json()
industries = [ind.get("name") for ind in industries_data]

print(f"✅ Found {len(industries)} industries")

# Pick first 5 industries for demo (so we don't overload)
sample_industries = industries[:5]

all_jobs = []

# Step 2: Fetch jobs per industry
for ind in sample_industries:
    try:
        jobs_url = f"{BASE_URL}/jobs/"
        params = {
            "country_code": "IN",   # India jobs
            "industry": ind,        # filter by industry
            "results_per_page": 20
        }
        resp = requests.get(jobs_url, params=params)
        resp.raise_for_status()
        data = resp.json()

        # Some APIs return directly a list, others wrap in dict
        jobs = data.get("results", data)

        print(f"📌 {len(jobs)} jobs found in industry: {ind}")

        for job in jobs:
            all_jobs.append({
                "title": job.get("title"),
                "company": job.get("company"),
                "industry": ind,
                "location": job.get("location"),
                "job_type": job.get("job_type"),
                "salary": job.get("salary"),
                "posted_date": job.get("date_posted"),
                "apply_link": job.get("url")
            })

    except Exception as e:
        print(f"❌ Error fetching jobs for {ind}: {e}")

# Step 3: Save to CSV
if all_jobs:
    df = pd.DataFrame(all_jobs)
    df.to_csv("jobdataapi_jobs_free.csv", index=False, encoding="utf-8")
    print(f"\n🎉 Saved {len(df)} jobs into jobdataapi_jobs_free.csv")
else:
    print("⚠️ No jobs fetched.")
