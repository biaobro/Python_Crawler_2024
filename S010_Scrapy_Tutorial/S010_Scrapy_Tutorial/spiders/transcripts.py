import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class TranscriptsSpider(CrawlSpider):
    name = "transcripts"
    allowed_domains = ["subslikescript.com"]

    # 从A开始
    # start_urls = ["https://subslikescript.com/movies"]

    # 从A开始数据量太大，为了测试，从X开始
    start_urls = ["https://subslikescript.com/movies_letter-X"]

    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'

    # 初始化请求参数，增加user-agent
    def start_requests(self):
        yield scrapy.Request(url=self.start_urls[0], headers={
            'user-agent': self.user_agent
        })

    # follow：表示提取的链接请求完成后是否还要应用当前规则（boolean），如果为False则不会对提取出来的网页进行进一步提取，默认为False
    # 所以对于第一条规则详情页，不需要进一步匹配；
    # 但对于第二条规则列表页，需要进一步匹配是否有新的翻页按钮
    # process_request：链接请求预处理（添加header或cookie等）
    rules = (
        Rule(LinkExtractor(restrict_xpaths="//ul[@class='scripts-list']/li/a"), callback="parse_item", process_request='set_user_agent'),  # follow=True),# ),
        Rule(LinkExtractor(restrict_xpaths="(//a[@rel='next'])[1]"), follow=True, process_request='set_user_agent'),
    )

    def set_user_agent(self, request, spider):
        request.headers['User-Agent'] = self.user_agent
        return request

    def parse_item(self, response):
        # print(response.url)
        article = response.xpath("//article[@class='main-article']")
        yield{
            'title': article.xpath("./h1/text()").get(),
            'plot': article.xpath("./p/text()").get(),
            'transcript': article.xpath("./div[@class='full-script']/text()").getall(),
            'url': response.url,
        }
