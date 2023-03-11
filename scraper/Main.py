from GenericDriver import FireFoxWebDriver
from GenericDriver import ChromeWebDriver
from GlassDoorScraper import GlassDoorScraper

from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import sys 
import time 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import numpy as np 

def create_workers(num_workers, company_code, company_name):
    """Creates multiple clients, intended for async operations."""
    workers = []
    for i in range(num_workers):
        account_type = f"Facebook_{i}"
        worker = GlassDoorScraper(driver=ChromeWebDriver(), company_code=company_code, company_name=company_name)
        try: 
            worker.login_using_facebook(account_type=account_type)
        except: 
            print(f"worker#{i} failed to login")
            continue
        workers.append(worker)
    if len(workers) == 0:
        print(f"No workers logged in, please check accounts.json folder")
        sys.exit(1)
    return workers

def create_worker(company_code, company_name, account_number):
    """Creates 1 worker, that will be used to scrape glassdoor"""
    account_type = f"Facebook_{account_number}"
    try:
        worker = GlassDoorScraper(driver=ChromeWebDriver(), company_code=company_code, company_name=company_name)
        worker.login_using_facebook(account_type=account_type)
    except InvalidSessionIdException:
        print(f"Failed to login using {account_type} - Blocked by captcha.")
        sys.exit(1)
    return worker

def start_worker(worker, batch_size):
    start_time = time.time()
    while(worker.list_of_review_pages):
        url = worker.list_of_review_pages.pop(0)
        try:
            review_elements = worker._get_reviews_on_page(url)
            reviews = worker._extract_reviews(review_elements)
            worker.reviews_collected.append(reviews)
            if (len(worker.reviews_collected) == batch_size) or (len(worker.list_of_review_pages) == 0):
                worker.dump_reviews_json(worker.reviews_collected)
                worker.reviews_collected.clear()
                end_time = time.time()
                elapsed_time = end_time - start_time # stop timer
                print(f"{batch_size} urls scrapped. Time Elapsed: {elapsed_time}")
                start_time = end_time # reset timer

        except Exception as e:
            print(f"Error scraping reviews from {url}: {str(e)}")

def main():
    # Modify company_code, company_name and account_number (see accounts.json)
    company_code = 138872 
    company_name = "NCS"
    # will be resolved to Facebook_0 in accounts.json. 
    account_number = 0 

    # Will scrap 100 urls (10 reviews per url) before dumping results to json
    batch_size = 100 

    worker = create_worker(company_code, company_name, account_number)
    worker.generate_urls()
    print(f"Starting to scrape {company_name} in batches of {batch_size} urls.")
    start_worker(worker, batch_size)

if __name__ == "__main__":
  main()
