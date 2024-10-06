import scrapy


class WorldpopulationbycountrySpider(scrapy.Spider):
    name = "worldpopulationbycountry"
    allowed_domains = ["www.worldometers.info"]
    start_urls = ["https://www.worldometers.info/world-population/population-by-country"]

    def parse(self, response):
        title = response.xpath('//h1/text()').get()

        # 得到国家名称列表，结果是字符串列表
        # countries = response.xpath('//td/a/text()').getall()

        # 得到国家 xpath 对象
        countries = response.xpath('//td/a')

        for country in countries:
            countryName = country.xpath(".//text()").get()
            countryLink = country.xpath(".//@href").get()

            yield {
                # 'title': title,
                'countryName': countryName,
                'countryLink': countryLink
            }
