from typing import Any, Optional, Union

import scrapy
from scrapy.http import Response
from twisted.internet.defer import Deferred

from lazada_P.items import JapaneseAnimeItem


class AnimerankSpider(scrapy.Spider):
    name = "animeRank"
    allowed_domains = ["www.douban.com"]
    start_urls = ["https://www.douban.com/doulist/45955373/"]
    max_pages = 2
    result = []

    def __init__(self, name: Optional[str] = None, **kwargs: Any):
        super().__init__(name, **kwargs)
        self.page_count = 1  # 计数器,默认

    def parse(self, response: Response, **kwargs: Any):
        """解析网页内容"""
        # 打印抓取的网页HTML
        listItems = response.xpath('//div[@class="article"]//div[@class="doulist-item"]')
        for item in listItems:
            ranking = item.xpath('.//span[@class="pos"]/text()').get()
            title = item.xpath('.//div[@class="title"]/a/text()').get()
            score = item.xpath('.//span[@class="rating_nums"]/text()').get()
            ratingPeople = item.xpath('.//div[@class="rating"]/span[last()]/text()').get()
            postImg = item.xpath('.//div[@class="post"]/a/img/@src').get()
            year = item.xpath('.//div[@class="abstract"]/text()').re_first(r'年份:\s*(\d+)')
            tmp = JapaneseAnimeItem()
            tmp["ranking"] = ranking.strip() if ranking else None
            tmp["title"] = title.strip() if title else None
            tmp["postImg"] = postImg.strip() if postImg else None
            tmp["year"] = year.strip() if year else None
            tmp["score"] = score.strip() if score else None
            tmp["ratingPeople"] = ratingPeople.strip() if ratingPeople else None
            self.result.append(tmp)
            yield tmp

        # 处理分页
        next_page = response.css('.next a::attr(href)').get()
        if next_page and self.page_count < self.max_pages:
            self.page_count += 1
            print(f"准备请求{self.page_count}页, 链接:{next_page}")
            yield scrapy.Request(url=next_page, callback=self.parse)

    def close(self, reason: str) -> Union[Deferred, None]:
        # 这里可以打印汇总后的数据
        print("result:", self.result)
        return super().close(self, reason)
