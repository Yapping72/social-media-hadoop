from GenericScraper import ChromeWebScraper
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select
import re
import pyperclip as pc
import time
import json
import requests
from bs4 import BeautifulSoup
import math
import concurrent.futures
import os

GLASSDOOR_WEBSITE = "https://www.glassdoor.sg/index.htm"

class GlassDoorScraper:
    def __init__(self, scraper, company_code, company_name):
        self.webpage = GLASSDOOR_WEBSITE
        self.driver = scraper
        self.driver.navigate_to(self.webpage)
        self.company_code = company_code
        self.company_name = company_name
        self.number_of_review_pages = 0
        self.reviews_count = 0
        self.list_of_review_pages = []

    def login_using_facebook(self):
        self._set_credentials(account_type="Facebook_2")
        # Log in to Glassdoor via facebook 
        print("Clicking Sign in with Facebook button")
        facebook_login_button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@data-test='facebookBtn']")))
        facebook_login_button.click()

        # Switch to the pop-up window
        window_handles = self.driver.getWindowHandles()
        self.driver.switch_to_window(window_handles[1])
        try:
            # Type in email and password
            email_field = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@id='email']")))
            email_field.send_keys(self.username)
            
            password_field = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//input[@id="pass"]')))
            password_field.send_keys(self.password)
            
            login_button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="loginbutton"]')))
            login_button.click()    
        except TimeoutException:
            print("Failed to find email, password or login button for facebook login")

        # Login success determined in original window contains 
        self.driver.switch_to_window(window_handles[0])
        self._is_login_successful()
    
    def generate_urls(self):
        url = f"https://www.glassdoor.sg/Reviews/{self.company_name}-Reviews-E{self.company_code}.htm"
        self.driver.navigate_to(url)
        self._count_pages_to_scrape(self.driver.get_current_url())
        self.list_of_review_pages.append(url)

        for page_num in range(2, self.number_of_review_pages):
            url = f"https://www.glassdoor.sg/Reviews/{self.company_name}-Reviews-E{self.company_code}_P{page_num}.htm?filter.iso3Language=eng"
            self.list_of_review_pages.append(url)


    def _set_credentials(self, account_type):
        # Load JSON data from file
        with open('accounts.json', 'r') as f:
            data = json.load(f)
            self.username = data[account_type]['username']
            self.password = data[account_type]['password']
    
    def _is_login_successful(self): 
        try:
            # Wait for the email address of the user to appear
            email_address_element = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//h3[contains(@class, 'css-17vthrg') and contains(@class, 'e11rhuha1')]")))
            # If the email address element is found, login was successful
            print("Login successful!")
            return True
        except TimeoutException:
            # If the email address element is not found, login failed
            print("Login failed!")
            self.driver.driver.close()
            return False

    def _count_pages_to_scrape(self, url):
        """Identify number of pages that need to be scrapped"""
        html_source = self.driver.get_html_source()
        soup = BeautifulSoup(html_source, "html.parser")
        reviews_count_str = soup.find('div', {'data-test': 'pagination-footer-text'}).text
        reviews_count = int(reviews_count_str.replace(',', '').split()[-2])
        self.reviews_count = reviews_count
        self.number_of_review_pages = math.ceil(reviews_count / 10) + 1
        print(f"Total reviews: {reviews_count} stored in {self.number_of_review_pages} pages")

    def _get_reviews_on_page(self, url):
        """ Retrieves the 10 reviews listed on a page"""
        # Navigate to a company's Glassdoor page
        self.driver.navigate_to(url)

        # Wait for the reviews to load
        reviews_section = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@id='ReviewsRef']")))

        # Get the HTML source of the reviews section
        reviews_html = reviews_section.get_attribute("innerHTML")

        # Parse the HTML using BeautifulSoup
        soup = BeautifulSoup(reviews_html, "html.parser")
    
        # Find the reviews feed element
        reviews_feed = soup.find("div", id="ReviewsFeed")
       
        # Find all review elements
        review_elements = reviews_feed.find_all("li", class_="empReview")
        return review_elements

    def _extract_reviews(self, review_elements):
        reviews = []   
        for review_element in review_elements:
            try:
                rating = review_element.find('span', class_='ratingNumber').text.strip()
            except: 
                rating = "N/A"
            try:
                reviewer_affiliation = review_element.find("span", class_="pt-xsm pt-md-0 css-1qxtz39 eg4psks0").text.strip()
            except:
                reviewer_affiliation = "N/A"
            try:
                job_title_text = review_element.find('span', class_='common__EiReviewDetailsStyle__newUiJobLine').span.text.replace('\xa0', ' ').strip()
                job_title_parts = job_title_text.split(' - ')
                job_date = job_title_parts[0]
                job_title = job_title_parts[1]
            except:
                job_date = "N/A"
                job_title = "N/A"
            try:
                duration = review_element.find('span', class_='cmp-reviewer-job-duration').text.strip()
            except:
                duration = "N/A"
            try:
                review_title = review_element.find('a', class_='reviewLink').text.strip()
            except:
                review_title = "N/A"
            try:
                pros = review_element.find('span', attrs={'data-test': 'pros'}).text.strip()
            except:
                pros = "N/A"
            try:
                cons = review_element.find('span', attrs={'data-test': 'cons'}).text.strip()
            except:
                cons = "N/A"
            review = {'review_title': review_title, 'rating': rating, 'reviewer_affiliation': reviewer_affiliation ,'job_date': job_date, 'job_title': job_title, 'duration': duration, 'pros': pros, 'cons': cons}
            reviews.append(review)
        return reviews
    
    def scrape_reviews(self):
        start_time = time.time()
        all_reviews = []

        for url in self.list_of_review_pages[:10]:
            review_elements = self._get_reviews_on_page(url)
            reviews = self._extract_reviews(review_elements)
            all_reviews.append(reviews)

        # Dump the reviews to a JSON file
        path = os.path.join("../data", f"{self.company_name}.json")
        self.dump_reviews_json(all_reviews, path)

        end_time = time.time()
        elapsed_time = end_time - start_time
        print(len(all_reviews))
        print(f"Elapsed time: {elapsed_time} seconds")
            
    def dump_reviews_json(self, reviews, file_path):
        """Dump the reviews to a JSON file"""
        with open(file_path, 'w') as file:
            json.dump(reviews, file)
 

    

        