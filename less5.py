import scrapy
from scrapy.http import Response

class DivannewparsSpider(scrapy.Spider):
    name = 'divannewpars'
    allowed_domains = ['market-sveta.ru']
    start_urls = ['https://www.market-sveta.ru/category/ljustry-podvesnye/']

    def parse(self, response: Response):
        lamps = response.css('div.product-item')
        for i, lamp in enumerate(lamps, start=1):
            name = lamp.css('div.name a::text').get()
            price = lamp.css('div.price.ys_p::text').get()
            url = lamp.css('a').attrib['href']
            name = name.strip() if name else None
            price = price.strip() if price else None
            url = url.strip() if url else None
            print(f"Lamp {i}: Name: {name}, Price: {price}, URL: {url}")
            yield {
                'name': name,
                'price': price,
                'url': url
            }




