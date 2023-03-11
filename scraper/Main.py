from GenericDriver import FireFoxWebDriver
from GenericDriver import ChromeWebDriver
from GlassDoorScraper import GlassDoorScraper

from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import pyperclip as pc #send_keys sends strings line by line, faster to copy from clipboard
import sys 
import time 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from bs4 import BeautifulSoup
import asyncio
import numpy as np 

def create_workers(num_workers, company_code, company_name):
    workers = []
    for i in range(num_workers):
        account_type = f"Facebook_{2}"
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

def divide_urls(list_of_urls, num_workers):
    """Divides list of urls into equal-sized chunks for workers"""
    url_chunks = np.array_split(list_of_urls, num_workers)
    return [chunk.tolist() for chunk in url_chunks]

def assign_urls(chunks, workers):   
    for i, worker in enumerate(workers):
        worker.list_of_urls = chunks[i]

"""
async def start_worker(worker, batch_size):
    while(worker.list_of_urls):
        url = worker.list_of_urls.pop(0)
        try:
            review_elements = worker._get_reviews_on_page(url)
            reviews = worker._extract_reviews(review_elements)
            worker.reviews_collected.append(reviews)
            if len(worker.reviews_collected) == batch_size:
                worker.dump_reviews_json(worker.reviews_collected)
                worker.reviews_collected.clear()
        except Exception as e:
            print(f"Error scraping reviews from {url}: {str(e)}")
"""

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
                print(f"{batch_size} review pages scrapped. Time Elapsed: {elapsed_time}")
                start_time = end_time # reset timer

        except Exception as e:
            print(f"Error scraping reviews from {url}: {str(e)}")


async def main():
    num_workers = 1
    #company_name = "Accenture"
    #company_code = 4138
    
    #company_name = "Meta"
    #company_code = 40772

    #company_name = "Shopee"
    #company_code = 1263091

    #company_name = "Micron"
    #company_code = 1648

    #company_name = "Google"
    #company_code = 9079

    #company_code = 1138
    #company_name = "Apple"
    
    company_code = 6036
    company_name = "Amazon"
    
    #company_code = 1737
    #company_name = "Oracle"

    #company_code = 11891
    #company_name = "Netflix"

    #company_code = 1651
    #company_name = "Microsoft"

    batch_size = 100

    workers = create_workers(num_workers, company_name = company_name, company_code = company_code)
    
    urls = workers[0].generate_urls()
    print(f"Starting to scrape {company_name} in batches of {batch_size}.")
    start_worker(workers[0], batch_size)
    """
    workers = create_workers(num_workers, company_name = company_name, company_code = company_code)
    urls = workers[0].generate_urls()

    chunks = divide_urls(urls, len(workers))
    assign_urls(chunks, workers)
    
    tasks = []
    for worker in workers:
        task = asyncio.create_task(start_worker(worker, batch_size))
        tasks.append(task)
        await asyncio.gather(*tasks)
    """
if __name__ == "__main__":
  asyncio.run(main())
