# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from peewee import *
from playhouse.db_url import connect

db = connect('mysql://root:@127.0.0.1:3306/jinmeng_scrapy')  # 连接数据库

class HK_JYS(Model):
    time_hk = CharField()
    data1 = CharField()
    data2 = CharField()
    data3 = CharField()

    class Meta:
        database = db  # 要连接的数据库
        db_table = 'J03_01_C_T60'  # 要映射的数据表,名称与原表一致


class JinmengPipeline(object):
    def process_item(self, item, spider):

        item_time = item['time_item']
        item_data1 = item['data1']
        item_data2 = item['data2']
        item_data3 = item['data3']

        hk_jys = HK_JYS(time_hk = item_time,data1 = item_data1,data2 = item_data2,data3 = item_data3)
        hk_jys.save()
        print 'nnn111'

        return item