# E-Commerce Web Scraper & Automated Price Monitor

Automated Python web scraping pipeline that extracts product catalogs, prices, ratings, and stock availability from e-commerce pages, logs historical price data in SQLite, and generates an executive Excel alert report.

## Business Problem Solved
E-commerce businesses and resellers need to track competitor pricing and stock changes daily. Manually checking product pages is slow and error-prone. This tool automates data extraction, historical tracking, and low-price alert filtering in seconds.

## Key Features
* **Automated Web Scraping (`requests` + `BeautifulSoup4`):** Parses product titles, prices, star ratings, and stock status.
* **Historical Price Tracking (`SQLite3`):** Appends timestamped extractions into a relational database to monitor price trends over time.
* **SQL Alert Filtering:** Automatically queries products below a target price threshold.
* **Multi-Sheet Excel Reporting (`pandas` + `openpyxl`):** Exports a clean workbook containing the full catalog and filtered price alerts.

## Tech Stack
* **Python 3**
* **BeautifulSoup4 & Requests** (Web scraping & HTML parsing)
* **SQLite3** (Historical database storage & SQL filtering)
* **pandas & openpyxl** (Data structuring & automated Excel reporting)

## How to Run
1. Install dependencies: `pip install requests beautifulsoup4 pandas openpyxl`
2. Run the monitor: `python price_monitor.py`