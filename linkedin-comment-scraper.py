import csv
import re
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def login(driver, email, password):
    """
    Logs into LinkedIn using the provided credentials.

    Parameters:
        driver (webdriver): The Selenium WebDriver.
        email (str): User's email.
        password (str): User's password.

    Raises:
        TimeoutException: If the login elements do not appear within the specified timeout.
    """
    driver.get("https://www.linkedin.com/login")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username"))).send_keys(email)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "password"))).send_keys(password)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(),'Sign in')]"))).click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "global-nav-typeahead")))

def validate_url(url):
    """
    Validates if the given URL is a LinkedIn post URL.

    Parameters:
        url (str): URL to validate.

    Returns:
        bool: True if the URL is a valid LinkedIn post URL, False otherwise.
    """
    pattern = re.compile(r"https://www\.linkedin\.com/posts/[\w-]+")
    return pattern.match(url) is not None

def scrape_comments(post_url, email, password):
    """
    Scrapes comments from a LinkedIn post URL using Selenium and BeautifulSoup.

    Parameters:
        post_url (str): URL of the LinkedIn post.
        email (str): LinkedIn email for login.
        password (str): LinkedIn password for login.

    Returns:
        list of dict: A list of dictionaries containing comment details.

    Raises:
        Exception: General exceptions during comment parsing, with error printed.
    """
    driver = webdriver.Chrome()
    try:
        login(driver, email, password)
        driver.get(post_url)
        time.sleep(5)  # Allow page to load

        # Scroll down until all comments are loaded
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)  # Wait for the page to load
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        # Ensure comments section is loaded
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.comments-comments-list")))

        # Parse comments using BeautifulSoup
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        comments = soup.find_all('article', {'class': 'comments-comment-item'})

        comments_data = []
        for comment in comments:
            try:
                # Extract comment details
                url = comment.find('a', {'class': 'comments-post-meta__actor-link'})['href']
                name_div = comment.find('div', {'class': 'comments-post-meta'})
                full_text = name_div.get_text(strip=True)
                name = full_text.split('View')[0].strip()
                position = comment.find('span', {'class': 'comments-post-meta__headline'}).get_text(strip=True)
                comment_text = comment.find('span', {'class': 'comments-comment-item__main-content'}).get_text(strip=True)
                comments_data.append({'Name': name, 'LinkedIn URL': url, 'Position': position, 'Comment Text': comment_text})
            except Exception as e:
                print(f"Failed to parse a comment due to: {e}")

        return comments_data
    finally:
        driver.quit()

def save_to_csv(data, filename='linkedin_comments.csv'):
    """
    Saves scraped data to a CSV file.

    Parameters:
        data (list of dict): List of dictionaries containing comment data to write.
        filename (str): Filename for the CSV file.

    Raises:
        IOError: If the file could not be written.
    """
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

def main():
    """
    Main function to handle user input and orchestrate scraping and saving comments.
    """
    email = input("Enter your LinkedIn email: ")
    password = input("Enter your LinkedIn password: ")
    post_url = input("Enter the LinkedIn post URL: ")

    if validate_url(post_url):
        comments = scrape_comments(post_url, email, password)
        if comments:
            save_to_csv(comments)
            print("Comments have been saved to 'linkedin_comments.csv'.")
            print("Scraped comments (" + str(len(comments)) + "):")
            count = 1
            for comment in comments:
                print("\n" + str(count) + ". --- Comment Details ---")
                count += 1
                print(f"Name: {comment['Name']}")
                print(f"LinkedIn URL: {comment['LinkedIn URL']}")
                print(f"Position: {comment['Position']}")
                print(f"Comment: {comment['Comment Text']}\n")
        else:
            print("No comments were found.")
    else:
        print("Invalid LinkedIn post URL. Please ensure the URL is correct and try again.")

if __name__ == "__main__":
    main()