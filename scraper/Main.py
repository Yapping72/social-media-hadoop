from GenericScraper import FireFoxWebScraper
from GenericScraper import ChromeWebScraper
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


def main():
    chrome_scraper = ChromeWebScraper()
    company = "Accenture"
    code = "4138"
    Accenture = GlassDoorScraper(scraper = ChromeWebScraper(), company_code=code, company_name=company)
    Accenture.login_using_facebook()
    Accenture.generate_urls()
    Accenture.scrape_reviews()
    # TODO: start scraping the urls here - (asynchronously)

    """
    company = "Deloitte"
    code = "2763"
    Deloitte = GlassDoorScraper(scraper = ChromeWebScraper(), company_code=code, company_name=company)
    Deloitte.login_using_facebook()
    Deloitte.generate_urls()
     # TODO: start scraping the urls here - (asynchronously)
    """

if __name__ == "__main__":
    main()
