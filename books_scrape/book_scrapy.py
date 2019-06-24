"""
controller控制层
爬取网页页面的数据，分析页面数据，保存db
（1）爬取页面的数据，采用requests
（2）解析， xpath,bs4
（3）保存db, sqlachemy orm
"""

import requests

from lxml import etree

from bs4 import BeautifulSoup as BSP4

from books_scrape.orm_helper import MySqlOrmHealper

from books_scrape.models import Book

from books_scrape.config import *

headers = {
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
}


class BooksScrapyProcesser(object):
    def __init__(self):
        self.__minst = MySqlOrmHealper()
        self.__session = self.__minst.create_session()

    def parse_url(self, path):
        if path.startswith('catalogue'):
            path = f"{DOMAIN}{path}"
        else:
            path = f'{DOMAIN}catalogue/{path}'
        return path

    def fetch_web_site(self, url):
        print(f"current fetch url:{url}")
        response = requests.get(url)   # text--str  ,  content --- bytes
        html_doc = response.text
        html_tree = etree.HTML(html_doc)     # 将requests获取到的页面数据转化成树形结构的xpath对象

        book_li_list = html_tree.xpath("//article[@class='product_pod']")
        for book in book_li_list:
            book_detail = book.xpath("./div[@class='image_container']/a/@href")[0]
            book_detail = self.parse_url(book_detail)
            image_url = DOMAIN +'catalogue/'+ book.xpath("./div[@class='image_container']/a/img/@src")[0]
            image_url = self.parse_url(image_url)
            book_title = book.xpath("./h3/a/text()")[0]
            book_price = book.xpath("./div[2]/p[1]/text()")[0]

            book = Book(book_title=book_title, image_url=image_url, book_url=book_detail,book_price=book_price)
            self.__minst.add_records(self.__session, book)

        # get next page
        next_page_node = html_tree.xpath("//ul[@class='pager']/li[@class='next']/a/@href")

        if len(next_page_node) > 0:
            next_node = next_page_node[0]
            next_url = self.parse_url(next_node)
            self.fetch_web_site(next_url)
        else:
            print('NO')


url = 'http://books.toscrape.com'
my_scrapy = BooksScrapyProcesser()
my_scrapy.fetch_web_site(url)
