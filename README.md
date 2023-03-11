# social-media-hadoop
A project for big data processing and analysis, focusing on social media data. 

# Usage
<ol>
<li> Replace the Facebook account information in scraper/accounts.json file. </li>
    <ul><li> Current implementation uses facebook login as it is not blocked for scraping </li> 
        <li> Current implementation uses google chrome, to use firefox, uncomment out the firefox lines in Main.py and change absolute path in FIREFOX_PATH to where your FIREFOX browser is located. </li>
        <li> New facebook accounts have a 60-min delay before they can be used to create a glassdoor account. After glassdoor account registered to facebook account, follow their prompts to setup account, skipping the setup process (allow glassdoor connect to fb and add job review) will prevent scraping. </li>
    </ul>
<li> Replace the company code, company name and account_number in main.py </li>
    <ul>
    <li> Company codes can be received from the reviews page 
        <ul> https://www.glassdoor.sg/Overview/Working-at-Accenture-EI_IE4138.11,20.htm 
        <li> company code = 4138, company name = Accenture </li> </ul>
    <li> TODO: Add interface for users to supply code and name</li>
    <li> TODO: Get list of company codes and companies in accenture to automate company selection</li>
    </ul>
<li> Run main.py it should open glassdoor website and attempt to login using account information provided in scraper/accounts.json file. </li>
<li> Current implementation can create mutliple sessions of glassdoor with different login details, however, work is still scheduled sequentially </li>
    <ul>
    <li> TODO: Add async / parallel processing for urls.</li>
    <li> Note opening more than 4 chrome sessions will increase likelihood of captcha </li>
    </ul>
</ol>

# Dependencies
<ol>
<li> pip install selenium
<li> pip install beautifulsoup4
<li> pip install numpy
</ol>