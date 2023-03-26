import json 
import os

COMPANY_INFORMATION_FILE= os.path.join("..", "data", "Company Information", "Company_Information.json")

def check_company_information(company, file):
    """Loads COMPANY_INFORMATION_FILE to verify one company dictionary"""
    try:
        with open(file, "r", encoding = "utf-8") as f:
            data = json.load(f)
            print(data[company])
    except FileNotFoundError:
        print(f"Error: {file} does not exists. Check that you are in social-media-haddop\hadoop_analysis folder.")
    except KeyError:
        print(f"Error: Company \'{company}\' not found in {file}")

check_company_information("MondelÄ“z-International", COMPANY_INFORMATION_FILE)