# Python Analysis Script

## Usage
1. After using the GlassDoor Scraper, the group the data/company/company.json files into their respective industries.
* Current repository uses the 11 Global Industry Classification Standard (GICS) to classify companies.
2. Modify the INDUSTRY variable in **analysis.py**.
3. Analysis.py will iterate over all company files, and will return Results/industry.json. This JSON will contain an overview of all companies and review information of each company. It will also combine word-count and review-counts from hadoop analysis. 

### Failure to load company
A small percentage of companies (4 out of 182) were observed to have invalid JSON files. You can view the list of JSON files that failed to load in the json_parse_errors.txt. Use https://jsonlint.com/ to determine cause. Can typically be resolved by removing the faulty lines and replacing it with a comma. 
