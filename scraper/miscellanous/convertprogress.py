import json

# initialize empty dictionary to hold company data
data = {}

# initialize empty list to hold company dictionaries
companies = []

# open progress.md file in read mode
with open('progress.md', 'r') as f:
    
    # loop through each line in the file
    for line in f.readlines():
        
        # check if the line starts with '###'
        if line.startswith('###'):
            
            # check if companies list is not empty
            if companies:
                
                # get the last company dictionary from the list
                company_data = companies[-1]
                
                # check if each required field is present in the dictionary, and add empty values if not
                if 'company_name' not in company_data:
                    company_data['company_name'] = ''
                if 'company_code' not in company_data:
                    company_data['company_code'] = ''
                if 'reviews_url' not in company_data:
                    company_data['reviews_url'] = ''
                if 'reviews_on_glassdoor' not in company_data:
                    company_data['reviews_on_glassdoor'] = ''
                if 'actual_reviews_collected' not in company_data:
                    company_data['actual_reviews_collected'] = ''
                if 'coverage' not in company_data:
                    company_data['coverage'] = ''
                
                # add company dictionary to the data dictionary with company_name as key
                data[company_data['company_name']] = company_data
            
            # add a new empty company dictionary to the companies list
            companies.append({})
            
            # add company name to the new dictionary
            companies[-1]['company_name'] = line.split('### ')[1].strip()
        
        # check if the line starts with '- Company Name:'
        elif line.startswith('- Company Name:'):
            
            # update company name in the last dictionary in the companies list
            companies[-1]['company_name'] = line.split(': ')[1].strip()
        
        # check if the line starts with '- Company Code:'
        elif line.startswith('- Company code:' ) or line.startswith( '- Company Code:'):
            
            # update company code in the last dictionary in the companies list
            companies[-1]['company_code'] = int(line.split(': ')[1].strip())
    
        # check if the line contains 'reviews in'
        elif 'reviews in' in line:
            
            # split the line to get the reviews url and the number of reviews
            reviews_info = line.split(' reviews in ')
            
            # update reviews_url in the last dictionary in the companies list
            companies[-1]['reviews_url'] = int(reviews_info[1].strip().split(' ')[0])
            
            # if the number of reviews scraped is not separated from the rest of the line
            if '-' in reviews_info[0]:
                
                # update reviews_on_glassdoor in the last dictionary in the companies list
                companies[-1]['reviews_on_glassdoor'] = int(reviews_info[0].split('-')[1].strip())
            
            # otherwise
            else:
                
                # update reviews_on_glassdoor in the last dictionary in the companies list
                companies[-1]['reviews_on_glassdoor'] = int(reviews_info[0].strip())
            
            # calculate actual_reviews_collected and coverage and update in the last dictionary in the companies list
            companies[-1]['actual_reviews_collected'] = ""

    if companies:
        company_data = companies[-1]
       # If the company name is not in the data, set it to an empty string
if 'company_name' not in company_data:
    company_data['company_name'] = ''

# If the company code is not in the data, set it to an empty string
if 'company_code' not in company_data:
    company_data['company_code'] = ''

# If the reviews URL is not in the data, set it to an empty string
if 'reviews_url' not in company_data:
    company_data['reviews_url'] = ''

# If the number of reviews on Glassdoor is not in the data, set it to an empty string
if 'reviews_on_glassdoor' not in company_data:
    company_data['reviews_on_glassdoor'] = ''

# If the number of actual reviews collected is not in the data, set it to an empty string
if 'actual_reviews_collected' not in company_data:
    company_data['actual_reviews_collected'] = ''

# If the coverage percentage is not in the data, set it to an empty string
if 'coverage' not in company_data:
    company_data['coverage'] = ''

# Add the company data to the dictionary using the company name as the key
data[company_data['company_name']] = company_data
with open('progress.json', 'w') as outfile:
    json.dump(data, outfile, indent=4)
