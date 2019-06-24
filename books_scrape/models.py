"""
orm 类的封装层
"""
from books_scrape.orm_helper import MySqlOrmHealper, Base
from sqlalchemy import Column, String, Integer, ForeignKey

import json
import random

class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    book_title = Column(String(200))    # 书籍标题
    image_url = Column(String(200)) # 图片地址
    book_url = Column(String(300))   # 详情页
    book_price = Column(String(10))

    def __str__(self):
        mdict = dict(id=self.id, book_title=self.book_title, image_url=self.image_url,
                     book_price=self.book_price)
        return json.dumps(mdict)   # 字典转换成字符串


if __name__ == '__main__':
    minst = MySqlOrmHealper()
    session = minst.create_session()
    print(session)

    book_list = []
    for i in range(10):
        book = Book(book_title=f'book_title{i}', image_url=f'image_url{i}', book_price=random.randint(20, 100),
                    book_url=f'http://book-{i}.com')
        book_list.append(book)

    minst.add_records(session, book_list)
