# social-media-hadoop
A project for big data processing and analysis, focusing on social media data. 

# Usage 
<ol>
<li> Ensure facebook accounts in accounts.json file is not banned and has completed glassdoor account setup. </li>
    <ul><li> Current implementation uses facebook login as it is not blocked for scraping </li> 
        <li> New facebook accounts have a 60-min delay before they can be used to create a glassdoor account. **After glassdoor account registered to facebook account, follow their prompts to setup account**, skipping the setup process (allow glassdoor connect to fb and add job review) will prevent scraping. </li>
    </ul>
<li> Replace the **company code, company name and account_number** in main.py. </li>
    <ul>
    <li> Company codes can be obtained from the reviews page.
        <ul> https://www.glassdoor.sg/Overview/Working-at-Accenture-EI_IE4138.11,20.htm 
        <li> company code = 4138, company name = Accenture </li> </ul>
    </ul>
<li> Run main.py it should open glassdoor website and attempt to login using account information provided in 'scraper/accounts.json' file. </li>
    <ul>
        <li>Chrome broswer should automatically open</li>
        <li>Automatic login via facebook **Please solve captcha if it appears, frequency of apperance increasing**</li>
        <li>On login success terminal should display login successful, and will automatically retrieve the list of urls to scrape and will begin scraping.
        <li>You will see the chrome browser traversing through each page and storing reviews.
        <li>Once 100 pages (~300-800 seconds) have been crawled, json contain reviews saved to the 'data/company_name' folder. (Each json file will contain 1000 reviews).
    </ul>
</ul>
</ol>

# Multiple Chrome Broswers
To scrape multiple companies in parallel, run multiple instance of main.py. Each instance should use a different facebook account. Scraping with multiple chrome browsers increases likelihood of captcha and Invalid session. Can safely run 3-4 chrome browswers without captcha occurinng frequently (depends on facebook account used).

# Dependencies
<ol>
<li> pip install selenium
<li> pip install beautifulsoup4
<li> pip install numpy
</ol>