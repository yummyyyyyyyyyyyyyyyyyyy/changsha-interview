import csv

import requests

url = "https://www.questnutrition.com/collections/protein-bars-all/products.json"
csv_path = "quest_products.csv"
headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
    )
}

resp = requests.get(url, headers=headers, timeout=15)
products = resp.json()["products"]
print(f"共 {len(products)} 个产品")

rows = []
for product in products:
    ids = []
    for variant in product["variants"]:
        ids.append(str(variant["id"]))

    row = {
        "handle": product["handle"],
        "title": product["title"],
        "id": ",".join(ids),
    }
    rows.append(row)

with open(csv_path, "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(f, fieldnames=["handle", "title", "id"])
    writer.writeheader()
    writer.writerows(rows)

print(f"已写入 {len(rows)} 条 -> {csv_path}")
