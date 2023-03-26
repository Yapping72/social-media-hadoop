from selenium import webdriver
from abc import ABC, abstractmethod
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import os 
import requests


CHROME_DRIVER_PATH = os.path.join(".","chromedriver_v110.0.5481.77", "chromedriver.exe")
FIREFOX_DRIVER_PATH = os.path.join(".","geckodriver_v0.32.0", "geckodriver.exe")
FIREFOX_BROSWER = r"C:\Program Files\Mozilla Firefox\firefox.exe"

class WebDriver(ABC):
    @abstractmethod
    def __init__(self, webpage:str):
        self.webpage = webpage
    
    def navigate_to(self, url:str):
        self.driver.get(url)
        
    def get_driver(self):
        return self.driver

    def find_element(self, by, value):
        return self.driver.find_element(by, value)
    
    def getWindowHandles(self):
        return self.driver.window_handles

    def switch_to_window(self, window):
        return self.driver.switch_to.window(window)
    
    def find_element_by_id(self, id):
        return self.driver.find_element_by_id(id)

    def find_element_by_xpath(self, xpath):
        return self.driver.find_element(By.XPATH, xpath)

    def get_current_url(self):
        return self.driver.current_url
    
    def get_html_source(self):
        return self.driver.page_source
        
    def close(self):
        self.driver.close()

class ChromeWebDriver(WebDriver):
    def __init__(self):
        self.webpage = "chrome://newtab"
        super().__init__(self.webpage)
        # Web driver for google chrome located in CHROME_DRIVER_PATH
        self.set_options()
        self.driver = webdriver.Chrome(CHROME_DRIVER_PATH, options= self.options)
        self.driver.get(self.webpage)
    
    def set_options(self):
        self.options =  webdriver.ChromeOptions()
        self.options.add_argument('--disable-blink-features=AutomationControlled')
        self.options.add_argument('--disable-features=SafeBrowsingEnhancedProtection')
        self.options.add_argument('--blink-settings=imagesEnabled=false')
        self.options.add_argument('--blink-settings=videoEnabled=false')
        self.options.add_experimental_option('excludeSwitches', ['enable-logging']) # to remove usb_device_handle_win logging message

class FireFoxWebDriver(WebDriver):
    def __init__(self):
        self.webpage = "about:home"
        super().__init__(self.webpage)
        self.set_options()
        # Web driver for firefox (geckodriver) located in FIREFOX_DRIVER_PATH
        #absolute path firefox.exe
        self.driver = webdriver.Firefox(executable_path = FIREFOX_DRIVER_PATH, options=self.options)
        self.driver.get(self.webpage)

    def set_options(self):
        self.options = Options()
        self.options.binary_location = FIREFOX_BROSWER
        self.options.set_preference("dom.webdriver.enabled", False)
        self.options.set_preference("useAutomationExtension", False)
        self.options.set_preference("privacy.trackingprotection.enabled", False)
        self.options.set_preference("network.cookie.cookieBehavior", 1)
        self.options.set_preference("intl.accept_languages", "en-US,en")
        self.options.binary_location = FIREFOX_BROSWER  