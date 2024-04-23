import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
from time import sleep
from random import randint

def clean_html(content):
    """Remove unwanted HTML tags and return clean text."""
    soup = BeautifulSoup(content, 'html.parser')
    for tag in soup(["script", "style", "meta", "link", "header", "footer", "nav"]):
        tag.extract()
    text = soup.get_text(separator=' ')
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    return ' '.join(chunk for chunk in chunks if chunk)

def find_frameworks(description, frameworks):
    """Find and return frameworks mentioned in the description."""
    matches = set()
    for framework in frameworks:
        if framework.lower() in description.lower():
            matches.add(framework)
    return ', '.join(matches) if matches else "Not found"

def scrape_job_listings():
    """Scrape job listings and return a DataFrame."""
    base_url = "https://www.karriere.at/jobs"
    search_params = {"keywords": "IT", "location": "Wien"}
    jobs_data = []
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    
    with requests.Session() as session:
        session.headers.update(headers)
        
        for page in range(1, 11):  # Adjust to scrape more pages
            print(f"Scraping page {page}...")
            search_params['page'] = page
            response = session.get(base_url, params=search_params)
            soup = BeautifulSoup(response.text, 'html.parser')
            job_listings = soup.find_all('div', class_='m-jobsListItem__dataContainer')

            for job in job_listings:
                title_info = job.find('h2', class_='m-jobsListItem__title')
                job_title = title_info.text.strip() if title_info else "No title available"
                job_link = title_info.find('a')['href'] if title_info and title_info.find('a') else None
                company_info = job.find('a', class_='m-jobsListItem__companyName--link')
                company = company_info.text.strip() if company_info else "Unknown"

                description = "No description available"
                if job_link:
                    print(f"Fetching job details for {job_title} at {job_link}...")
                    job_detail_response = session.get(job_link)
                    description = clean_html(job_detail_response.text)

                frameworks_found = find_frameworks(description, frameworks_list)

                jobs_data.append({
                    'Company': company,
                    'Job Title': job_title,
                    'URL': job_link,
                    'Description': description,
                    'Frameworks': frameworks_found,
                    'Extract Date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })

                sleep(randint(1, 3))  # Random delay to avoid being blocked
            print(f"Completed page {page}.")

    print("Scraping complete.")
    return pd.DataFrame(jobs_data)

frameworks_list = [
    "ITIL", "DevOps", "Agile", "Scrum", "Kanban", "COBIT", "TOGAF", "Six Sigma", "Lean IT", "ISO/IEC 27001"
]

df = scrape_job_listings()
current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
filename = f'it_jobs_karriere_at_{current_time}.csv'
try:
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")
except Exception as e:
    print(f"Failed to save file: {e}")
