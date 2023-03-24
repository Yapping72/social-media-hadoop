import json
import os
import re
import pandas as pd 
import sys
DATA_DIRECTORY = os.path.join("..", "data")

def getIndustryDirectories():
    """Returns list of file paths to each industry i.e., data\Materials"""
    industry_list = os.listdir(DATA_DIRECTORY)
    industry_directory = []
    for industry in industry_list:
        industry_path  = os.path.join(DATA_DIRECTORY, industry)
        industry_directory.append(industry_path)
    return industry_directory

def getCompaniesInIndustry(one_industry_directory_path:str):
    """Returns the list of files paths of each company in the each industry folder 
    e.g.., ..\data\Materials\Air-Liquide"""
    company_path_list = []
    for company in os.listdir(one_industry_directory_path):
        company_folder = os.path.join(one_industry_directory_path, company)
        company_path_list.append(company_folder)
    return company_path_list

def getReviewsJson(a_company_path:str):
    """Retruns the list of paths to each json review for a company"""
    company_reviews_path_list = []
    for company_review in os.listdir(a_company_path):
        company_review_json_path = os.path.join(a_company_path, company_review)
        company_reviews_path_list.append(company_review_json_path)
    return company_reviews_path_list

def getCompanyName(file_path):
    pattern = r"^[^-]+-(.+?)-\d+\.json$"
    match = re.match(pattern, file_path)

    if match:
        company_name = match.group(1)
        return company_name
    else:
        print("No match")

def loadAllReviewsIntoDataframe(json_review):
    with open(json_review, "r") as f:
        review_data = json.load(f)
        [company_reviews.append(review) for review in review_data]

def mergeJsonDataToDataframe():
    pass

def logInvalidJson(error_message):
    """Some json cannot be parsed figure out why."""
    with open('failed_json.txt', 'a') as f:
        f.write(error_message + '\n')

def process_company_reviews(company, all_data):
    """Loads all reviews for each industry into 1 pandas dataframe"""
    company_reviews = []
    all_json_reviews_for_company = getReviewsJson(company)

    for num_json, json_review in enumerate(all_json_reviews_for_company):
        """Read json data and add to pandas dataframe"""
        with open(json_review, "r") as f:
            try:
                review_data = json.load(f)
                [company_reviews.append(review) for review in review_data]
            except json.JSONDecodeError as e:
                error_message = f"Error loading {json_review}, {e}"
                print(error_message)
                logInvalidJson(error_message)
                continue

        if num_json == len(all_json_reviews_for_company) - 1:
            # Concatenate all the review data for the company into a single DataFrame
            company_df = pd.concat([pd.DataFrame(review) for review in company_reviews], ignore_index=True)
            # Add a column to the DataFrame with the company name
            company_df["company"] = getCompanyName(os.path.basename(json_review))
            # Append the company DataFrame to the list of all data
            all_data.append(company_df)
            print(f"Successfully loaded {getCompanyName(os.path.basename(json_review))} into data frame")

    return all_data

def companiesInDataframe(all_data_df):
    unique_companies = all_data_df['company'].unique()
    return unique_companies

def main():
    a_industry_directory = os.path.join(DATA_DIRECTORY, "Finances")
    companies_in_industry = getCompaniesInIndustry(a_industry_directory)
    all_data = []
    
    for company in companies_in_industry:
        all_data = process_company_reviews(company, all_data)

    all_data_df = pd.concat(all_data, ignore_index= True)
    companiesInDataframe(all_data_df)
    

if __name__ == "__main__":
  main()
