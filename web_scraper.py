import requests
from bs4 import BeautifulSoup
import pandas as pd

# Website URL
url = "https://books.toscrape.com/"

# Send request to the website
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")

    products = []

    # Find all product containers
    books = soup.find_all("article", class_="product_pod")

    # Extract product information
    for book in books:
        name = book.h3.a["title"]
        price = book.find("p", class_="price_color").text.strip().replace("Â£", "").replace("£", "")

        rating_classes = book.find("p", class_="star-rating")["class"]
        rating = rating_classes[1]  # One, Two, Three, Four, Five

        products.append({
            "Product Name": name,
            "Price": price,
            "Rating": rating
        })

    # Create DataFrame
    df = pd.DataFrame(products)

    # Save CSV with Excel-compatible UTF-8 encoding
    df.to_csv("products.csv", index=False, encoding="utf-8-sig")

    print("=================================")
    print("Web Scraping Completed Successfully")
    print("CSV File Saved: products.csv")
    print(f"Total Products: {len(products)}")
    print("=================================")

else:
    print("Failed to retrieve the webpage.")
    print("Status Code:", response.status_code)