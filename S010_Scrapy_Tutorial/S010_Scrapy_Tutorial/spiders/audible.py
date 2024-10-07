import scrapy


class AudibleSpider(scrapy.Spider):
    name = "audible"
    allowed_domains = ["www.audible.com"]
    start_urls = ["https://www.audible.com/search"]

    def parse(self, response):
        # xpath 无法定位到 class 包含2个以及以上值时的情况
        # 需要改用 contains
        products = response.xpath('//li[contains(@class, "productListItem")]')
        for product in products:
            # 注意 // 和 / 的区别，
            # // 是遍历所有，包括子级 和 子子级别
            # / 是指定路径

            # 有些book有多个作者，所以用 getall()
            title = product.xpath('.//h3//a/text()').get().strip()
            author = product.xpath('.//li[contains(@class, "authorLabel")]/span/a/text()').getall()
            length = product.xpath('.//li[contains(@class, "runtimeLabel")]/span/text()').get().strip()
            releaseDate = product.xpath('.//li[contains(@class, "releaseDateLabel")]/span/text()').get().replace(' ', '').replace('\n','')
            language = product.xpath('.//li[contains(@class, "languageLabel")]/span/text()').get().replace(' ', '').replace('\n','')

            # 不是所有Book都有rating，需要考虑失败的情况
            # rating = product.xpath('.//li[contains(@class, "ratingsLabel")]/span[2]/text()').get().strip()

            yield {
                'title': title,
                'author': author,
                'length': length,
                'releaseDate': releaseDate,
                'language': language,
                # 'rating': rating
            }
