import csv
import html
import re

import requests

url = "https://www.cosrx.com/collections/all/products.json"
csv_path = "cosrx_products.csv"
headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
    )
}

products = []
for page in range(1, 6):
    resp = requests.get(url, params={"page": page}, headers=headers, timeout=30)
    products += resp.json()["products"]
    print(f"page={page} -> {len(resp.json()['products'])} 条")

products = [p for p in products if p["product_type"] != "FREEGIFT_HIDDEN" and "Not available" not in p["tags"]]
print(f"合计 {len(products)} 条在售商品")


def to_text(body_html):
    text = re.sub(r"<(?:br|/p|/div|/h[1-6]|/li|/tr|/td)[^>]*>", "\n", body_html or "", flags=re.I)
    text = html.unescape(re.sub(r"<[^>]+>", " ", text)).replace("\xa0", " ")
    return "\n".join(line for line in (re.sub(r"\s+", " ", x).strip() for x in text.split("\n")) if line)


def pick(text, label):
    match = re.search(rf"(?:^|\n)\s*{label}\s*[:：]\s*(.+)", text, re.I)
    stop = r"(?:Size|Color|How\s+to\s+Use|Directions|Full\s+Ingredients|Ingredients|Notice)\s*[:：]"
    return re.split(stop, match.group(1), maxsplit=1, flags=re.I)[0].strip(" -–—|") if match else ""


rows = []
for product in products:
    text = to_text(product["body_html"])

    # 价格：
    price = min(float(v["price"]) for v in product["variants"])
    compare = max([float(v["compare_at_price"]) for v in product["variants"] if v["compare_at_price"]] or [0])
    price = max(price, compare)

    # 图片
    images = ",".join(
        "https:" + img["src"] if img["src"].startswith("//") else img["src"] for img in product["images"]
    )

    # 尺码：
    sizes = [
        value
        for option in product["options"]
        if re.search(r"size|volume", option["name"], re.I)
        for value in option["values"]
    ]

    rows.append({
        "name": product["title"],
        "price": f"${price:.2f}",
        "images": images,
        "Key Ingredients": pick(text, r"Key\s+Ingredients?") or pick(text, "Ingredients"),
        "Size": ",".join(dict.fromkeys(sizes)) or pick(text, "Size"),
    })

with open(csv_path, "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(f, fieldnames=["name", "price", "images", "Key Ingredients", "Size"])
    writer.writeheader()
    writer.writerows(rows)

print(f"已写入 {len(rows)} 条 -> {csv_path}")
