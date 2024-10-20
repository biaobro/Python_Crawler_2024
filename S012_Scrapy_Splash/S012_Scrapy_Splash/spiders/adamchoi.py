import scrapy


class AdamchoiSpider(scrapy.Spider):
    name = "adamchoi"
    allowed_domains = ["www.adamchoi.co.uk"]
    start_urls = ["https://www.adamchoi.co.uk/overs/detailed"]

    def parse(self, response):
        pass
