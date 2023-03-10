# social-media-hadoop
A project for big data processing and analysis, focusing on social media data. 

# Usage
<ol>
<li> Replace the Facebook account information in scraper/accounts.json file. 
e.g., "Facebook_1": {
        "username": "example123@gmail.com",
        "password": "examplepassword"
    } </li>
    <ul> <li> Current implementation uses facebook login as it is not blocked for scraping </li> 
        <li> Current implementation uses google chrome, to use firefox, uncomment out the firefox lines in Main.py and change absolute path in FIREFOX_PATH to where your FIREFOX browser is located. </li>
    </ul>
<li> Run main.py it should open glassdoor website and attempt to login using account information provided in scraper/accounts.json file. </li>
<li> Replace the company code and company name in main.py </li>
    <ul>
    <li> TODO: Add interface for users to supply code and name</li>
    <li> TODO: Get list of company codes and companies in accenture to automate company selection</li>
    </ul>
<li> Current implementation can create mutliple sessions of glassdoor with different login details, however, work is still scheduled sequentially </li>
    <ul>
    <li> TODO: Add async / parallel processing for urls.</li>
    </ul>
</ol>

# Dependencies
<ol>
<li> pip install selenium
<li> pip install beautifulsoup4
<li> pip install numpy
</ol>