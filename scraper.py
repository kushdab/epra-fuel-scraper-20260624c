import requests
from bs4 import BeautifulSoup
import csv
import os
import sys
import logging
from datetime import datetime

# Setup logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

class EPRAScraper:
    """
    A scraper to extract monthly petroleum prices from the Energy and Petroleum
    Regulatory Authority (EPRA) website for Kenya.
    """
    
    TARGET_URL = "https://www.epra.go.ke/services/petroleum/petroleum-prices/"
    
    def __init__(self, filename=None):
        self.timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.filename = filename or f"epra_fuel_prices_{self.timestamp}.csv"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

    def fetch_page_content(self):
        """Downloads the HTML content of the EPRA prices page."""
        try:
            logger.info(f"Requesting EPRA website: {self.TARGET_URL}")
            response = requests.get(self.TARGET_URL, headers=self.headers, timeout=20)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            logger.error(f"Network error occurred: {e}")
            return None

    def parse_pricing_table(self, html_content):
        """Parses the HTML to find the petroleum prices table."""
        if not html_content:
            return []

        soup = BeautifulSoup(html_content, 'html.parser')
        # Locate the table - EPRA often uses standard <table> tags for price lists
        table = soup.find('table')
        
        if not table:
            logger.warning("No data table found on the page. The site structure might have changed.")
            return []

        rows_data = []
        rows = table.find_all('tr')
        
        for row in rows:
            cells = row.find_all(['td', 'th'])
            # Clean text and remove empty strings
            clean_cells = [cell.get_text(strip=True) for cell in cells]
            if clean_cells:
                rows_data.append(clean_cells)
        
        return rows_data

    def export_to_csv(self, data):
        """Writes the list of lists into a CSV file."""
        if not data:
            logger.warning("No data available to export.")
            return False

        try:
            with open(self.filename, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerows(data)
            logger.info(f"Successfully exported {len(data)} rows to {self.filename}")
            return True
        except IOError as e:
            logger.error(f"Failed to write CSV: {e}")
            return False

    def run(self):
        """Orchestrates the scraping process."""
        logger.info("Starting EPRA Fuel Price Scraper...")
        
        html = self.fetch_page_content()
        if html:
            data = self.parse_pricing_table(html)
            if data:
                self.export_to_csv(data)
                logger.info("Scraping completed successfully.")
            else:
                logger.error("Process aborted: No data extracted.")
        else:
            logger.error("Process aborted: Could not reach website.")

if __name__ == "__main__":
    scraper = EPRAScraper()
    scraper.run()