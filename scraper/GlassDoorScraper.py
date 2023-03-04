from GenericScraper import ChromeWebScraper
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
import pyperclip as pc
import time
import json

GLASSDOOR_WEBSITE = "https://www.glassdoor.sg/index.htm"

class GlassDoorScraper:
    def __init__(self, scraper):
        self.webpage = GLASSDOOR_WEBSITE
        self.driver = scraper
        self.driver.navigate_to(self.webpage)

    def setAccountInformation(self, account_type):
        # Load JSON data from file
        with open('accounts.json', 'r') as f:
            data = json.load(f)
            self.username = data[account_type]['username']
            self.password = data[account_type]['password']
    
    def loginUsingFacebook(self):
        self.setAccountInformation(account_type="Facebook")
        # Log in to Glassdoor via facebook 
        print("Clicking Sign in with Facebook button")
        facebook_login_button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@data-test='facebookBtn']")))
        facebook_login_button.click()

        # Switch to the pop-up window
        window_handles = self.driver.getWindowHandles()
        print(window_handles)
        self.driver.switch_to_window(window_handles[1])

        # Type in email and password
        email_field = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@id='email']")))
        email_field.send_keys(self.username)
        
        password_field = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//input[@id="pass"]')))
        password_field.send_keys(self.password)
        
        login_button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="loginbutton"]')))
        login_button.click()

    def loginUsingGoogle(self):
        """Note google authentication often will block login attempts"""
        self.setAccountInformation("Google")
        # Log in to Glassdoor
        print("Clicking Sign in with Google button")
        google_login_button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(@class, "google") and contains(@data-test, "googleBtn")]')))
        google_login_button.click()

        # Switch to the pop-up window
        window_handles = self.driver.getWindowHandles()
        self.driver.switch_to_window(window_handles[1])

        # Input email and click next
        email_field = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@type='email']")))
        email_field.send_keys(self.username)

        next_button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[@type="button"]/span[text()="Next"]')))
        next_button.click()
        
        """
        # Click try again prompt 
        try_again_button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="next"]/div/button/span')))
        try_again_button.click()
        """ 

        # Input password
        password_input = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//input[@type="password"]')))
        password_input.send_keys(self.password)
        password_input.send_keys(Keys.RETURN)
    
    def get_reviews(self):
        # Find and click the search bar
        search_bar = self.driver.find_element_by_id("sc.keyword")
        search_bar.send_keys("company name") # Replace with the name of the company you want to search for
        search_bar.send_keys(Keys.RETURN)

        # Wait for the search results to load
        wait = WebDriverWait(self.driver, 10)
        results = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "react-job-listing")))

        # Click the first result to go to the company page
        first_result = results.find_element_by_tag_name("a")
        first_result.click()

        # Find and click the "Reviews" tab
        reviews_tab = self.driver.find_element_by_xpath("//a[@href='#reviews']")
        reviews_tab.click()

        # Wait for the reviews to load
        reviews = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='cell reviewBodyCell']")))

        # Scrape the reviews
        review_elements = reviews.find_elements_by_xpath(".//p[@class='mt-0 mb-0 ']")
        for review in review_elements:
            print(review.text)
