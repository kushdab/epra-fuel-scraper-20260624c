# EPRA Fuel Price Scraper

Python utility to extract the latest petroleum prices (Super Petrol, Diesel, Kerosene) from the Kenya Energy and Petroleum Regulatory Authority (EPRA) website.

## Features
- Fetches monthly price updates automatically.
- Parses HTML tables into structured data.
- Exports results to a timestamped CSV file.
- Comprehensive logging for troubleshooting.

## Installation
1. Ensure you have Python 3.8+ installed.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
Run the scraper directly:
```bash
python scraper.py
```

The output will be saved as `epra_fuel_prices_YYYY-MM-DD_HH-MM-SS.csv` in the root directory.

## Requirements
- `requests`: Handling HTTP requests.
- `beautifulsoup4`: Parsing HTML content.