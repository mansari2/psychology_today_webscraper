from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import json
import time
import os

class TherapistScraper:
    def __init__(self, url, driver_path):
        self.url = url
        self.driver_path = driver_path
        self.driver = self.setup_driver()

    def setup_driver(self):
        options = Options()
        options.headless = True
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        service = Service(self.driver_path)
        driver = webdriver.Chrome(service=service, options=options)
        return driver

    def scrape(self):
        self.driver.get(self.url)
        time.sleep(3)  # Wait for JavaScript to render

        data = []
        while True:
            # Locate therapist cards on the current page
            elements = self.driver.find_elements(By.CLASS_NAME, 'results-row')  # Main container for each therapist

            for element in elements:
                try:
                    # Extract individual data points
                    name = element.find_element(By.CLASS_NAME, 'profile-title').text
                    location = element.find_element(By.CLASS_NAME, 'profile-location').text

                    # Phone number may need to be handled as an optional field
                    try:
                        phone = element.find_element(By.CLASS_NAME, 'profile-phone').text
                    except:
                        phone = "Not listed"

                    data.append({
                        'name': name,
                        'location': location,
                        'phone': phone
                    })
                except Exception as e:
                    print(f"Error extracting data for a therapist: {e}")
                    continue

            # Check for the 'Next' button and navigate
            try:
                next_button = self.driver.find_element(By.CLASS_NAME, 'next')  # Update this if the "Next" button has a different class name
                next_button.click()
                time.sleep(3)  # Wait for the next page to load
            except:
                print("No more pages. Exiting pagination.")
                break

        self.driver.quit()
        return data

    def save_data(self, data, filename='therapists_data.json'):
        output_dir = 'data/raw'
        os.makedirs(output_dir, exist_ok=True)  # Ensure the directory exists
        file_path = os.path.join(output_dir, filename)
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"Data saved to {file_path}")


if __name__ == "__main__":
    url = 'https://www.psychologytoday.com/us/therapists/tennessee'  # Target website
    driver_path = '/usr/local/bin/chromedriver'  # Update with the actual path to your chromedriver

    scraper = TherapistScraper(url, driver_path)
    scraped_data = scraper.scrape()
    scraper.save_data(scraped_data)
