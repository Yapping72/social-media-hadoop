# social-media-hadoop
A project for big data processing and analysis, focusing on Glassdoor reviews. Extracts reviews and company branding information from www.glassdoor.com. Performs analysis using Python and/or MapReduce. 
* Analysis was done in python to compare performance differences between Python and MapReduce.
* All analysis performed used MapReduce. Results from Hadoop analysis, was then processed in Python.
* Data visualized using Python-Flask Framework.

# Dependencies
<ol>
<li> pip install selenium
<li> pip install beautifulsoup4
<li> pip install numpy
</ol>

# General Guide for Scraping & Analysis Using Python
<ol>
<li> Ensure facebook accounts in accounts.json file is not banned and has completed glassdoor account setup. </li>
    <ul><li> Current implementation uses facebook login as it is not blocked for scraping </li> 
        <li> New facebook accounts have a 60-min delay before they can be used to create a glassdoor account. </li>
        <li> <strong> After glassdoor account registered to facebook account, follow their prompts to setup account, skipping the setup process will prevent scraping.</strong> </li>
    </ul>
<br>
<li> Replace the <strong> company code, company name and account_number </strong> in main.py. </li>
    <ul>
    <li> Company codes can be obtained from the reviews page.
        <ul> https://www.glassdoor.sg/Overview/Working-at-Accenture-EI_IE4138.11,20.htm 
        <li> company code = 4138, company name = Accenture </li> </ul>
    </ul>
<br>
<li> Run main.py it should open glassdoor website and attempt to login using account information provided in 'scraper/accounts.json' file. </li>
    <ul>
        <li>Chrome broswer should automatically open</li>
        <li>Automatic login via facebook <strong> Please solve captcha if it appears. </strong> </li>
        <li>On login success terminal should display login successful, and will automatically retrieve the list of urls to scrape and will begin scraping.
        <li>You will see the chrome browser traversing through each page and storing reviews.
        <li>Once 100 pages (~300-800 seconds) have been crawled, json containing reviews will be saved to the 'data/company_name' folder. Each json file will contain 1000 reviews.
        <li> /miscellanous/Progress.md is used to track companies that were scraped.
    </ul>
<br>
<li> Use GlassDoorCompanyInformationWorker.py to retrieve Company Information on previously scraped datasets.
    <ul>
    <li> Specify a json file that company code and company names, follow the same format used for multiple scrapes. (You can use the JSON files used for start_multiple_scrapes). 
    <li> Run GlassDoorCompanyInformationWorker.py, company information will be outputted ../data/Company Information/company_information.json.
    <li> Future work will integrate this part while scraping for companies reviews.
    </ul>
</ol>

# Scraping with Multiple Chrome Browsers
To scrape multiple companies in parallel, run multiple instance of main.py. Each instance should use a different facebook account. Scraping with multiple chrome browsers increases likelihood of captcha and Invalid session. Can safely run 3-4 chrome browswers without captcha occurinng frequently (depends on facebook account used).

# Scrapes that prematurely terminate before completion
To resume a scrape from the last successful batch, invoke the resume_scrape() instead of start_one_scrape().

# Sequential Scraping of a List of Companies
Create a json file and populate it with company_codes and company_names (see '../scraper/Industry/Financials' for example). Run the start_multiple_scrapes() instead of start_one_scrape(). You can also adopt the same approach to use multiple chrome sessions to scrape multiple companies in each session. Each instance of main.py will use a different company_list and facebook accounts. 
* Note that you may need to solve the captchas that appear on each login. Fresh glassdoor accounts less prone to Captcha verification on login.
* Modify the FILE_PATH variable in main. 

# Analysis 
View README.md file in hadoop_analysis folder to see how data sets can be analyzed.

# MapReduce - Compile MapReduce codes to .Jar
Copy the entire folder in eclipse in the VM. Before you export, ensure that the input and output folders are correct. Chanage the path according to your own needs. Otherwise, leave it as it is and export as a .Jar file. Once the jar file has been compiled. Scp the jar file to the big hadoop cluster. 
* Command: scp -r <Filename> <user@IPaddress:/home/user/>

# MapReduce - Use existing Jar files.
There are 3 .jar files inside the JAR folder. To use them, use the command specified above to send them to the big hadoop cluster

# MapReduce - Set Up 
Ensure that the company that you want to analyze is in a folder called "Materials". Note that the analysis can only be done 1 company at a time so ensure there is only 1 company folder inside the "Materials" folder.
Here is the command to scp your codes from your main machine to the big hadoop cluster.
* Command: scp -r <path to Materials folder> <user@IPaddress:/home/user/>

Next, Put the folder into the hadoop file system.
* Command: hadoop fs -put Materials /user/username/

Check the codes for the input and output file path. Below are the 3 different sets of directories you will need.
To run word count analysis
* hadoop fs -mkdir /user/username/wordcount/
* hadoop fs -mkdir /user/username/wordcount/output

To run rating count analysis
* hadoop fs -mkdir /user/username/ratingcount/
* hadoop fs -mkdir /user/username/ratingcount/output

To run sentiment count analysis
* hadoop fs -mkdir /user/username/sentimentcount/
* hadoop fs -mkdir /user/username/sentimentcount/output

# MapReduce - Running the Mapreduce on Hadoop
Once all the set up above has been done, use the commands below to run the jar files.

To run Word count .jar
* hadoop jar WordCountAnalysis.jar WordCountAnalysis

To run rating count .jar
* hadoop jar RatingCountAnalysis.jar RatingCountAnalysis

To run sentiment count .jar
* hadoop jar SentimentCountAnalysis.jar SentimentCountAnalysis

# MapReduce - View results
Once the Mapreduce process is finished. Write one of the 3 commands to view the output

Word Count output
* command: hadoop fs -cat /user/username/wordcount/output/part-r-00000

Rating Count output
* command: hadoop fs -cat /user/username/ratingcount/output/part-r-00000

Sentiment Count output
* command: hadoop fs -cat /user/username/sentimentcount/output/part-r-00000

# MapReduce - Summary
Follow all ths steps above to carry out the different processes on a single company file.
* Note: If you want to run MapReduce for other companies, insert the company folder into the Materials folder into the Materials folder and scp the folder into the big hadoop cluster and run the entire process again.


# Visualization in Flask
pip install flask , pip install wordcloud

To run the website run visualization.py under 2107Hadoopflask folder. 