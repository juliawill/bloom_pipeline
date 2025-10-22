
from ingestion.scrape_competitors import run 
#needs the run function in this file


if __name__ == "__main__":
    urls = [
        ("https://www.sephora.com/product/pro-filtr-soft-matte-longwear-foundation-P87985432?skuId=2164697", "Fenty Beauty", "Pro Filt'r - 498 Very Rich"),
        ("https://www.sephora.com/product/pro-filtr-soft-matte-longwear-foundation-P87985432?skuId=2164689", "Fenty Beauty", "Pro Filt'r - 495 Very Deep Cool"),
        ("https://www.sephora.com/product/pro-filtr-soft-matte-longwear-foundation-P87985432?skuId=1925510", "Fenty Beauty", "Pro Filt'r - 495 Very Deep Neutral"),
        ("https://www.sephora.com/product/pro-filtr-soft-matte-longwear-foundation-P87985432?skuId=2590081", "Fenty Beauty", "Pro Filt'r - 485 Neutral"),
    ]

    for url, brand, product in urls:
        run(url, brand, product, f"data/{brand}_{product}.csv")



