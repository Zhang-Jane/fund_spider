# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import json
import os
import traceback

import pymysql
from pymysql.err import Error
from itemadapter import ItemAdapter
from scrapy.crawler import logger


class OrientalWealthPipeline:
    @classmethod
    def from_crawler(cls, crawler):
        """
        创建pipeline对象,读取配置文件
        :param crawler:crawler.settings就是settings配置文件
        :return:
        """
        # settings中的配置名称必须大写
        db_host = crawler.settings.get('MYSQL_HOST')
        port = crawler.settings.get('MYSQL_POST')
        database = crawler.settings.get('MYSQL_DATABASE')
        fund_data_table = crawler.settings.get('FUND_DATA_TABLE')
        fund_rate_table = crawler.settings.get('FUND_RATE_TABLE')
        fund_equity_table = crawler.settings.get('FUND_EQUITY_TABLE')
        return cls(db_host, port, database, fund_data_table,
                   fund_rate_table, fund_equity_table)

    def __init__(self, db_host, port, database, fund_data_table,
                 fund_rate_table, fund_equity_table):
        """
        数据初始化
        :param db_host:
        """
        self.cursor = None
        self.connect = None
        self.db_host = db_host
        self.port = port
        self.database = database
        self.user = os.environ.get('MYSQL_USERNAME', '')
        self.passwd = os.environ.get('MYSQL_PASSWORD', '')
        self.fund_data_table = fund_data_table
        self.fund_rate_table = fund_rate_table
        self.fund_equity_table = fund_equity_table

    def open_spider(self, spider):
        """
        爬虫开始执行时，建立数据连接
        :param spider:
        :return:
        """
        if self.user and self.passwd:
            self.connect = pymysql.connect(
                host=self.db_host,
                db=self.database,
                port=self.port,
                user=self.user,
                passwd=self.passwd,
                charset='utf8'
            )
            self.cursor = self.connect.cursor()
        else:
            raise Error('数据库账号或密码错误')

    def insert_data2mysql(self, sql):
        try:
            self.cursor.execute(sql)
            self.connect.commit()
        except Exception:
            self.connect.rollback()
            traceback.print_exc()

    def process_item(self, item, spider):
        """
        用于持久化存储数据，操作数据
        :param item:
        :param spider:
        :return:
        """
        if spider.name == 'dongfang_funds':
            vaules = (item.get('fund_code'), item.get('fund_name'), json.dumps(item))
            sql = f"INSERT INTO {self.fund_data_table} (fund_id, fund_title, info) VALUES {vaules}"
            self.insert_data2mysql(sql)
            print(f"正在存储1：{spider.name:=^30}")
        elif spider.name == 'fund_rate_info':
            vaules = (item.get('fund_code'), item.get('fund_name'), json.dumps(item))
            sql = f"INSERT INTO {self.fund_rate_table} (fund_id, fund_title, info) VALUES {vaules}"
            self.insert_data2mysql(sql)
            print(sql)
            print(f"正在存储2：{spider.name:=^30}")
        elif spider.name == 'fund_units_cumulative_equity':
            vaules = (item.get('fund_code'), item.get('fund_name'), json.dumps(item))
            sql = f"INSERT INTO {self.fund_equity_table} (fund_id, fund_title, info) VALUES {vaules}"
            self.insert_data2mysql(sql)
            print(f"正在存储3：{spider.name:=^30}")
        print(item)

        # 交给下一个pipline进行处理
        return item

    def close_spider(self, spider):
        """
        爬虫关闭时，关闭数据连接
        :param spider:
        :return:
        """
        if self.connect:
            self.connect.close()
