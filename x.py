from bs4 import BeautifulSoup
import requestsurl = 'https://www.karriere.at/jobs/wien?jobFields%5B%5D=2172'

page = requests.get(url)

soup = BeautifulSoup(page.text, 'html')
print(soup)

