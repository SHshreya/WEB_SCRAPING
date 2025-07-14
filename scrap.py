from bs4 import BeautifulSoup
import os
from datetime import datetime
import csv

all_rfqs = []

# Folder where all static HTML files are stored
html_folder = "alibaba_pages"  # Make sure this folder contains page1.html, page2.html, ..., page100.html

for i in range(1, 101):
    filename = os.path.join(html_folder, f"page{i}.html")
    if not os.path.exists(filename):
        print(f"Page {i} not found. Skipping.")
        continue

    print(f"📄 Parsing page {i}...")
    with open(filename, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")

    cards = soup.find_all("div", class_="rfqSearchList")
    print(f" Found {len(cards)} RFQs on Page {i}")

    if len(cards) == 0:
        print("No RFQs found. Possibly end of data.")
        break

    for card in cards:
        try:
            title = card.select_one(".brh-rfq-item__subject-link").get_text(strip=True)
        except:
            title = "N/A"
        try:
            buyer_name = card.select_one(".text").get_text(strip=True)
        except:
            buyer_name = "N/A"
        try:
            buyer_image = card.select_one("img")["src"]
        except:
            buyer_image = "N/A"
        try:
            quotes_left = card.select_one(".brh-rfq-item__quote-left").get_text(strip=True)
        except:
            quotes_left = "N/A"
        try:
            country = card.select_one(".brh-rfq-item__countryl").get_text(strip=True)
        except:
            country = "N/A"
        try:
            quantity = card.select_one(".brh-rfq-item__quantity").get_text(strip=True)
        except:
            quantity = "N/A"
        try:
            inquiry_time = card.select_one(".brh-rfq-item__publishtime").get_text(strip=True)
        except:
            inquiry_time = "N/A"
        try:
            full_text = card.get_text(strip=True).lower()
            email_confirmed = "Yes" if "email confirmed" in full_text else "No"
            experienced_buyer = "Yes" if "experienced buyer" in full_text else "No"
            complete_order = "Yes" if "complete order via rfq" in full_text else "No"
            interactive_user = "Yes" if "interactive user" in full_text else "No"
        except:
            email_confirmed = experienced_buyer = complete_order = interactive_user = "N/A"
        try:
            rfq_url = card.select_one("a")["href"]
            rfq_id = rfq_url.split("rfqid=")[-1].split("&")[0] if "rfqid=" in rfq_url else "N/A"
        except:
            rfq_url = rfq_id = "N/A"

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

# Save to CSV
if all_rfqs:
    with open("alibaba_rfqs_from_html.csv", mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=all_rfqs[0].keys())
        writer.writeheader()
        writer.writerows(all_rfqs)

    print(f"\nTotal RFQs scraped: {len(all_rfqs)}")
    print("Data saved to 'alibaba_rfqs_from_html.csv'")
else:
    print("No RFQs were extracted.")
