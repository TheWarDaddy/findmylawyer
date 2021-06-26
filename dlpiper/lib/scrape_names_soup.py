from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import psycopg2
from config import config
from main_profile import set_chrome_options
from multiprocessing.pool import ThreadPool
import requests
from bs4 import BeautifulSoup


PATH = "/usr/local/bin/chromedriver"
driver = webdriver.Chrome(PATH, chrome_options=set_chrome_options())

def scrape_names(profile_url):
    try:
        driver.get(profile_url)
        driver.set_window_size(1920, 1080)
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        list = driver.find_elements_by_class_name("coveo-results-per-page-list-item")
        list[3].click()
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        pages = driver.find_elements_by_class_name("coveo-pager-list-item-text")
        full_profiles = []
        time.sleep(2)
        try:
            params = config()
            connection = psycopg2.connect(**params)
            print("Database connected...")
            time.sleep(2)
        except Exception as DatabaseConnectionRefused:
            print("database Connection Refused")
        for page in pages:
            time.sleep(2)
            current_url = driver.current_url
            html_text = driver.page_source
            soup = BeautifulSoup(html_text, 'html.parser')
            time.sleep(2)
            soup_title = soup.find_all('div', {"class":"coveo-title"})
            time.sleep(2)
            for div in soup_title:
                name = div.find('a').contents[0]
                url = div.find('a')['href']
                cursor = connection.cursor()
                cursor.execute("INSERT INTO names (name, url) VALUES(%s, %s)", (str(name), str("https://www.dlapiper.com" + url)))
                connection.commit()
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            next_page = driver.find_element_by_class_name("coveo-pager-next")
            next_page.click()
            time.sleep(2)
            screen_height = driver.execute_script("return window.screen.height;")
        return full_profiles
    except Exception as error:
        print(error)
    finally:
        driver.close()
