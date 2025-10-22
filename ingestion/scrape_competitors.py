import csv
import json
import re
from pathlib import Path
from typing import Dict, Iterable, Iterator, List, Optional
import requests


HEADERS = {"User-Agent": "Mozilla/5.0"}
BV_CONFIG_PATTERN = re.compile(r"Sephora\.configurationSettings\s*=\s*(\{.*?\});", re.S)
PRODUCT_ID_PATTERN = re.compile(r"(P\d+)")
BV_API_URL = "https://api.bazaarvoice.com/data/reviews.json"
PAGE_SIZE = 100
MAX_REVIEWS_PER_PRODUCT = 500  # prevent pulling all 17k reviews unless we really need them


def fetch_html(url: str) -> str:
    response = requests.get(url, headers=HEADERS, timeout=30)
    response.raise_for_status()
    return response.text


def extract_bv_config(html: str) -> Dict[str, Dict[str, str]]:
    match = BV_CONFIG_PATTERN.search(html)
    if not match:
        raise ValueError("Bazaarvoice configuration block not found.")
    return json.loads(match.group(1))


def extract_product_id(source: str) -> str:
    match = PRODUCT_ID_PATTERN.search(source)
    if not match:
        raise ValueError("Could not determine Sephora product id (P#######).")
    return match.group(1)


def fetch_reviews_from_bazaarvoice(
    product_id: str,
    passkey: str,
    api_version: str,
    max_reviews: Optional[int] = MAX_REVIEWS_PER_PRODUCT,
) -> Iterator[Dict[str, Optional[str]]]:
    fetched = 0
    offset = 0

    while True:
        if max_reviews is not None:
            remaining = max_reviews - fetched
            if remaining <= 0:
                break
            limit = min(PAGE_SIZE, remaining)
        else:
            limit = PAGE_SIZE

        params = {
            "apiversion": api_version,
            "Filter": f"ProductId:{product_id}",
            "Sort": "SubmissionTime:desc",
            "Limit": str(limit),
            "Offset": str(offset),
            "Stats": "Reviews",
            "Include": "Products",
            "PassKey": passkey,
        }
        response = requests.get(BV_API_URL, params=params, headers=HEADERS, timeout=30)
        response.raise_for_status()

        data = response.json()
        results = data.get("Results") or []
        if not results:
            break

        for item in results:
            text = (item.get("ReviewText") or "").strip()
            if not text:
                continue
            yield {
                "rating": item.get("Rating"),
                "review_text": text,
                "review_date": item.get("SubmissionTime"),
            }
            fetched += 1
            if max_reviews is not None and fetched >= max_reviews:
                break

        total_results = data.get("TotalResults") or 0
        if max_reviews is not None and fetched >= max_reviews:
            break

        offset += limit
        if offset >= total_results:
            break


def save_csv(rows: Iterable[Dict[str, str]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["source", "brand", "product", "url", "rating", "review_text", "review_date"],
        )
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def collect_reviews(url: str) -> Dict[str, str]:
    html = fetch_html(url)
    config = extract_bv_config(html)
    token_info = config.get("bvApi_review_page") or config.get("bvApi_rwdRating_desktop_read")
    if not token_info:
        raise ValueError("Unable to locate Bazaarvoice review token.")
    product_id = extract_product_id(url)
    return {
        "product_id": product_id,
        "passkey": token_info["token"],
        "api_version": token_info.get("version", "5.4"),
    }


def run(url: str, brand: str, product: str, out_csv: str, cache: Dict[str, List[Dict[str, Optional[str]]]]) -> None:
    product_id = extract_product_id(url)
    if product_id not in cache:
        bv_config = collect_reviews(url)
        reviews: List[Dict[str, Optional[str]]] = []
        for review in fetch_reviews_from_bazaarvoice(
            product_id=bv_config["product_id"],
            passkey=bv_config["passkey"],
            api_version=bv_config["api_version"],
        ):
            reviews.append(review)
        cache[product_id] = reviews

    rows = [
        {
            "source": "sephora",
            "brand": brand,
            "product": product,
            "url": url,
            "rating": review["rating"],
            "review_text": review["review_text"],
            "review_date": review["review_date"],
        }
        for review in cache[product_id]
    ]
    save_csv(rows, Path(out_csv))
    print(f"Saved {len(rows)} reviews to {out_csv}")


if __name__ == "__main__":
    urls = [
        (
            "https://www.sephora.com/product/pro-filtr-soft-matte-longwear-foundation-P87985432?skuId=2164697",
            "Fenty Beauty",
            "Pro Filt'r - 498 Very Rich",
        ),
        (
            "https://www.sephora.com/product/pro-filtr-soft-matte-longwear-foundation-P87985432?skuId=2164689",
            "Fenty Beauty",
            "Pro Filt'r - 495 Very Deep Cool",
        ),
        (
            "https://www.sephora.com/product/pro-filtr-soft-matte-longwear-foundation-P87985432?skuId=1925510",
            "Fenty Beauty",
            "Pro Filt'r - 495 Very Deep Neutral",
        ),
        (
            "https://www.sephora.com/product/pro-filtr-soft-matte-longwear-foundation-P87985432?skuId=2590081",
            "Fenty Beauty",
            "Pro Filt'r - 485 Neutral",
        ),
        # add more
    ]

    cache: Dict[str, List[Dict[str, Optional[str]]]] = {}
    for url, brand, product in urls:
        run(url, brand, product, f"data/{brand}_{product}.csv", cache)
