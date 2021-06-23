from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import psycopg2
from config import config
from main_profile import set_chrome_options


PATH = "/usr/local/bin/chromedriver"
driver = webdriver.Chrome(PATH, , chrome_options=set_chrome_options())

def scrape_names(url):
    driver.get(profile_url, chrome_options=set_chrome_options())
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
    scroll_pause_time = 2
    screen_height = driver.execute_script("return window.screen.height;")
    i = 1
    j = 0
    for page in pages:
        time.sleep(2)
        while True:
            driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))
            main = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "coveo-result-list-container"))
                    )
            peoples = main.find_elements_by_class_name("coveo-list-layout")
            try:
                params = config()
                connection = psycopg2.connect(**params)
                print("Database connected...")
                time.sleep(2)
            except Exception as DatabaseConnectionRefused:
                print("database Connection Refused")
            for people in peoples:
                profiles_dictionnary = dict.fromkeys(["full_name", "profile_url"], None)
                url = people.find_element_by_tag_name("a").get_attribute('href')
                name = people.find_element_by_class_name("CoveoResultLink")
                profiles_dictionnary["full_name"] = name.text
                profiles_dictionnary["profile_url"] = url
                cursor = connection.cursor()
                cursor.execute("INSERT INTO names (names, urls) VALUES(%s, %s)", (name.text, url))
                connection.commit()
                full_profiles.append(profiles_dictionnary)
            cursor.close()
            connection.close()
            i += 1
            time.sleep(scroll_pause_time)
            scroll_height = driver.execute_script("return document.body.scrollHeight;")
            if (screen_height) * i > scroll_height:
                break
        j += 1
        if j == len(pages):
#            LOGGER.info(str(len(full_profiles)) + " profile is scrapped ...")
            break
        else:
#            LOGGER.info("Move to the next page...")
            next_page = driver.find_element_by_class_name("coveo-pager-next")
            next_page.click()
        time.sleep(2)
        screen_height = driver.execute_script("return window.screen.height;")
    return full_profiles

if __name__ == "__main__":
    scrape_names("https://www.dlapiper.com/en/uk/people/#first=900&sort=relevancy")
