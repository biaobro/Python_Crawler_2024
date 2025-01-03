import scrapy
from scrapy_splash import SplashRequest


class AdamchoiSpider(scrapy.Spider):
    name = "adamchoi"
    allowed_domains = ["www.adamchoi.co.uk"]
    # start_urls = ["https://www.adamchoi.co.uk/overs/detailed"]

    script = '''
        function main(splash, args)
          -- splash:set_user_agent('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36')
          --[[
          headers = {
            ['USER_AGENT'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
          }
          --]]
          splash:on_request(function(request)
            request:set_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36')
          end)
          
          splash:set_custom_headers(headers)
          splash.private_mode_enabled = false
          assert(splash:go(args.url))
          assert(splash:wait(3))
          all_matches = assert(splash:select_all('label.btn.btn-sm.btn-primary'))
          all_matches[2]:mouse_click()
          assert(splash:wait(3))
          splash:set_viewport_full()
          return {
            splash:html(),
            splash:png()
          }
        end
    '''

    def start_requests(self):
        yield SplashRequest(
            url='https://www.adamchoi.co.uk/overs/detailed',
            callback=self.parse,
            endpoint='execute',
            args={'lua_source': self.script}
        )

    def parse(self, response):
        print(response.body)
        rows = response.xpath('//tr')
        for row in rows:
            date = row.xpath('./td[1]/text()').get()
            home_team = row.xpath('./td[2]/text()').get()
            score = row.xpath('./td[3]/text()').get()
            away_team = row.xpath('./td[4]/text()').get()

            yield {
                'date': date,
                'home_team': home_team,
                'score': score,
                'away_team': away_team
            }
