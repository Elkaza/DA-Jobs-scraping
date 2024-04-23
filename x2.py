import requests
from bs4 import BeautifulSoup
import csv

# URL to scrape
url = 'https://www.karriere.at/jobs?jobFields%5B%5D=2172#7159438'

# Send HTTP request
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Assuming structure to identify jobs, modify as needed
jobs = soup.find_all('div', class_='m-jobDetailContent__inner')

# CSV file structure
csv_file = open('jobs.csv', 'w', newline='', encoding='utf-8')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Job Title', 'Company Name', 'Location', 'Job Description', 'Publication Date'])

# Loop through each job and extract information
for job in jobs:
    try:
        job_title = job.find('h1', class_='m-jobHeader__jobTitle').text.strip()
        company_name = job.find('div', class_='m-jobHeader__companyTitle').text.strip()
        location = job.find('li', class_='m-jobHeader__keyfactBoxItem').text.strip()
        job_description = job.find('div', class_='m-jobContent__jobText').text.strip()
        publication_date = job.find('li', class_='m-jobHeader__keyfactBoxItem', text=lambda x: x and 'veröffentlicht' in x).text.strip()
        
        # Write to CSV
        csv_writer.writerow([job_title, company_name, location, job_description, publication_date])
    except Exception as e:
        print(f"Error processing job: {e}")

# Close the file
csv_file.close()
print("Data has been written to CSV.")
