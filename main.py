import requests
from bs4 import BeautifulSoup
import pandas as pd
base_url = "http://www.thewhiskyexchange.com"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"
}
url = "https://www.thewhiskyexchange.com/c/35/japanese-whisky"
r = requests.get(url).content
soup = BeautifulSoup(r, "lxml")
products = soup.find_all("li", class_="product-grid__item")
products_full_links_list = []
for product in products:
    tail = product.find("a", href=True)["href"]
    full_url = base_url + tail
    products_full_links_list.append(full_url)
products = []
for link in products_full_links_list:
    r = requests.get(link, headers=headers).content
    soup = BeautifulSoup(r, "lxml")
    product_info_dict = {
        "title": soup.find("h1", class_="product-main__name").text,
        "description": soup.find("div", class_="product-main__description").text,
        "availability": soup.find("p", class_="product-action__stock-flag").text,
        "price": soup.find("p", class_="product-action__price").text,

    }
    try:
        product_info_dict["rating"] = soup.find("span", class_="review-overview__rating star-rating star-rating--35").text
    except:
        product_info_dict["rating"] = "no rating"

    products.append(product_info_dict)
df = pd.DataFrame(products)
df.to_csv("products.csv", index=False)




