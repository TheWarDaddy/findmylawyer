from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


PATH = "/usr/local/bin/chromedriver"
driver = webdriver.Chrome(PATH)

def set_chrome_options():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_prefs = {}
    chrome_options.experimental_options["prefs"] = chrome_prefs
    chrome_prefs["profile.default_content_settings"] = {"images": 2}
    return chrome_options


def scrape_infos(profile_url):
    try:
        driver.get(profile_url)
        driver.set_window_size(1920, 1080)
        profile = dict.fromkeys(["full_name", "post", "post2", "email", "location", "phoneT", "related_services", "related_sectors"], None)
        time.sleep(2)
        card = driver.find_elements_by_class_name("media-body")
        profile["full_name"] = driver.find_elements_by_tag_name("h2")[1].text
        profile["post"] = driver.find_element_by_tag_name("h3").text
        try:
            profile["post2"] = driver.find_element_by_tag_name("h4").text
        except Exception as Error:
            print(error)
#            logging.warning('No Post Founded')
        profile["email"] = driver.find_element_by_class_name("attyemail").text
        locations = driver.find_element_by_class_name("addresses")
        local_address = locations.find_elements_by_tag_name("p")
        profile["location"] = []
        profile["related_services"] = []
        profile["related_sectors"] = []
        for i in range(0, len(local_address)):
            current = locations.find_elements_by_tag_name("p")[i].text
            profile["location"].append(current)
        profile["phoneT"] = locations.find_element_by_tag_name("span").text
        body = driver.find_elements_by_class_name("js-ui-related-info")
        content_block = driver.find_elements_by_class_name("related-options")
        for i in range(0,len(content_block)):
            if str(content_block[i].find_element_by_tag_name("h4").text)=="Related services":
                services = content_block[i].find_elements_by_class_name("module-list__item")
                for service in services:
                    profile["related_services"].append(service.text)
                break
        for i in range(0,len(content_block)):
            if str(content_block[i].find_element_by_tag_name("h4").text)=="Related sectors":
                sectors = content_block[i].find_elements_by_class_name("module-list__item")
                for sector in sectors:
                    profile["related_sectors"].append(sector.text)
                break
        return profile
    finally:
        driver.close()

def get_related_services(profile_url):
    try:
        driver.get(profile_url)
        driver.set_window_size(1920, 1080)
        time.sleep(2)
        related_services = []
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        body = driver.find_elements_by_class_name("js-ui-related-info")
        content_block = driver.find_elements_by_class_name("related-options")
        for i in range(0,len(content_block)):
            if str(content_block[i].find_element_by_tag_name("h4").text)=="Related services":
                services = content_block[i].find_elements_by_class_name("module-list__item")
                for service in services:
                    related_services.append(service.text)
                break
        return related_services
    finally:
        driver.close()

def get_related_sectors(profile_url):
    try:
        driver.get(profile_url)
        driver.set_window_size(1920, 1080)
        time.sleep(2)
        related_sectors = []
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        body = driver.find_elements_by_class_name("js-ui-related-info")
        content_block = driver.find_elements_by_class_name("related-options")
        for i in range(0,len(content_block)):
            if str(content_block[i].find_element_by_tag_name("h4").text)=="Related sectors":
                sectors = content_block[i].find_elements_by_class_name("module-list__item")
                for sector in sectors:
                    related_sectors.append(sector.text)
                break
        return related_sectors
    finally:
        driver.close()

def get_main_text(profile_url):
    try:
        driver.get(profile_url)
        driver.set_window_size(1920, 1080)
        overview = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "col--main"))
                )
        text_overview = overview.text
        return str(text_overview)
    finally:
        driver.close()

def get_quote(profile_url):
    try:
        driver.get(profile_url)
        driver.set_window_size(1920, 1080)
        quote = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "blockquote"))
                )
        text_quote = quote.text
        return str(text_quote)
    finally:
        driver.close()


def get_main_experience(profile_url):
    try:
        driver.get(profile_url)
        driver.set_window_size(1920, 1080)
        experience_button = driver.find_element_by_class_name("experience")
        experience_button.click()
        time.sleep(2)
        experience = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "col--main"))
                )
        text_experience= experience.text
        return str(text_experience)
    except Exception as ProfileWithNoExperience:
#        logging.warning('no experience founded')
        return ""
    finally:
        driver.close()

def get_main_credentials(profile_url):
    try:
        driver.get(profile_url)
        driver.set_window_size(1920, 1080)
        credentials_button = driver.find_element_by_class_name("credentials")
        credentials_button.click()
        time.sleep(2)
        credentials = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "col--main"))
                )
        text_credentials= credentials.text
        return str(text_credentials)
    except Exception as ProfileWithNoCredentials:
#        logging.warning('no credentials founded')
        return ""
    finally:
        driver.close()
