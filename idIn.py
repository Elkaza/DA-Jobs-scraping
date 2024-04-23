import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime

def setup_driver():
    options = Options()
    options.headless = False  # Set to True for no GUI
    service = Service(executable_path=r'C:\Users\Mo\Downloads\chromeDDDriver\chromedriver-win64\chromedriver-win64\chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def scrape_indeed_jobs():
    driver = setup_driver()
    wait = WebDriverWait(driver, 10)
    base_url = "https://at.indeed.com/jobs?q=IT&l=%C3%96sterreich&sort=date"
    driver.get(base_url)

    jobs_data = []
    try:
        # Wait for the job cards to be visible and retrieve them
        wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div.job_seen_beacon')))
        job_cards = driver.find_elements(By.CSS_SELECTOR, 'div.job_seen_beacon')

        for card in job_cards:
            details_link = card.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
            driver.get(details_link)
            wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.jobsearch-JobComponent')))

            # Try-except blocks to capture data or note failures
            try:
                job_title = driver.find_element(By.CSS_SELECTOR, 'h1').text
            except:
                job_title = "Title not found"
                print("Failed to find job title.")

            try:
                company = driver.find_element(By.CSS_SELECTOR, '.jobsearch-CompanyReview--heading').text
            except:
                company = "Company not found"
                print("Failed to find company name.")

            try:
                description = driver.find_element(By.CSS_SELECTOR, '#jobDescriptionText').text
            except:
                description = "Description not found"
                print("Failed to find job description.")

            jobs_data.append({
                'Title': job_title,
                'Company': company,
                'Description': description,
                'Link': details_link,
                'Date Scraped': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
            driver.back()  # Go back to the listing page
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()
        return pd.DataFrame(jobs_data)

# Run the scraping function
df = scrape_indeed_jobs()
if not df.empty:
    filename = 'indeed_jobs.csv'
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")
else:
    print("No data collected.")
