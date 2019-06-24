"""
ORM 功能封装
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from books_scrape.config import DB_SET_MAP

# 初始化数据库连接
mysql_conn_str = f"mysql+pymysql://{DB_SET_MAP['user']}:{DB_SET_MAP ['password']}@{DB_SET_MAP['host']}:" \
    f"{DB_SET_MAP['port']}/{DB_SET_MAP['db']}?charset=utf8"
engine = create_engine(mysql_conn_str)

# 产生一个model基础类,凡是继承了base类，具有orm特征
Base = declarative_base()

"""
定义一个mysql orm 操作类，提供增删改查等操作功能
"""

class MySqlOrmHealper(object):

    def __create_db_table(self):
        """
        同步，orm类 ---》 mysql同步
        :return:
        """
        Base.metadata.create_all(engine)

    def create_session(self):
        """
        创建session对象
        :return:
        """
        self.__create_db_table()
        Session = sessionmaker(bind=engine)  # 引擎绑定过来
        return Session()   # 返回实例化对象

    def add_records(self, session, objs):
        """
        添加orm对象到数据库中，支持单个插入和批量插入
        :param session:
        :param objs: object, [object1, object2]
        :return:
        """
        if isinstance(objs, list):   # 是列表，多个对象， 批量增加
            session.add_all(objs)
        else:                       # 单个对象， 单个增加
            session.add(objs)
        session.commit()            # 提交

    def update_record(self, session, Cls, cd_field, cd_value, up_dict):
        """
        更新数据库，
        :param session:
        :param Cls: 要更新的orm类（Student）
        :param cd_field: 要更新的条件字段(Student.id)
        :param cd_value: 要更新的条件值(10)
        :param up_dict: 更新的字典（{‘age’:20}）
        :return:
        """
        # django :rom Student.objects.filter()
        flag = session.query(Cls).filter(cd_field=cd_value).update(up_dict)
        if flag:
            session.commit()
            return True
        else:
            return False


    def query_record(self, session, Cls):
        """
        查询orm类中所有记录数
        :param session:
        :param Cls:
        :return:
        """
        return session.query(Cls).all()

    def query_condition(self, session, Cls, cd_field, cd_value):
        """
        查询满足条件的db数据
        :param session:
        :param Cls:
        :param cd_field:
        :param cd_value:
        :return:
        """
        return session.query(Cls).filter(cd_field=cd_value)

    def delete_records(self, session, Cls, cd_field, cd_value):
        """
        删除数据库的元素
        :param session:
        :param Cls:
        :param cd_field:
        :param cd_value:
        :return:
        """
        flag = session.query(Cls).filter(cd_field=cd_value).delete()
        if flag:
            session.commit()
            return True
        else:
            return False