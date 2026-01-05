import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

# List to store all product data
products_data = []

# Loop through pages 1-4
for page in range(1, 5):
    url = f"https://www.sportsmanswarehouse.co.za/category/fitness-3/home-gym/?srsltid=AfmBOorjYM-69VwrjiX9ak_4pG8eET9CQTloQpRRd1UqoxoxJXro-eKC&page={page}"
    
    print(f"Scraping page {page}...")
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all product items
        grid_items = soup.find_all('div', class_='grid-item')
        
        for item in grid_items:
            try:
                # Extract product name
                title_div = item.find('div', class_='title')
                product_name = title_div.find('a').text.strip() if title_div else 'N/A'
                
                # Extract image URL
                img_tag = item.find('img', class_='hover-product-image')
                image_url = img_tag['src'] if img_tag else 'N/A'
                
                # Extract price
                price_div = item.find('div', class_='price')
                if price_div:
                    # Get the price text and clean it
                    price_text = price_div.get_text(strip=True)
                    # Remove non-breaking spaces and other special characters
                    price_text = price_text.replace('\xa0', '').replace('Â', '').replace('\u00a0', '')
                    # Extract just the numbers and decimal
                    price_match = re.search(r'R\s*([\d\s]+\.?\d*)', price_text)
                    if price_match:
                        # Clean up the number part - remove spaces
                        price_number = price_match.group(1).replace(' ', '')
                        price = f"R {price_number}"
                    else:
                        price = 'N/A'
                else:
                    price = 'N/A'
                
                # Add to products list
                products_data.append({
                    'product_name': product_name,
                    'image_url': image_url,
                    'price': price,
                    'page': page
                })
                
            except Exception as e:
                print(f"Error extracting product on page {page}: {e}")
                continue
        
        print(f"Successfully scraped {len(grid_items)} products from page {page}")
        
    else:
        print(f"Failed to retrieve page {page}. Status code: {response.status_code}")

# Create DataFrame
df = pd.DataFrame(products_data)

print(f"\nTotal products scraped: {len(df)}")
print("\nFirst few products:")
print(df.head())

# Export to CSV
csv_filename = 'sportsmans_warehouse_products.csv'
df.to_csv(csv_filename, index=False, encoding='utf-8')
print(f"\nData exported to {csv_filename}")

# Export to JSON
json_filename = 'sportsmans_warehouse_products.json'
df.to_json(json_filename, orient='records', indent=2, force_ascii=False)
print(f"Data exported to {json_filename}")

print("\nScraping complete!")
