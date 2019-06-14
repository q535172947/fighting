# -*- coding: utf-8 -*-
import scrapy
from demSpider.items import DemspiderItem

class SpidersSpider(scrapy.Spider):
    name = 'spiders'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        quotes = response.css('.quote')             # ( .) 代表class
        item = DemspiderItem()
        for quote in quotes:
            text = quote.css('.text::text').extract_first()             # ::text  代表取文本
            author = quote.css('.author::text').extract_first()         # extract_first 取数组的第一个字符串
            tags = quote.css('.tags a::text').extract()                 # extract()字符串列表
            item['text'] = text
            item['author'] = author
            item['tags'] = tags
            yield item
        next_page = response.css('.pager .next a::attr(href)').extract_first()
        url = response.urljoin(next_page)  # 把基地址和相对地址智能连接成一个绝对地址
        yield scrapy.Request(url, callback=self.parse)
