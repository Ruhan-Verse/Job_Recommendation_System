import requests
from bs4 import BeautifulSoup

API_KEY = "e2a2630d57f91595583e3c9fc9010a92"

# Target Internshala jobs page
target_url = "https://internshala.com/internships"

# Build API request
api_url = f"http://api.scraperapi.com?api_key={API_KEY}&url={target_url}&render=true"

# Send request
response = requests.get(api_url)
html = response.text

# Parse with BeautifulSoup
soup = BeautifulSoup(html, "html.parser")

# Example: Extract job titles
jobs = []
for job_card in soup.select(".individual_internship"):
    title = job_card.select_one(".heading_4_5 a")
    company = job_card.select_one(".company_name")
    location = job_card.select_one(".location_link")
    jobs.append({
        "title": title.get_text(strip=True) if title else "N/A",
        "company": company.get_text(strip=True) if company else "N/A",
        "location": location.get_text(strip=True) if location else "N/A"
    })

# Print results
for j in jobs:
    print(j)
