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
import json 

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
            print(f"Failed to scrape: {url} view error_logs for list of failed urls.")
            worker.dump_scrape_error_log(url)

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
    print(f"Resuming {worker.company_name} Batch: #{worker.batch_counter}\nResume from url: {worker.list_of_review_pages[0]}")

def start_multiple_scrapes(account_number, batch_size, file_path):
    """Scrapes multiple companies for reviews."""
    # Read json containing company codes and list
    with open(file_path) as f:
        json_data = json.load(f)

    # Extract code and name
    for company in json_data:
        company_info = json_data[company]
        company_code = company_info['company_code']
        company_name = company_info['company_name']
        start_one_scrape(company_code, company_name, account_number, batch_size)

def start_one_scrape(company_code, company_name, account_number, batch_size):
    """ Scrape one company for reviews """
    worker = create_worker(company_code, company_name, account_number)
    worker.generate_urls()

    print(f"Starting to scrape {company_name} in batches of {batch_size} urls.")
    start_worker(worker, batch_size)
    print(f"{worker.username}: Completed scrape on {worker.company_name}")

def resume_scrape(company_code, company_name, account_number, batch_size):
    """Resumes a scrape from the last completed batch"""

    worker = create_worker(company_code, company_name, account_number)
    worker.generate_urls()

    print(f"Starting to scrape {company_name} in batches of {batch_size} urls.")
    # resume_work(worker) is used for scrapes that prematurely terminated
    resume_work(worker) 
    start_worker(worker, batch_size)
    print(f"{worker.username}: Completed scrape on {worker.company_name}")

def main():
    # Modify company_code, company_name and account_number (see accounts.json)
    
    # e.g., for Visa - https://www.glassdoor.sg/Overview/Working-at-Visa-Inc-EI_IE3035.11,19.htm
    # e.g., Company_name = Visa, Company_code = 3035
    company_code = 9304
    company_name = "Huawei"

    # Will be resolved to Facebook_{account_number} in accounts.json. 
    account_number = 2

    # will scrape 100 urls (10 reviews per url) before dumping results to json
    batch_size = 100 

    """Uncomment if you intend to scrape only 1 company"""
    # start_one_scrape(company_code, company_name, account_number, batch_size) # Starts scraping company for reviews
    
    """Uncomment if you intend to resume a scrape for a company"""
    resume_scrape(company_code, company_name, account_number, batch_size) # Resumes a prematurely terminated scrape
    
    """Uncomment if you intend to Scrape multiple companies (listed in company_list_1.json)"""
    # FILE_PATH = "company_list_2.json"
    # start_multiple_scrapes(account_number, batch_size, FILE_PATH)

if __name__ == "__main__":
  main()
