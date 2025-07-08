# Key.sa Car Scrapers

This repository contains two Python scripts to scrape vehicle data from the Key.sa website. The scrapers are built using Python and BeautifulSoup to extract structured car information for personal or educational use.

## 📌 Description

The scripts automate data collection from the Key.sa website, targeting two specific sections:

1. **Fleet Cars Scraper**: Extracts data about cars available for rental from the company's fleet.
2. **Cars for Sale Scraper**: Gathers details on used vehicles listed for sale.

These tools are intended to help developers, data analysts, and researchers quickly gather structured datasets from dynamic HTML content.

---

## 📁 Files

### 1. `fleet_scraper.py`

Scrapes the car fleet listings from Key.sa and saves the data to a CSV file (`key_fleet_parsed.csv`).

* **Target URL:** `https://www.key.sa/en/fleetPagination`
* **Pagination:** Uses `offset` to iterate through all pages
* **Output Fields:** ID, Name, Image, Category, Transmission, Doors, Bags, Prices, Booking URL, etc.

* ![image](https://github.com/user-attachments/assets/f5f9203d-a035-4b57-9c42-44e4ae774455)

![image](https://github.com/user-attachments/assets/f38ffe9b-8577-4ec3-a80d-b43b59dbd136)

### 2. `sale_scraper.py`

Scrapes cars available for sale and saves the data to a CSV file (`cars_for_sale.csv`).

* **Target URL:** `https://www.key.sa/en/getMoreSellingCars`
* **Pagination:** Uses offset with a limit of 6 per request
* **Output Fields:** Brand, Model, Year, Kilometers, Price, Discount, Sold status, Image, ID
![image](https://github.com/user-attachments/assets/53b03159-bff6-4d99-833f-d320d95512c6)
![image](https://github.com/user-attachments/assets/9bf64d56-05e2-4e7c-8ac8-482bdb5706d7)

---

## ✅ Prerequisites

* Python 3.7+
* Install required packages:

```bash
pip install requests beautifulsoup4 lxml
```

---

## 🚀 Usage

### Fleet Scraper:

```bash
python fleet_scraper.py
```

* Outputs to: `key_fleet_parsed.csv`

### Sale Scraper:

```bash
python sale_scraper.py
```

* Outputs to: `cars_for_sale.csv`

---

## 📝 Notes

* Scripts use `POST` requests with dynamic offset-based pagination.
* Returned HTML is escaped, so parsing involves unescaping and decoding.
* You can customize request headers or scraping logic based on future changes to the website.

---

## 📄 License

This project is for educational and non-commercial use only. Please respect the website’s `robots.txt` and terms of use.

---

## ⚠️ Disclaimer

This repository is intended for **educational purposes only**. The authors are not affiliated with Key.sa. Any misuse of this code for violating the terms of service, scraping rate limits, or copyright policies of the target website is strictly discouraged. Always review and follow the target website's `robots.txt` file and terms of service before scraping.
