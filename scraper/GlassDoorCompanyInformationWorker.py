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

MISCELLANOUS_DIRECTORY = os.path.join(".", "miscellanous")
DATA_DIRECTORY = os.path.join("..", "data")

DESTINATION_DIRECTORY = os.path.join(DATA_DIRECTORY, "Company Information")

class GlassDoorCompanyInformationWorker:
    def __init__(self, company_code, company_name, account_number):
        self.company_code = company_code
        self.company_name = company_name
        self.account_number = account_number
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

    def scrape_company_information(self, company_code, company_name):
        """ Start scraping for company information"""
        self.company_code = self.worker.company_code = company_code
        self.company_name = self.worker.company_name = company_name
        return self.worker._get_company_information()

    def scrape_multiple_companies(self, file_path): 
        """Scrapes company information provided in file_path"""
        company_list = self.get_company_codes_and_names(file_path)
        for index, (company_name, company_code) in enumerate(company_list):
            print(f"Company {index} of {len(company_list)}: ", end="")
            company_information_dictionary = self.scrape_company_information(company_code = company_code, company_name = company_name)
            self.dump_dictionary_to_json(company_information_dictionary)

    def get_company_codes_and_names(self, file_path):
        """ Obtain the list of company_codes and names from a .json file"""
        source = file_path
        company_code_and_name_list = []
        try:
            with open(source) as f:
                data = json.load(f)
                company_code_and_name_list.extend({(d['company_name'], d['company_code']) for d in data.values()})
        except FileNotFoundError:
            print(f"Error opening {source}, please check if it exists.")
            print("Please ensure you are in social-media-hadoop\scraper directory.")

        return company_code_and_name_list

    def dump_dictionary_to_json(self, company_dictionary):    
        """Dumps dictionary to json file ..\data\Company Information\Company_information"""
        # Saves dictionary to ..\data\Company Information\Company_information
        if not os.path.exists(DESTINATION_DIRECTORY):
            os.makedirs(DESTINATION_DIRECTORY)
        
        # Use company name as the key to the company dictionary
        # Pop off the 'company' key and add it as the new key
        company_key = company_dictionary["company_name"]
        new_company_dict = {company_key: company_dictionary}

        # Load existing JSON data if it exists
        destination_file = os.path.join(DESTINATION_DIRECTORY, f"Company_Information.json")
        if os.path.exists(destination_file):
            with open(destination_file, "r", encoding = "utf-8") as f:
                existing_data = json.load(f)
            existing_data.update(new_company_dict)
        else:
            existing_data = new_company_dict
        
        # Write new data to JSON file
        with open(destination_file, "w", encoding = "utf-8") as f:
            json.dump(existing_data, f)
    
def main():
    # TODO: Modify GlassDoorScraper() such that it can be instantiated without code and name
    company_code = 158708
    company_name = "Nanyang-Technological-University"

    # Will be resolved to Facebook_{account_number} in accounts.json. 
    account_number = 2

    # Create worker object and start scraping for company information
    worker = GlassDoorCompanyInformationWorker(company_code, company_name, account_number)
    worker.scrape_multiple_companies("./Industries/Health_care.json") 

if __name__ == "__main__":
        main()