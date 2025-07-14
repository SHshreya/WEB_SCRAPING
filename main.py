from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import time

# Create a folder to save pages
SAVE_DIR = "alibaba_pages"
os.makedirs(SAVE_DIR, exist_ok=True)

# Set up Selenium WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run browser in background
driver = webdriver.Chrome(options=options)

# Loop through 1 to 100 pages
for i in range(1, 101):
    print(f"🌐 Fetching page {i}...")
    try:
        url = f"https://sourcing.alibaba.com/rfq/rfq_search_list.htm?country=AE&recently=Y&page={i}"
        driver.get(url)
        time.sleep(5)  # Wait for page to fully load

        # Save HTML content to file
        html = driver.page_source
        filepath = os.path.join(SAVE_DIR, f"page{i}.html")
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"✅ Saved page {i} to {filepath}")

    except Exception as e:
        print(f"❌ Error on page {i}: {e}")
        continue

# Close the browser
driver.quit()
print("\n🎉 Done downloading all pages.")
