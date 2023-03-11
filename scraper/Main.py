from GenericDriver import FireFoxWebDriver
from GenericDriver import ChromeWebDriver
from GlassDoorScraper import GlassDoorScraper

from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import InvalidSessionIdException
import sys 
import time 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import numpy as np 
import os 

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
                print(f"Batch of {batch_size} urls scrapped. Time Elapsed: {elapsed_time}")
                start_time = end_time # reset timer
        except Exception as e:
            print(f"Error scraping reviews from {url}: {str(e)}")

def resume_work(worker):
    """For jobs that were prematurely terminated, can invoke this to resume scraping 
        at the i'th URL. 
    """
    folder_path = os.path.join("..", "data", f"{worker.company_name}")
    if os.path.exists(folder_path): # Get number of previously scrapped reviews
        num_json_files = len([f for f in os.listdir(folder_path) if f.endswith('.json')])
    else: # included such that resume_work wont cause script to break if left uncommented.
        num_json_files = 0

    new_index = num_json_files * 100
    worker.list_of_review_pages = worker.list_of_review_pages[new_index:]
    worker.batch_counter = num_json_files
    print(f"Resuming {worker.company_name} Batch: #{worker.batch_counter}\nScrape from url: {worker.list_of_review_pages[0]}")

def main():
    # Modify company_code, company_name and account_number (see accounts.json)

    # e.g., for Visa - https://www.glassdoor.sg/Overview/Working-at-Visa-Inc-EI_IE3035.11,19.htm
    # e.g., Company_name = Visa, Company_code = 3035
    company_code = 12830
    company_name = "VMware"

    # Will be resolved to Facebook_{account_number} in accounts.json. 
    account_number = 2

    # Will scrape 100 urls (10 reviews per url) before dumping results to json
    batch_size = 100 

    worker = create_worker(company_code, company_name, account_number)
    worker.generate_urls()

    print(f"Starting to scrape {company_name} in batches of {batch_size} urls.")
    # resume_work(worker) is used for scrapes that prematurely terminated
    # resume_work(worker) # uncomment this line to resume a scrape that failed halfway
    start_worker(worker, batch_size)

if __name__ == "__main__":
  main()
