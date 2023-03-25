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

class GlassDoorReviewWorker:
    def __init__(self, company_code, company_name, account_number, batch_size):
        self.company_code = company_code
        self.company_name = company_name
        self.account_number = account_number
        self.batch_size = batch_size
        self.list_of_review_pages = []
        self.reviews_collected = []
        self.batch_counter = 0
        self.worker = self.create_worker() # Aggregation

    def create_worker(self):
        """Creates 1 worker, that will be used to scrape glassdoor"""
        account_type = f"Facebook_{self.account_number}"
        try:
            worker = GlassDoorScraper(driver=ChromeWebDriver(), company_code=self.company_code, company_name=self.company_name)
            worker.login_using_facebook(account_type=account_type)
        except InvalidSessionIdException:
            print(f"Failed to login using {account_type} - Blocked by captcha.")
            sys.exit(1)
        return worker

    def start_worker(self):
        """Override this to invoke other types of scrapes e.g., Company information"""
        start_time = time.time()
        while self.list_of_review_pages:
            url = self.list_of_review_pages.pop(0)
            try:
                review_elements = self.worker._get_reviews_on_page(url)
                reviews = self.worker._extract_reviews(review_elements)
                self.reviews_collected.append(reviews)
                if (len(self.reviews_collected) == self.batch_size) or (len(self.list_of_review_pages) == 0):
                    self.worker.dump_reviews_json(self.reviews_collected)
                    self.reviews_collected.clear()
                    end_time = time.time()
                    elapsed_time = end_time - start_time # stop timer
                    print(f"Batch of {self.batch_size} urls scrapped. Time Elapsed: {elapsed_time}")
                    start_time = end_time # reset timer
            except Exception as e:
                print(f"Failed to scrape: {url} view error_logs for list of failed urls.")
                self.worker.dump_scrape_error_log(url)

    def resume_work(self):
        """For jobs that were prematurely terminated, can invoke this to resume scraping 
            at the i'th URL. 
        """
        folder_path = os.path.join("..", "data", f"{self.company_name}")
        if os.path.exists(folder_path): # Get number of previously scrapped reviews
            num_json_files = len([f for f in os.listdir(folder_path) if f.endswith('.json')])
        else: # included such that resume_work wont cause script to break if left uncommented.
            num_json_files = 0
        new_index = num_json_files * 100
        self.list_of_review_pages = self.list_of_review_pages[new_index:]
        self.batch_counter = num_json_files
        print(f"Resuming {self.company_name} Batch: #{self.batch_counter}\nResume from url: {self.list_of_review_pages[0]}")

    def generate_urls(self):
        """Generates a list of urls to scrape"""
        self.list_of_review_pages = self.worker.generate_reviews_urls()

    def start_one_scrape(self):
        """ Scrape one company for reviews """
        self.generate_urls()
        print(f"Starting to scrape {self.company_name} in batches of {self.batch_size} urls.")
        self.start_worker()
        print(f"{self.worker.username}: Completed scrape on {self.worker.company_name}")

    def resume_scrape(self):
        """Resumes a scrape from the last completed batch"""
        self.generate_urls()
        print(f"Starting to scrape {self.company_name} in batches of {self.batch_size} urls.")
        self.resume_work()
        self.start_worker()
        print(f"{self.worker.username}: Completed scrape on {self.worker.company_name}")
    
    def start_multiple_scrapes(self, file_path):
        """Scrapes multiple companies for reviews."""
        # Read json containing company codes and list
        try:
            with open(file_path) as f:
                json_data = json.load(f)
                # Extract code and name
                for company in json_data:
                    company_info = json_data[company]
                    self.company_code = company_info['company_code']
                    self.company_name = company_info['company_name']
                    self.worker.company_code = self.company_code
                    self.worker.company_name = self.company_name
                    self.batch_counter = 0
                    self.start_one_scrape()

        except FileNotFoundError:
            print(f"Error: {file_path} provided does not exists. Exiting.")
            print("Please ensure that your are in the social-media-hadoop\scraper directory")
            sys.exit(1)

     
