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
        options.add_argument('--headless=new') 
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        service = Service(self.driver_path)
        driver = webdriver.Chrome(service=service, options=options)
        return driver

    def scrape_main_page(self):
        """Scrape names, locations, profile links, and statements from all pages."""
        self.driver.get(self.url)
        time.sleep(3)  # Wait for JavaScript to render

        data = []
        page_number = 1  # Track the current page number for debugging

        while True:
            print(f"Scraping page {page_number}...")

            # Locate therapist cards on the current page
            elements = self.driver.find_elements(By.CLASS_NAME, 'results-row')

            for element in elements:
                try:
                    # Extract name, location, and profile link
                    name = element.find_element(By.CLASS_NAME, 'profile-title').text
                    location = element.find_element(By.CLASS_NAME, 'profile-location').text
                    link_element = element.find_element(By.CLASS_NAME, 'results-row-image')
                    profile_url = link_element.get_attribute('href')

                    # Extract the statement
                    try:
                        statement = element.find_element(By.CLASS_NAME, 'profile-statement').text
                    except:
                        statement = "Not available"

                    # Append data for each therapist
                    data.append({
                        'name': name,
                        'location': location,
                        'profile_url': profile_url,
                        'statement': statement,
                        'phone': None  # Placeholder for phone number
                    })
                except Exception as e:
                    print(f"Error extracting data for a therapist: {e}")
                    continue

            # Check for the 'Next' button and navigate
            try:
                next_button = self.driver.find_element(By.XPATH, '//a[@class="page-btn button-element page-btn" and ./span[@aria-label="Next"]]')
                next_page_url = next_button.get_attribute('href')  # Extract the href for debugging
                print(f"Navigating to next page: {next_page_url}")
                next_button.click()
                time.sleep(3)  # Wait for the next page to load
                page_number += 1
            except Exception as e:
                print(f"No more pages or error finding Next button: {e}. Exiting pagination.")
                break

        return data

    def scrape_phone_numbers(self, therapists):
        """Iterate over each therapist's profile URL to scrape phone numbers."""
        for therapist in therapists:
            try:
                self.driver.get(therapist['profile_url'])
                time.sleep(3)  # Wait for the detail page to load

                # Locate the phone number on the detail page
                phone_element = self.driver.find_element(By.CLASS_NAME, 'lets-connect-phone-number')
                phone = phone_element.get_attribute('href').replace("tel:", "")  # Clean phone number
                therapist['phone'] = phone
            except Exception as e:
                print(f"Error extracting phone number for {therapist['name']}: {e}")
                therapist['phone'] = "Not found"

        return therapists

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

    # Step 1: Scrape main page for names, locations, profile links, and statements
    therapists = scraper.scrape_main_page()
    scraper.save_data(therapists, filename='therapists_basic_data.json')

    # Step 2: Scrape phone numbers from profile links
    therapists_with_phones = scraper.scrape_phone_numbers(therapists)
    scraper.save_data(therapists_with_phones, filename='therapists_full_data.json')

    scraper.driver.quit()
