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
            elements = self.driver.find_elements(By.CLASS_NAME, 'profile-listing')

            for element in elements:
                try:
                    name = element.find_element(By.CLASS_NAME, 'profile-name').text
                    location = element.find_element(By.CLASS_NAME, 'location').text
                    specialty = element.find_element(By.CLASS_NAME, 'profile-specialties').text
                    rating = self.extract_rating(element)
                    reviews = self.extract_reviews(element)
                    contact_info = element.find_element(By.CLASS_NAME, 'contact-info').text

                    data.append({
                        'name': name,
                        'location': location,
                        'specialty': specialty,
                        'rating': rating,
                        'reviews': reviews,
                        'contact_info': contact_info
                    })
                except Exception as e:
                    print(f"Error extracting data for a therapist: {e}")
                    continue

            # Check for the 'Next' button and navigate
            try:
                next_button = self.driver.find_element(By.CLASS_NAME, 'next-page')
                next_button.click()
                time.sleep(3)  # Wait for the next page to load
            except:
                print("No more pages. Exiting pagination.")
                break

        self.driver.quit()
        return data

    def extract_rating(self, element):
        try:
            return element.find_element(By.CLASS_NAME, 'rating').text
        except:
            return None

    def extract_reviews(self, element):
        try:
            return element.find_element(By.CLASS_NAME, 'review-count').text
        except:
            return None

    def save_data(self, data, filename='therapists_data.json'):
        output_dir = 'data/raw'
        os.makedirs(output_dir, exist_ok=True)  # Ensure the directory exists
        file_path = os.path.join(output_dir, filename)
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"Data saved to {file_path}")


if __name__ == "__main__":
    url = 'https://www.psychologytoday.com/us/therapists/tennessee'  # Target website
    driver_path = 'path/to/chromedriver'  # Update with the actual path to your chromedriver

    scraper = TherapistScraper(url, driver_path)
    scraped_data = scraper.scrape()
    scraper.save_data(scraped_data)