# social-media-hadoop
A project for big data processing and analysis, focusing on social media data. 

# Usage
<ol>
<li> Replace the gmail or Facebook account information in scraper/accounts.json file. 
e.g., "Google": {
        "username": "example123@gmail.com",
        "password": "examplepassword"
    } </li>
    <ul> <li> Current implementation uses facebook login, not blocked for scraping </li> </ul>
<li> Run Main.py it should open glassdoor website and attempt to login using account information provided in scraper/accounts.json file. </li>
<li> Current implementation uses google chrome, to use firefox, uncomment out the firefox lines in Main.py and change absolute path in FIREFOX_PATH to where your FIREFOX browser is located. 
</ol>

# Dependencies
<ol>
<li> pip install selenium
<li> pip install pyperclip
</ol>