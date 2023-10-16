#!/usr/bin/python
import requests
from bs4 import BeautifulSoup

url="https://www.linkedin.com/jobs/search/?currentJobId=3737830952&keywords=network%20engineer%20internship&origin=BLENDED_SEARCH_RESULT_CARD_NAVIGATION&originToLandingJobPostings=3737830952%2C3725523520%2C3702787742"

response = requests.get(url)
soup = BeautifulSoup(response.text,'html.parser')
print(soup)