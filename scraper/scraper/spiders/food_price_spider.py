import scrapy
import os
from urllib.parse import urljoin

class FoodPricesSpider(scrapy.Spider):
    name = "food_prices"
    start_urls = ["https://www.nigerianstat.gov.ng/elibrary"]

    def parse(self, response):
        for row in response.css("tr"):
            row_text = "".join(row.css("td *::text").getall()).lower()
            if "food prices" in row_text:
                link = row.css("td a::attr(href)").get()
                if link:
                    full_link = urljoin(response.url, link)
                    yield scrapy.Request(full_link, callback=self.parse_dataset_page)

    def parse_dataset_page(self, response):
        for link in response.css("a::attr(href)").getall():
            if link.endswith(".xlsx"):
                full_link = urljoin(response.url, link)
                yield scrapy.Request(full_link, callback=self.save_file)

    def save_file(self, response):
        filename = response.url.split("/")[-1]
        raw_dir = "data/raw"
        os.makedirs(raw_dir, exist_ok=True)
        file_path = os.path.join(raw_dir, filename)
        with open(file_path, "wb") as f:
            f.write(response.body)
        self.log(f"Saved file: {file_path}")
