import scrapy
from scrapy_splash import SplashRequest


class LaptopSSpider(scrapy.Spider):
    name = "laptop_S"

    def start_requests(self):
        # laptops 商品列表页，splash渲染不出来，所以无法得到数据
        # url = 'https://www.lazada.com.my/tag/laptops/?spm=a2o4k.homepage.search.d_go'

        # 首页可以渲染得到
        url = 'https://www.lazada.com.my'
        yield SplashRequest(url)

    def parse(self, response):
        with open('with_splash.html', 'w') as f:
            f.write(response.body.decode())
        products_selector = response.css('a.link-ripple-container')
        print(products_selector, len(products_selector))
        for product in products_selector:
            yield {
                'img' : product.css('img::src').extract(),
                'name': product.css('p::text').get(),
                'price': product.css('span:contains("RM")::text').get(),
                # 'originPrice' :
                'itemDiscount' : product.css('span.itemDiscount::text').get()
            }
