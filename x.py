import requests
from bs4 import BeautifulSoup
import csv

# List of frameworks and methods to search for
frameworks_methods = ["TOGAF", "ArchiMate", "Zachman Framework", "DoDAF", "FEAF", "COBIT", "ITIL", "IT4IT",
                      "ISO/IEC 27001", "ISO/IEC 38500", "CMMI", "PMBOK Guide", "Prince2", "Agile", "SAFe",
                      "Lean IT", "Balanced Scorecard", "Value Stream Mapping", "Six Sigma", "ISO 9001", "BPMN",
                      "Scrum", "Kanban", "DevOps", "ISO/IEC 20000"]

# URL to scrape from
url = 'https://www.karriere.at/jobs/wien?jobFields%5B%5D=2172'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Debug print
print("URL Loaded:", response.status_code)  # Check if the URL is loaded correctly
print("Soup Title:", soup.title.string)  # See what the title tag of the soup is

# Example selectors, adjust as needed
job_cards = soup.find_all('div', class_='job-card-selector')  # Adjust the class name based on actual HTML

# Debug print
print("Number of Job Cards Found:", len(job_cards))

results = []

for card in job_cards:
    job_title = card.find('h2').text.strip() if card.find('h2') else 'No Title Found'
    company_name = card.find('div', class_='company-name-selector').text.strip() if card.find('div', class_='company-name-selector') else 'No Company Found'
    job_link = card.find('a', href=True)['href'] if card.find('a', href=True) else 'No Link Found'

    # Debug print
    print("Job Title:", job_title)
    print("Company Name:", company_name)
    print("Job Link:", job_link)

    # Follow link to job description page
    job_response = requests.get(job_link)
    job_soup = BeautifulSoup(job_response.text, 'html.parser')
    job_description = job_soup.find('div', class_='job-description-selector').text if job_soup.find('div', class_='job-description-selector') else ''

    # Debug print
    print("Job Description Length:", len(job_description))

    # Check for frameworks/methods in the description
    found_frameworks = [fm for fm in frameworks_methods if fm.lower() in job_description.lower()]

    if found_frameworks:
        results.append({
            'Job Title': job_title,
            'Company Name': company_name,
            'Found Frameworks/Methods': ', '.join(found_frameworks)
        })

# Write results to a CSV file
with open('jobs_with_frameworks.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=['Job Title', 'Company Name', 'Found Frameworks/Methods'])
    writer.writeheader()
    writer.writerows(results)

print("CSV file has been created. Total Entries:", len(results))
