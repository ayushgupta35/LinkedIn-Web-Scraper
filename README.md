
# LinkedIn Comment Scraper

## Overview
The LinkedIn Comment Scraper is a Python tool that automates the process of extracting comments from LinkedIn posts using Selenium and BeautifulSoup. This tool is useful in analyzing comments on specific LinkedIn posts.

## Features
- **Login Automation**: Automates the login process to LinkedIn with user credentials.
- **Comment Extraction**: Scrapes all comments from a specified LinkedIn post.
- **Data Handling**: Parses and saves the extracted comment data into a CSV file for easy analysis and reporting.

## Requirements
- Python 3.6 or higher
- Selenium
- BeautifulSoup4
- Chrome WebDriver

## Installation

Before running the scraper, you need to install the required Python libraries and set up Chrome WebDriver.

### Python Libraries
Install the required Python libraries using pip:

```bash
pip install selenium
pip install beautifulsoup4
```

### Chrome WebDriver
Download the Chrome WebDriver from [ChromeDriver - WebDriver for Chrome](https://sites.google.com/a/chromium.org/chromedriver/) and place it in your system PATH.

## Usage

To use the LinkedIn Comment Scraper, follow these steps:

1. Clone this repository to your local machine.
2. Ensure you have all the required software installed as mentioned under the Installation section.
3. Run the script from the command line:

```bash
python linkedin_comment_scraper.py
```

4. Enter your LinkedIn credentials and the URL of the post from which you want to scrape comments when prompted.

## Configuration

No additional configuration is needed. User inputs for LinkedIn credentials and post URL are handled through command line prompts.

## Output

The script will output the scraped comments in the console as well as into a CSV file named `linkedin_comments.csv` in the same directory where the script is run. Each row in the CSV file represents a comment and includes the following details:
- Name of the commenter
- LinkedIn profile URL of the commenter
- Commenter's position (if available)
- Text of the comment
