from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

def get_driver():
    service = Service(executable_path="scrapers/chromedriver.exe")
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Run in headless mode
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver