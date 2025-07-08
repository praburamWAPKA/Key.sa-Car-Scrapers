import requests
from bs4 import BeautifulSoup
import csv
import html

URL = "https://www.key.sa/en/getMoreSellingCars"
OUTPUT = "cars_for_sale.csv"
LIMIT = 6

CSV_HEADERS = [
    "Brand", "Model", "Year", "Kilometers", "Price (SAR)", "Discount", "Sold", "ID", "Image"
]

def parse_html_block(raw_html):
    clean_html = html.unescape(raw_html).replace('\\"', '"').replace("\\/", "/")
    soup = BeautifulSoup(clean_html, "lxml")
    cars = []

    for div in soup.select(".car-to-sell"):
        brand = div.find("h3").get_text(strip=True)
        model = div.find("p").get_text(strip=True)

        year = kilometers = price = discount = ""

        # ✅ Try <ul class="features"> first
        features = div.select(".features li")
        if features:
            for li in features:
                text = li.get_text(strip=True)
                if "Year" in text:
                    year = text.split(":")[-1].strip()
                elif "Kilometers" in text:
                    kilometers = text.split(":")[-1].replace("km", "").replace(",", "").strip()
                elif "Price" in text:
                    price = text.split(":")[-1].replace("SAR", "").replace(",", "").strip()
                elif "Discount" in text:
                    discount = text.split(":")[-1].replace("SAR", "").replace(",", "").strip()
        else:
            # ✅ Fallback to <p> blocks
            for p in div.find_all("p"):
                text = p.get_text(strip=True)
                if "Year" in text:
                    year = text.split(":")[-1].strip()
                elif "Kilometers" in text:
                    kilometers = text.split(":")[-1].replace("km", "").replace(",", "").strip()
                elif "Price" in text:
                    price = text.split(":")[-1].replace("SAR", "").replace(",", "").strip()
                elif "Discount" in text or "Key Program Discount" in text:
                    discount = text.split(":")[-1].replace("SAR", "").replace(",", "").strip()

        # Get image
        img_tag = div.find("img")
        image = img_tag["src"] if img_tag else ""

        # Sold status
        sold = bool(div.select_one(".sold-img"))

        # Car ID from onclick
        onclick = div.select_one("button.btn-contact")
        car_id = ""
        if onclick and "interested_in_buying(" in onclick.get("onclick", ""):
            car_id = onclick["onclick"].split("(")[-1].split(")")[0]

        cars.append([
            brand, model, year, kilometers, price, discount,
            "Yes" if sold else "No", car_id, image
        ])
    return cars

def main():
    all_cars = []
    offset = 0

    print("🚗 Scraping cars for sale from Key.sa\n")

    while True:
        print(f"🔄 Fetching offset={offset}, limit={LIMIT}")
        response = requests.post(URL, data={"offset": offset, "limit": LIMIT})
        response.raise_for_status()

        json_data = response.json()
        html_block = json_data.get("html", "")
        show_more = json_data.get("show_load_more", False)

        cars = parse_html_block(html_block)
        print(f"✅ Found {len(cars)} cars at offset={offset}")
        all_cars.extend(cars)

        if not cars or not show_more:
            print("🛑 No more cars. Stopping.")
            break

        offset += LIMIT

    # Save to CSV
    with open(OUTPUT, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(CSV_HEADERS)
        writer.writerows(all_cars)

    print(f"\n💾 Saved {len(all_cars)} cars → {OUTPUT}")

if __name__ == "__main__":
    main()
