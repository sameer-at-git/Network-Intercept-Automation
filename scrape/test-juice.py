import os
import csv
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

options = Options()
service = Service("./chromedriver.exe")  
driver = webdriver.Chrome(service=service, options=options)
driver.get("http://localhost:3000")
driver.quit()

products = []
page = 0

while True:
    r = requests.get(f"http://localhost:3000/rest/products/search?q={page}")
    batch = r.json().get("data", [])
    if not batch:
        break
    products.extend(batch)
    page += 1

if not os.path.exists("images"):
    os.makedirs("images")

missing_images = 0

for p in products:
    image_name = p.get("image","")
    if image_name:
        image_url = f"http://localhost:3000/assets/public/images/products/{image_name}"
        try:
            resp = requests.get(image_url)
            if resp.status_code == 200:
                with open(os.path.join("images", image_name), "wb") as f:
                    f.write(resp.content)
            else:
                missing_images += 1
        except:
            missing_images += 1
    else:
        missing_images += 1

with open("juice_shop_products.csv","w",newline="",encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["id","name","description","price","deluxePrice","image","createdAt","updatedAt","deletedAt"])
    for p in products:
        writer.writerow([
            p.get("id",""),
            p.get("name",""),
            p.get("description",""),
            p.get("price",""),
            p.get("deluxePrice",""),
            p.get("image",""),
            p.get("createdAt",""),
            p.get("updatedAt",""),
            p.get("deletedAt","")
        ])

print(f"Total products: {len(products)}")
print(f"Products missing images: {missing_images}")
