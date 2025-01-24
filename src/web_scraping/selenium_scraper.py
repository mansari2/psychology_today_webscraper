from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import json
import time

class SeleniumScraper:
    def __init__(self, url):
        self.url = url
        self.driver = self.setup_driver()

    def setup_driver(self):
        options = Options()
        options.headless = True
        service = Service('path/to/chromedriver')  # Update with the path to your chromedriver
        driver = webdriver.Chrome(service=service, options=options)
        return driver

    def scrape(self):
        self.driver.get(self.url)
        time.sleep(3)  # Wait for JavaScript to render

        data = []
        elements = self.driver.find_elements(By.CLASS_NAME, 'therapist-card')  # Update with the actual class name

        for element in elements:
            name = element.find_element(By.CLASS_NAME, 'name').text  # Update with actual class name
            specialty = element.find_element(By.CLASS_NAME, 'specialty').text  # Update with actual class name
            rating = element.find_element(By.CLASS_NAME, 'rating').text  # Update with actual class name
            reviews = element.find_element(By.CLASS_NAME, 'reviews').text  # Update with actual class name
            contact_info = element.find_element(By.CLASS_NAME, 'contact-info').text  # Update with actual class name
            location = element.find_element(By.CLASS_NAME, 'location').text  # Update with actual class name

            data.append({
                'name': name,
                'specialty': specialty,
                'rating': rating,
                'reviews': reviews,
                'contact_info': contact_info,
                'location': location
            })

        self.driver.quit()
        return data

    def save_data(self, data, filename='scraped_data.json'):
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)

if __name__ == "__main__":
    url = 'https://example.com/therapists'  # Update with the actual URL
    scraper = SeleniumScraper(url)
    scraped_data = scraper.scrape()
    scraper.save_data(scraped_data)