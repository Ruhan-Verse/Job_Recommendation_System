from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import math
import time

job_data = []
options = Options()
options.headless = True
driver = webdriver.Chrome(options=options)

search_url = 'https://www.naukri.com/software-jobs-in-india-{}'
jobs_per_page = 20
total_jobs = 500
num_pages = math.ceil(total_jobs / jobs_per_page)

for page in range(1, num_pages + 1):
    if len(job_data) >= 500:
        break
    driver.get(search_url.format(page))
    time.sleep(5)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    job_cards = soup.find_all('div', class_='srp-jobtuple-wrapper')
    
    for card in job_cards:
        if len(job_data) >= 500:
            break
        details = {
            'job_ID': None,
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
        title_elem = card.find('a', class_='title')
        details['job'] = title_elem.text.strip() if title_elem else None
        details['job_ID'] = title_elem['href'].split('-')[-1] if title_elem and title_elem['href'] else None
        details['location'] = card.find('span', class_='locWdth').text.strip() if card.find('span', class_='locWdth') else None
        if details['location'] and 'India' not in details['location'] and not any(city in details['location'] for city in ['Bangalore', 'Mumbai', 'Delhi', 'Hyderabad', 'Chennai', 'Pune', 'Kolkata']):
            continue
        details['company_name'] = card.find('a', class_='comp-name').text.strip() if card.find('a', class_='comp-name') else None
        details['full_time_remote'] = 'Remote' if details['location'] and 'remote' in details['location'].lower() else None
        details['Column1'] = card.find('span', class_='sal-wrap').text.strip() if card.find('span', class_='sal-wrap') else None
        details['posted_day_ago'] = card.find('span', class_='job-post-day').text.strip() if card.find('span', class_='job-post-day') else None
        link = title_elem['href'] if title_elem else None
        if link:
            driver.get(link)
            time.sleep(3)
            detail_soup = BeautifulSoup(driver.page_source, 'html.parser')
            description = detail_soup.find('div', class_='job-desc')
            details['job_details'] = description.text.strip().replace('\n', ' ') if description else None
        job_data.append(details)
    time.sleep(3)

driver.quit()
df = pd.DataFrame(job_data)
df.to_csv('naukri_jobs_dataset.csv', index=False, encoding='utf-8')
print(f"Naukri scraping complete. Collected {len(job_data)} India-specific jobs. Data saved to naukri_jobs_dataset.csv")