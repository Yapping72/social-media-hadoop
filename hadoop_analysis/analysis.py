import json
import os
import re
import pandas as pd 
import sys
import string
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords

def get_industry_directories():
    """Returns list of file paths to each industry i.e., data\Materials
        Use to easily re-run all analysis """
    industry_list = os.listdir(DATA_DIRECTORY)
    industry_directory = []
    for industry in industry_list:
        industry_path  = os.path.join(DATA_DIRECTORY, industry)
        industry_directory.append(industry_path)
    return industry_directory

def get_companies_from_industry(one_industry_directory_path:str):
    """Returns the list of files paths of each company in the each industry folder 
    e.g.., ..\data\Materials\Air-Liquide"""
    company_path_list = []
    try: 
        for company in os.listdir(one_industry_directory_path):
            company_folder = os.path.join(one_industry_directory_path, company)
            company_path_list.append(company_folder)
    except FileNotFoundError:
        print(f"Error: Directory '{one_industry_directory_path}' does not exists. Exiting.")
        print("Check that you specified the correct INDUSTRY in main.py and you are in the correct directory (social-media-hadoop\hadoop_analysis)")
        sys.exit(1)

    return company_path_list

def get_reviews_in_json(a_company_path:str):
    """Returns a list of paths to each json review for a company"""
    company_reviews_path_list = []
    for company_review in os.listdir(a_company_path):
        company_review_json_path = os.path.join(a_company_path, company_review)
        company_reviews_path_list.append(company_review_json_path)
    
     # Sort the list of file names based on the last number following the company name
    company_reviews_path_list = sorted(company_reviews_path_list, key=lambda x: int(re.findall(r'\d+', x)[-1]))
    return company_reviews_path_list

def get_company_name(file_path):
    """Regex expression to obtain company name from file"""
    pattern = r"^[^-]+-(.+?)-\d+\.json$"
    match = re.match(pattern, file_path)

    if match:
        company_name = match.group(1)
        return company_name
    else:
        print("No match")

def load_all_reviews_into_dataframe(json_review):
    """Loads all reviews in json into 1 data frame"""
    with open(json_review, "r") as f:
        review_data = json.load(f)
        [company_reviews.append(review) for review in review_data]

def log_invalid_jsons(error_message, industry):
    """Saves invalid jsons to ./json_parse_errors"""
    destination_directory = os.path.join(".", "json_parse_errors")
    if not os.path.exists(destination_directory):
        os.makedirs(destination_directory)
    
    error_log_file = os.path.join(destination_directory, f"{industry}_json_parsing_errors.txt")
    with open(error_log_file, 'a') as f:
        f.write(error_message + '\n')

def process_company_reviews(company, all_data, industry):
    """Loads all reviews for each industry into 1 pandas dataframe"""
    company_reviews = []
    all_json_reviews_for_company = get_reviews_in_json(company)

    for num_json, json_review in enumerate(all_json_reviews_for_company):
        # Read json data and add to pandas dataframe
        with open(json_review, "r") as f:
            try:
                review_data = json.load(f)
                [company_reviews.append(review) for review in review_data]
            except json.JSONDecodeError as e:
                error_message = f"Error loading {json_review}, {e}"
                print(error_message)
                print("Check json_parse_folders directory to find problematic json files")
                log_invalid_jsons(error_message, industry)
                continue

        if num_json == len(all_json_reviews_for_company) - 1:
            # Concatenate all the review data for the company into a single DataFrame
            company_df = pd.concat([pd.DataFrame(review) for review in company_reviews], ignore_index=True)
            # Add a column to the DataFrame with the company name
            company_df["company"] = get_company_name(os.path.basename(json_review))
            # Append the company DataFrame to the list of all data
            all_data.append(company_df)
            print(f"Loaded {num_json + 1} JSON files for {get_company_name(os.path.basename(json_review))}.")

    return all_data

def companies_in_dataframe(all_data_df):
    """Returns a list of companies present in the data frame"""
    unique_companies = all_data_df['company'].unique()
    return unique_companies

def create_review_text(all_data_df):
    """Creates a review text that comprises review_title, pros and cons, convert all to lowercase (for word cloud)"""
    all_data_df['review_text'] = all_data_df['review_title'] + ' ' + all_data_df['pros'] + ' ' + all_data_df['cons']
    all_data_df['review_text'] = all_data_df['review_text'].apply(lambda x: x.lower())
    
def obtain_median_reviews(company_reviews):
    """
    Returns the median rating of the company_reviews DataFrame.
    Skips rows with 'N/A' values in the 'rating' column.
    """
    filtered_reviews = company_reviews[company_reviews['rating'] != 'N/A']
    median_rating = filtered_reviews['rating'].median()
    return median_rating

def count_star_reviews(company_reviews, star_rating:str):
    """Returns the number of reviews with a given star rating"""
    count = len(company_reviews[company_reviews['rating'] == star_rating])
    return count

def create_company_dict(company_name):
    company_dict = {
        "name": company_name,
        "total_reviews": 0,
        "median_reviews": 0,
        "five_star_reviews": 0,
        "four_star_reviews": 0,
        "three_star_reviews": 0,
        "two_star_reviews": 0,
        "one_star_reviews": 0,
        "percent_five_star": 0,
        "percent_four_star": 0,
        "percent_three_star": 0,
        "percent_two_star": 0,
        "percent_one_star": 0,
        "word_count_dictionary": {},
    }
    return company_dict

def populate_company_dictionary(company_name:str, company_reviews:pd.DataFrame):
    """Populates the company dictionary with number of reviews"""
    company_dictionary = create_company_dict(company_name)
    # Obtain total reviews 
    company_dictionary['total_reviews'] = company_reviews.shape[0]
    # Obtain Median Reviews
    company_dictionary['median_reviews'] = obtain_median_reviews(company_reviews)
    # Obtain Number of 1-star to 5-star reviews
    company_dictionary['five_star_reviews'] = count_star_reviews(company_reviews, "5.0")
    company_dictionary['four_star_reviews'] = count_star_reviews(company_reviews, "4.0")
    company_dictionary['three_star_reviews'] = count_star_reviews(company_reviews, "3.0")
    company_dictionary['two_star_reviews'] = count_star_reviews(company_reviews, "2.0")
    company_dictionary['one_star_reviews'] = count_star_reviews(company_reviews, "1.0")
    # Obtain percentages of X-starred reviews
    get_percentage_of_reviews(company_dictionary)
    return company_dictionary

def get_percentage_of_reviews(company_dictionary):
    # Calculate percentage of X-starred reviews (rounded to 3 dp)
    company_dictionary["percent_five_star"] = round(company_dictionary["five_star_reviews"] / company_dictionary["total_reviews"] * 100, 3)
    company_dictionary["percent_four_star"] = round(company_dictionary["four_star_reviews"] / company_dictionary["total_reviews"] * 100, 3)
    company_dictionary["percent_three_star"] = round(company_dictionary["three_star_reviews"] / company_dictionary["total_reviews"] * 100, 3)
    company_dictionary["percent_two_star"] = round(company_dictionary["two_star_reviews"] / company_dictionary["total_reviews"] * 100, 3)
    company_dictionary["percent_one_star"] = round(company_dictionary["one_star_reviews"] / company_dictionary["total_reviews"] * 100, 3)

def get_word_count_dictionary(review_text:pd.Series):
    word_count_dictionary = {}
    for review in review_text:
        # Split a review into words
        words = review.split()

        # remove punctuation from words
        words = [word.strip(string.punctuation) for word in words]

        # Count the occurrence each word
        for word in words:
            word_count_dictionary[word] = word_count_dictionary.get(word, 0) + 1

    return word_count_dictionary

def remove_stop_words(word_count_dictionary):
    stop_words = set(stopwords.words('english'))
    words_to_remove = [word for word in word_count_dictionary.keys() if word in stop_words or word == ""]
    for word in words_to_remove:
        del word_count_dictionary[word]
    
def keep_first_n_keys(word_count_dictionary, n):
    return dict(list(word_count_dictionary.items())[:n])

def update_company_word_count_dictionary(company_dictionary, company_reviews: pd.DataFrame):
    # Get word count dictionary for all reviews in the company
    word_count_dict = get_word_count_dictionary(company_reviews['review_text'])
    # Add the word count dictionary to the company dictionary
    company_dictionary["word_count_dictionary"].update(word_count_dict)
    # Sort the word count dictionary by count, from highest to lowest
    company_dictionary["word_count_dictionary"] = dict(sorted(company_dictionary["word_count_dictionary"].items(), key=lambda item: item[1], reverse=True))
    # Remove stop words from the word count dictionary
    stop_words = set(stopwords.words('english'))
    words_to_remove = [word for word in company_dictionary["word_count_dictionary"].keys() if word in stop_words or word == ""]
    for word in words_to_remove:
        del company_dictionary["word_count_dictionary"][word]
    # Keep only the first 20 keys in the word count dictionary
    company_dictionary["word_count_dictionary"] = keep_first_n_keys(company_dictionary["word_count_dictionary"], 20)

def dump_dictionary_to_json(INDUSTRY, company_dictionary):
    # Saves dictionary to Results folder 
    destination_directory = os.path.join(".", "Results")
    if not os.path.exists(destination_directory):
        os.makedirs(destination_directory)
    
    # Use company name as the key to the company dictionary
    # Pop off the 'company' key and add it as the new key
    company_key = company_dictionary["name"]
    new_company_dict = {company_key: company_dictionary}

    # Load existing JSON data if it exists
    destination_file = os.path.join(destination_directory, f"{INDUSTRY}.json")
    if os.path.exists(destination_file):
        with open(destination_file) as f:
            existing_data = json.load(f)
        existing_data.update(new_company_dict)
    else:
        existing_data = new_company_dict

    # Write new data to JSON file
    with open(destination_file, "w") as f:
        json.dump(existing_data, f)

def get_individual_companies(all_data_df: pd.DataFrame):
    # Get list of companies successfully loaded from json into dataframe
    companies = companies_in_dataframe(all_data_df)
    # Iterate through each companies dataframe to obtain - median reviews, average reviews, num X-star and word-count
    for company in companies:
        # Slice the dataframe into manageable chunks
        company_df = all_data_df.groupby('company')
        company_reviews = company_df.get_group(company) 
        # Populates dictionary with total, median, number of X-starred % of X-starred reviews
        company_dictionary = populate_company_dictionary(company, company_reviews)
        dump_dictionary_to_json(INDUSTRY, company_dictionary)
        update_company_word_count_dictionary(company_dictionary, company_reviews)
        dump_dictionary_to_json(INDUSTRY, company_dictionary)
        print(f"Completed analysis on {company} reviews")

def get_industry_overview(all_data_df: pd.DataFrame):
    # Populates dictionary with total, median, number of X-starred % of X-starred reviews
    industry_dictionary = populate_company_dictionary(INDUSTRY, all_data_df)
    dump_dictionary_to_json(INDUSTRY, industry_dictionary)
    update_company_word_count_dictionary(industry_dictionary, all_data_df)
    dump_dictionary_to_json(INDUSTRY, industry_dictionary)
    print(f"Completed analysis on {INDUSTRY} reviews")

DATA_DIRECTORY = os.path.join("..", "data") 
INDUSTRY = "Materials" # <-- Modify this 

def main():
    """Iterates through all the ..\data\INDUSTRY directories to get company reviews."""
    industry_directory = os.path.join(DATA_DIRECTORY, INDUSTRY) 
    companies_in_industry = get_companies_from_industry(industry_directory)
    all_data = [] # stores all the json reviews for all countries in the specified industry
    
    for company in companies_in_industry:
        # Extract and store all json reviews for a company into one dataframe
        all_data = process_company_reviews(company, all_data, INDUSTRY)

    # Merge the dataframe, and create a new column that combines review title, pros and cons
    all_data_df = pd.concat(all_data, ignore_index= True)
    create_review_text(all_data_df)
    all_data_df = all_data_df.drop_duplicates()
    get_industry_overview(all_data_df)
    get_individual_companies(all_data_df)
    
if __name__ == "__main__":
  main()
