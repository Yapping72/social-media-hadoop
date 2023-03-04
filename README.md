# social-media-hadoop
A project for big data processing and analysis, focusing on social media data. 

# Usage
<ol>
<li> Replace the gmail account information in scraper/accounts.json file. </li>
<li> "Google": {
        "username": "example123@gmail.com",
        "password": "examplepassword"
    } </li>
<li> To run "python3 main.py", it should open glassdoor website and attempt to login using account infomration provided in scraper/accounts.json file. </li>
<li> Current implementation uses google chrome, to use firefox, uncomment out the firefox lines in Main.py and change absolute path in FIREFOX_PATH to where your FIREFOX browser is located. 
<ol>

## Dependencies
pip install selenium
pip install pyperclip
