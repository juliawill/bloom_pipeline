import csv
from pathlib import Path
# 
import requests
from bs4 import BeautifulSoup

HEADERS = {"User-Agent": "Mozilla/5.0"}

def fetch_html(url: str) -> str:
    r = requests.get(url, headers=HEADERS, timeout=30)
    r.raise_for_status()
    return r.text

def parse_sephora_reviews(html: str):
    soup = BeautifulSoup(html, "html.parser")
    # NOTE: selectors will likely need adjusting per product page
    blocks = soup.select("[data-comp='Review']") or []
    for b in blocks:
        text = b.get_text(" ", strip=True)
        if text:
            yield {"rating": None, "review_text": text, "review_date": None}
            print(text)

def save_csv(rows, path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["source", "brand", "product", "url", "rating", "review_text", "review_date"])
        w.writeheader()
        for r in rows:
            w.writerow(r)

def run(url: str, brand: str, product: str, out_csv: str):
    # call API
    html = fetch_html(url)
    reviews = []
    for r in parse_sephora_reviews(html):
        reviews.append({
            "source": "sephora",
            "brand": brand,
            "product": product,
            "url": url,
            "rating": r["rating"],
            "review_text": r["review_text"],
            "review_date": r["review_date"],
        })
    save_csv(reviews, Path(out_csv))
    print(f"Saved {len(reviews)} reviews to {out_csv}")

if __name__ == "__main__":

    urls = [
    ("https://www.sephora.com/product/pro-filtr-soft-matte-longwear-foundation-P87985432?skuId=2164697", "Fenty Beauty", "Pro Filt'r - 498 Very Rich"),
    ("https://www.sephora.com/product/pro-filtr-soft-matte-longwear-foundation-P87985432?skuId=2164689", "Fenty Beauty", "Pro Filt'r - 495 Very Deep Cool"),
    ("https://www.sephora.com/product/pro-filtr-soft-matte-longwear-foundation-P87985432?skuId=1925510", "Fenty Beauty", "Pro Filt'r - 495 Very Deep Neutral"),
    ("https://www.sephora.com/product/pro-filtr-soft-matte-longwear-foundation-P87985432?skuId=2590081", "Fenty Beauty", "Pro Filt'r - 485 Neutral"),

    # add more
    ]

for url, brand, product in urls:
    run(url, brand, product, f"data/{brand}_{product}.csv")
