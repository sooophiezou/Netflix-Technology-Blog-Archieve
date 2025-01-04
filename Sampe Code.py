"""This code is utilised for the purposes of my master's dissertation research.In order to identify the technology keywords from Netflix's technology blog, I employed the Selenium to simulate user interaction and to scratch the article title from Medium."""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import csv
from bs4 import BeautifulSoup

# Setting Selenium
chrome_options = Options()
chrome_options.add_argument("--headless") 
chrome_options.add_argument("--disable-blink-features=AutomationControlled") 
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

# Initialised WebDriver
browser = webdriver.Chrome(options=chrome_options)

# Open Netflix Technology Blog Archive
browser.get('https://netflixtechblog.com/archive')

# Loaded all the articles
def scroll_and_load():
    last_height = browser.execute_script("return document.body.scrollHeight")
    while True:
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2) 
        new_height = browser.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

data = []

# Loop for access all the articles by year
for year in range(2011, 2025):
    for month in range(1, 13):
        month_str = f'{month:02}'
        url = f'https://netflixtechblog.com/archive/{year}/{month_str}'
        print(f"Accessing {url}")
        browser.get(url)
        
        scroll_and_load()

        # Extract page content
        html = browser.page_source
        soup = BeautifulSoup(html, 'html.parser')
        
        # Extract page elements
        articles = soup.find_all('div', class_='streamItem streamItem--postPreview js-streamItem')
        print(f"Found {len(articles)} articles for {year}-{month_str}.")
        
        for article in articles:
            try:
                title_element = article.find('h3',class_='h3 name')
                time_element = article.find('time')
                if title_element and time_element:
                    title = title_element.text.strip()
                    datetime = time_element['datetime']
                    print(f"Title: {title}, Date: {datetime}")
                    data.append([datetime, title])
            except Exception as e:
                print(f"Error processing article: {e}")
                continue

# Quit brower
browser.quit()

# Checked the data
if not data:
    print("No data extracted.")
else:
    print("Data extraction successful.")

# Saved to CSV
with open('netflix_tech_blog_articles_2011-2024.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Date', 'Title'])
    writer.writerows(data)

print("Data has been saved to CSV files.")