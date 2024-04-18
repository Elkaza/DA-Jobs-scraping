import requests
from bs4 import BeautifulSoup

# Define the URL to scrape
url = 'https://www.karriere.at/jobs/wien?jobFields%5B%5D=2172'

# Fetch the page content
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')

# Find all job listings - Adjust the class name according to actual HTML structure
jobs = soup.find_all('div', class_='m-jobsListItem')

# List to store job data
job_list = []

for job in jobs:
    # Extract job title
    title_tag = job.find('h2', class_='m-jobsListItem__title')
    title = title_tag.get_text(strip=True) if title_tag else 'No title found'

    # Extract job link
    link = title_tag.find('a')['href'] if title_tag and title_tag.find('a') else 'No link found'

    # Extract company name
    company_tag = job.find('div', class_='m-jobsListItem__company')
    company_name = company_tag.get_text(strip=True) if company_tag else 'No company name found'

    # Extract location
    location_tag = job.find('span', class_='m-jobsListItem__location')
    location = location_tag.get_text(strip=True) if location_tag else 'No location found'

    # Store job info in a dictionary and add to the list
    job_info = {
        'title': title,
        'link': link,
        'company': company_name,
        'location': location
    }
    job_list.append(job_info)

# Print all job information
for job in job_list:
    print(f"Title: {job['title']}")
    print(f"Link: {job['link']}")
    print(f"Company: {job['company']}")
    print(f"Location: {job['location']}")
    print('-' * 80)  # Separator for readability
