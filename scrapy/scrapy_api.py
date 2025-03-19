from fastapi import FastAPI
import scrapy
from scrapy.crawler import CrawlerProcess
import json
import os
from scrapy.utils.project import get_project_settings
from threading import Thread

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.get("/scrape")
def scrape(url: str):
    class CompanySpider(scrapy.Spider):
        name = 'company_spider'
        
        def start_requests(self):
            yield scrapy.Request(url, self.parse)
        
        def parse(self, response):
            title = response.xpath('//title/text()').get()
            yield {"title": title}

    # Run the Scrapy crawl in a separate thread
    def run_spider():
        process = CrawlerProcess(get_project_settings())
        process.crawl(CompanySpider, start_urls=[url])
        process.start()

    # Start the crawl in a separate thread to avoid blocking FastAPI
    thread = Thread(target=run_spider)
    thread.start()

    # Wait for the thread to finish
    thread.join()

    # Now, return the scraped data
    if os.path.exists('output.json'):
        with open('output.json', 'r') as file:
            scraped_data = json.load(file)
        return {"data": scraped_data}
    else:
        return {"error": "Scraping failed, no data found."}
