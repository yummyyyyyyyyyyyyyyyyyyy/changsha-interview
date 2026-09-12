import json
import requests

url = f"https://roark.com/products/mens-bless-up-breathable-stretch-shirt-fossil-print.js"

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json, text/plain, */*",
}

resp = requests.get(url, headers=headers, timeout=15)
resp.raise_for_status()
product = resp.json()


def fmt_price(cents):
    if cents is None:
        return None
    return f"${cents / 100:.2f}"


name = product["title"]

price = fmt_price(product.get("price"))

compare_at_price = fmt_price(product.get("compare_at_price"))

images = ["https:" + img if img.startswith("//") else img for img in product.get("images", [])]

options = {opt["name"]: opt["values"] for opt in product.get("options", [])}
color = options.get("Color", [])

variants = product.get("variants", [])
first_variant = next((v for v in variants if v.get("available")), variants[0] if variants else None)
current_color = first_variant.get("option1") if first_variant else (color[0] if color else None)

size = options.get("Size", [])

print("=" * 60)
print(f"name===>   : {name}")
print(f"price===>      : {price}   (划线价: {compare_at_price})")
print(f"Color===>: {current_color}")
print(f"Size===>    : {size}")
print(f"images==>  : 共 {len(images)} 张")
for i, img in enumerate(images, 1):
    print(f"    [{i}] {img}")
