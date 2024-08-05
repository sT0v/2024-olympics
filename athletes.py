import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

import pandas as pd



def scraped_country_athlete_count() -> pd.DataFrame:
    """Get the number of athletes each country sent to the 2024 Olympics."""
    # https://olympics.com/en/paris-2024/athletes/all-disc/argentina
    # <div class="mirs-pagination-right"><span class="pe-3">143 Elements</span>
    # 1. get list of countries.
    # 2. query base url for each and extract number from "143 Elements"

    # Set up Chrome options
    chrome_options = Options()
    # does not seem to work in headless mode
    # chrome_options.add_argument("--headless")  # Enable headless mode
    # chrome_options.add_argument("--no-sandbox")  # Bypass OS security model
    # chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems


    # Set up the Chrome WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        # Navigate to the website
        driver.get('https://olympics.com/en/paris-2024/athletes/all-disc/argentina')

        # Wait for javascript to render page
        elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.mirs-pagination-right span.pe-3'))
        ) # represents number of athletes for country
    
        m = re.search("(?P<n_athletes>\d+) Elements", [e.text for e in elements][0])
        n_athletes = int(m.group("n_athletes"))
        print(n_athletes)

    finally:
        # Close the WebDriver
        driver.quit()