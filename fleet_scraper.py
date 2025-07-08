import csv
import html
import re
import requests
from bs4 import BeautifulSoup

# --- CONFIG ---
URL = "https://www.key.sa/en/fleetPagination"
HEADERS = {
    "Content-Type": "application/x-www-form-urlencoded",
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://www.key.sa/en/fleet"
}
OUTPUT_CSV = "key_fleet_parsed.csv"

HEADERS_CSV = [
    "ID", "Name", "Image", "Category", "Passengers", "Transmission", "Doors", "Bags", "Min Age", "Rent/Day (SAR)",
    "CDW", "CDW Plus", "Baby Seat", "Open KM", "Extra Driver", "Disabled Support", "Booking URL",
    "Extra Hours Bronze", "Silver", "Golden", "Platinum",
    "Extra KM Bronze", "Silver", "Golden", "Platinum"
]

def extract_cars(escaped_html):
    if escaped_html.startswith('"') and escaped_html.endswith('"'):
        escaped_html = escaped_html[1:-1]
    unescaped_html = html.unescape(escaped_html)
    unescaped_html = unescaped_html.replace('\\"', '"').replace("\\/", "/")

    soup = BeautifulSoup(unescaped_html, "lxml")
    anchors = soup.find_all("a", class_="compare-btn")
    results = []

    for car in anchors:
        results.append([
            car.get("data-id", ""),
            car.get("data-name", ""),
            car.get("data-image", ""),
            car.get("data-category", ""),
            car.get("data-passengers", ""),
            car.get("data-transmission", ""),
            car.get("data-doors", ""),
            car.get("data-bags", ""),
            car.get("data-min_age", ""),
            car.get("data-rent", ""),
            car.get("data-cdw", ""),
            car.get("data-cdw_plus", ""),
            car.get("data-baby_seat", ""),
            car.get("data-open_km", ""),
            car.get("data-extra_driver", ""),
            car.get("data-is_for_disabled", ""),
            car.get("data-book_url", ""),
            car.get("data-extra_hours_bronze", ""),
            car.get("data-extra_hours_silver", ""),
            car.get("data-extra_hours_golden", ""),
            car.get("data-extra_hours_platinum", ""),
            car.get("data-extra_km_bronze", ""),
            car.get("data-extra_km_silver", ""),
            car.get("data-extra_km_golden", ""),
            car.get("data-extra_km_platinum", "")
        ])
    return results

def main():
    all_data = []
    offset = 0

    while True:
        print(f"🔄 Requesting offset {offset} ...")
        data = {
            "branch": "",
            "cat_id": "0",
            "model": "",
            "class": "all",
            "from_region_id": "1",
            "offset": str(offset)
        }
        response = requests.post(URL, headers=HEADERS, data=data)
        response.raise_for_status()
        html_content = response.text.strip()

        cars = extract_cars(html_content)
        if not cars:
            print(f"🛑 No more cars found at offset {offset}. Stopping.")
            break

        print(f"✅ Found {len(cars)} cars at offset {offset}")
        all_data.extend(cars)
        offset += 1

    if all_data:
        with open(OUTPUT_CSV, "w", newline='', encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(HEADERS_CSV)
            writer.writerows(all_data)
        print(f"\n💾 Saved {len(all_data)} cars to {OUTPUT_CSV}")
    else:
        print("⚠️ No car data found.")

if __name__ == "__main__":
    main()
