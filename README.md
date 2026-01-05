# Sportsman's Warehouse Home Gym Scraper & Dashboard

This project scrapes product data from the Sportsman's Warehouse home gym section and provides a beautiful interactive dashboard for data exploration and visualization.

## Features
- Scrapes product name, image, and price from all pages
- Exports data to CSV and JSON
- Streamlit dashboard with:
  - Product gallery with images
  - Filters by brand, price, and page
  - Key metrics (total, min, max, average price)
  - Multiple interactive graphs (price distribution, brand analysis, market share, etc.)
  - Download filtered data as CSV/JSON

## Quickstart

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
2. **Scrape the data**
   ```bash
   python app.py
   ```
3. **Launch the dashboard**
   ```bash
   streamlit run streamlit_app.py
   ```
4. **Open in browser**
   - Go to the URL shown in the terminal (usually http://localhost:8501)

## Files
- `app.py` - Scrapes the website and exports data
- `streamlit_app.py` - Streamlit dashboard for data exploration
- `sportsmans_warehouse_products.csv` - Scraped data (generated)
- `requirements.txt` - Python dependencies

## Screenshots
![Dashboard Screenshot](screenshot.png)

## License
MIT
