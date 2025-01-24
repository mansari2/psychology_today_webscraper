from bs4 import BeautifulSoup
import requests
import json
import os

class PsychologistScraper:
    def __init__(self, base_url, output_file):
        self.base_url = base_url
        self.output_file = output_file
        self.data = []

    def scrape(self):
        response = requests.get(self.base_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            self.extract_data(soup)
            self.save_data()
        else:
            print(f"Failed to retrieve data: {response.status_code}")

    def extract_data(self, soup):
        for entry in soup.find_all('div', class_='therapist-entry'):
            name = entry.find('h2', class_='name').text.strip()
            location = entry.find('span', class_='location').text.strip()
            rating = entry.find('span', class_='rating').text.strip()
            reviews = entry.find('span', class_='reviews').text.strip()
            specialties = entry.find('div', class_='specialties').text.strip()
            contact_info = entry.find('span', class_='contact-info').text.strip()

            self.data.append({
                'name': name,
                'location': location,
                'rating': rating,
                'reviews': reviews,
                'specialty': specialties,
                'contact_info': contact_info
            })

    def save_data(self):
        os.makedirs(os.path.dirname(self.output_file), exist_ok=True)
        with open(self.output_file, 'w') as f:
            json.dump(self.data, f, indent=4)

if __name__ == "__main__":
    base_url = 'https://example.com/therapists'
    output_file = 'data/raw/therapists_data.json'
    scraper = PsychologistScraper(base_url, output_file)
    scraper.scrape()