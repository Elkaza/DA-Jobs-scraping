import csv
from datetime import datetime
import requests
from bs4 import BeautifulSoup

## Setup the query and url

def get_url(position, location):
    """Generate url from position and location"""
    template = 'https://www.indeed.com/jobs?q={}&l={}'
    position = position.replace(' ', '+')
    location = location.replace(' ', '+')
    url = template.format(position, location)
    return url


url = get_url('senior accountant', 'charlotte nc')
print(url)


##
##