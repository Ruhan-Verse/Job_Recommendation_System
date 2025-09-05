import requests
from bs4 import BeautifulSoup
import pandas as pd
import math
import time

job_data = []
job_ids = []
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
}
search_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=software&location=India&start={}'
jobs_per_page = 25
total_jobs = 500
num_pages = math.ceil(total_jobs / jobs_per_page)

# Fetch job IDs
for page in range(num_pages):
    if len(job_data) >= 500:
        break
    for attempt in range(3):
        res = requests.get(search_url.format(page * jobs_per_page), headers=headers)
        if res.status_code == 200:
            break
        print(f"Failed to fetch page {page}, attempt {attempt+1}: {res.status_code}")
        time.sleep(5)
    else:
        continue
    soup = BeautifulSoup(res.text, 'html.parser')
    job_elements = soup.find_all("li")
    for elem in job_elements:
        base_card = elem.find("div", {"class": "base-card"})
        if base_card:
            job_id = base_card.get('data-entity-urn', '').split(":")[3]
            job_ids.append(job_id)
    time.sleep(3)

# Fetch job details
job_detail_url = 'https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{}'
for job_id in job_ids:
    if len(job_data) >= 500:
        break
    for attempt in range(3):
        res = requests.get(job_detail_url.format(job_id), headers=headers)
        if res.status_code == 200:
            break
        print(f"Failed to fetch job {job_id}, attempt {attempt+1}: {res.status_code}")
        time.sleep(5)
    else:
        continue
    soup = BeautifulSoup(res.text, 'html.parser')
    
    details = {
        'job_ID': job_id,
        'job': None,
        'location': None,
        'company_id': None,
        'company_name': None,
        'work_type': None,
        'full_time_remote': None,
        'no_of_employ': None,
        'no_of_application': None,
        'posted_day_ago': None,
        'alumni': None,
        'Hiring_person': None,
        'linkedin_followers': None,
        'hiring_person_link': None,
        'job_details': None,
        'Column1': None
    }
    
    try:
        details['job'] = soup.find("h1", {"class": "top-card-layout_title"}).text.strip() if soup.find("h1", {"class": "top-card-layout_title"}) else None
        details['location'] = soup.find("span", {"class": "topcard_flavor topcardflavor--bullet"}).text.strip() if soup.find("span", {"class": "topcardflavor topcard_flavor--bullet"}) else None
        
        # Filter for India
        if details['location'] and not ('India' in details['location'] or any(city in details['location'] for city in ['Bangalore', 'Mumbai', 'Delhi', 'Hyderabad', 'Chennai', 'Pune', 'Kolkata'])):
            print(f"Skipping job {job_id}: Location {details['location']} not in India")
            continue
        
        company_link = soup.find("a", {"class": "topcard__org-name-link"})
        details['company_id'] = company_link.get('href', '').split('/company/')[1].split('/')[0] if company_link else None
        details['company_name'] = company_link.text.strip() if company_link else None
        criteria_list = soup.find("ul", {"class": "description__job-criteria-list"})
        if criteria_list:
            for crit in criteria_list.find_all("li"):
                subheader = crit.find("h3").text.strip()
                value = crit.find("span").text.strip()
                if subheader == "Employment type":
                    details['work_type'] = value
                if subheader == "Company size":
                    details['no_of_employ'] = value
        metadata_spans = soup.find_all("span", {"class": "posted-time-ago_text topcard_flavor--metadata"})
        # Safely handle metadata_spans
        if metadata_spans:
            details['posted_day_ago'] = metadata_spans[0].text.strip()
            details['full_time_remote'] = metadata_spans[1].text.strip() if len(metadata_spans) > 1 and metadata_spans[1].text.strip() in ['Remote', 'Hybrid', 'On-site'] else None
        applicants = soup.find("figcaption", {"class": "num-applicants__caption"})
        details['no_of_application'] = applicants.text.strip().split(' ')[0] if applicants else None
        hiring_section = soup.find("section", {"class": "hiring-team"})
        details['Hiring_person'] = hiring_section.find("span", {"class": "hiring-person__name"}).text.strip() if hiring_section else None
        details['hiring_person_link'] = hiring_section.find("a", {"class": "hiring-person__link"}).get('href') if hiring_section and hiring_section.find("a") else None
        description_section = soup.find("div", {"class": "description__text"})
        details['job_details'] = description_section.text.strip().replace('\n', ' ') if description_section else None
        job_data.append(details)
    except Exception as e:
        print(f"Error processing job {job_id}: {str(e)}")
        continue
    time.sleep(3)

df = pd.DataFrame(job_data)
df.to_csv('linkedin_jobs_dataset.csv', index=False, encoding='utf-8')
print(f"LinkedIn scraping complete. Collected {len(job_data)} India-specific jobs. Data saved to linkedin_jobs_dataset.csv")