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

            # yield {
            #     # 'title': title,
            #     'countryName': countryName,
            #     'countryLink': countryLink
            # }

            # 绝对地址，有2种方式
            # absUrl = f'https://www.worldometers.info/{countryLink}'
            # absUrl = response.urljoin(countryLink)
            # yield scrapy.Request(absUrl)

            # 相对地址
            # callback 直接写函数名称，不要带括号
            yield response.follow(url=countryLink, callback=self.parseCountry, meta={'countryName': countryName})

    def parseCountry(self, response):
        country = response.request.meta['countryName']
        # 得到的结果取第1个元素，是[1]，不是[0]
        table = response.xpath('(//table[contains(@class, "table-list")])[1]')
        rows = table.xpath('.//tbody/tr')

        for row in rows:
            year = row.xpath('.//td[1]/text()').get()
            population = row.xpath('.//td[2]/strong/text()').get()

            yield {
                'country': country,
                'year': year,
                'population': population
            }
