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


def main():
    chrome_scraper = ChromeWebScraper()
    glassdoor = GlassDoorScraper(chrome_scraper)

    #firefox_scraper = FireFoxWebScraper()
    #glassdoor = GlassDoorScraper(firefox_scraper)  
    #glassdoor.loginUsingGoogle()
    glassdoor.loginUsingFacebook()


if __name__ == "__main__":
    main()
