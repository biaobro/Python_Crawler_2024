import scrapy


class WorldpopulationbycountrySpider(scrapy.Spider):
    name = "worldpopulationbycountry"
    allowed_domains = ["www.worldometers.info"]
    start_urls = ["https://www.worldometers.info/world-population/population-by-country"]

    def parse(self, response):
        title = response.xpath('//h1/text()').get()
        countries = response.xpath('//td/a/text()').getall()

        yield {
            'title': title,
            'countries': countries
        }
