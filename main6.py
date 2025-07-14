from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from datetime import datetime
import csv

driver = webdriver.Chrome()
all_rfqs = []

for i in range(1, 101):  # Loop from page 1 to 100
    print(f"\n📄 Fetching page {i}...")
    url = f"https://sourcing.alibaba.com/rfq/rfq_search_list.htm?country=AE&recently=Y&page={i}"
    driver.get(url)
    time.sleep(5)  # wait for page to load

    try:
        container = driver.find_element(By.ID, "rfqSearchindex")
        cards = container.find_elements(By.CLASS_NAME, "rfqSearchList")
        print(f"📦 Found {len(cards)} RFQs on Page {i}")

        if len(cards) == 0:
            print("❌ No more RFQs. Ending loop early.")
            break  # stop if no RFQs found

        for idx, card in enumerate(cards):
            try:
                title = card.find_element(By.CLASS_NAME, "brh-rfq-item__subject-link").text.strip()
            except:
                title = "N/A"
            try:
                buyer_name = card.find_element(By.CLASS_NAME, "text").text.strip()
            except:
                buyer_name = "N/A"
            try:
                 buyer_image = card.find_element(By.TAG_NAME, "img").get_attribute("src")
            except:
                 buyer_image = "N/A"

            
            try:
                quotes_left = card.find_element(By.CLASS_NAME, "brh-rfq-item__quote-left").text.strip()
            except:
                quotes_left = "N/A"
            try:
                country = card.find_element(By.CLASS_NAME, "brh-rfq-item__countryl").text.strip()
            except:
                country = "N/A"
            try:
                quantity = card.find_element(By.CLASS_NAME, "brh-rfq-item__quantity").text.strip()
            except:
                quantity = "N/A"
            try:
              email_confirmed = "Yes" if "email confirmed" in card.text.lower() else "No"
            except:
               email_confirmed = "N/A"
            try:
              experienced_buyer = "Yes" if "experienced buyer" in card.text.lower() else "No"
            except:
             experienced_buyer = "N/A"
            try:
              complete_order = "Yes" if "complete order via rfq" in card.text.lower() else "No"
            except:
               complete_order = "N/A"

            try:
                interactive_user = "Yes" if "interactive user" in card.text.lower() else "No"
            except:
                interactive_user = "N/A"


            try:
                inquiry_time = card.find_element(By.CLASS_NAME, "brh-rfq-item__publishtime").text.strip()
            except:
                inquiry_time = "N/A"
            try:
                rfq_url = card.find_element(By.TAG_NAME, "a").get_attribute("href")
                rfq_id = rfq_url.split("rfqid=")[-1].split("&")[0] if "rfqid=" in rfq_url else "N/A"
            except:
                rfq_url = "N/A"
                rfq_id = "N/A"

            all_rfqs.append({
                "Page": i,
                "RFQ ID": rfq_id,
                "Title": title,
                "Buyer Name": buyer_name,
                "Buyer Image": buyer_image,
                "Quotes Left": quotes_left,
                "Country": country,
                "Quantity Required": quantity,
                "Inquiry Time": inquiry_time,
                "Inquiry URL": rfq_url,
                "Email Confirmed": email_confirmed,
                "Experienced Buyer": experienced_buyer,
                "Complete Order via RFQ": complete_order,
                "Interactive User": interactive_user,
                "Scraping Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
})


    except Exception as e:
        print(f"❌ Error on page {i}: {e}")

# Close browser
driver.quit()

# ✅ Print summary
print(f"\n✅ Total RFQs scraped: {len(all_rfqs)}")
for rfq in all_rfqs[:5]:  # Show first 5
    print(rfq)
with open("alibaba_rfqs.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=all_rfqs[0].keys())
    writer.writeheader()
    writer.writerows(all_rfqs)

print("📁 RFQ data saved to 'alibaba_rfqs.csv'")