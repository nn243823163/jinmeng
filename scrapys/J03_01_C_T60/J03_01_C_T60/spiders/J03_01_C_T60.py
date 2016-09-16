# -*- coding: utf-8 -*-
import scrapy
import os
from ..items import J0301CT60Item
import re
from scrapy.http import Request
import time
from peewee import *
from playhouse.db_url import connect
import logging.handlers

db = connect('mysql://root:@127.0.0.1:3306/jinmeng_scrapy')  # 连接数据库

#设置连接数据表
class CONTROLER(Model):
    id = PrimaryKeyField()
    time_interval = IntegerField()
    time_start = TimeField()
    time_stop = TimeField()
    use_days = CharField()
    holidays_used = BooleanField()
    status = CharField()
    last_run_time = DateTimeField()
    class Meta:
        database = db  # 要连接的数据库
        db_table = 'controler'  # 要映射的数据表,名称与原表一致

hk_controler = CONTROLER.get(CONTROLER.id == 1)


class DmozSpiderSpider(scrapy.Spider):
    name = "jinmeng"
    # allowed_domains = ["dmoz.org"]
    allowed_domains = ["http://www.hkex.com.hk/"]
    start_urls = (
        'http://www.hkex.com.hk//eng/csm/script/en_QuotaUsage.js?Token=53343',
    )

    #设置多个页面
    # def start_requests(self):
    #     reqs = []
    #     for i in range(1,10):
    #         req = scrapy.Request("http://www.hkex.com.hk//eng/csm/script/en_QuotaUsage.js?Token=53343")
    #         reqs.append(req)
    #     return reqs

    def parse(self, response):
        try:
            time_re = re.search(r"as at (\d\d:\d\d)", response.body)
            time_re = time_re.group(1)
            datas = re.findall(r"(\d\d,\d\d\d) Mil", response.body)
            data1 = datas[0].replace(',','')
            data2 = datas[1].replace(',','')
            data3 = re.findall(r"\d{3}%|\d{2}%|\d{1}%", response.body)[0]
            item = J0301CT60Item()
            item['time_item'] = time_re
            item['data1'] = data1
            item['data2'] = data2
            item['data3'] = data3

            # 以下为测试peewee读取controler数据表
            # item = J0301CT60Item()
            # item['time_item'] = hk_controler.time_start
            # item['data1'] = hk_controler.id
            # item['data2'] = hk_controler.id
            # item['data3'] = hk_controler.id

            # 设置时间间隔
            # time.sleep(hk_controler.time_interval)
            # 更改状态
            hk_controler.status = '正常工作'
            # 更改最后执行时间
            hk_controler.last_run_time = time.strftime('%Y-%m-%d %H:%M:%S ',time.localtime(time.time()))
            hk_controler.save()

            yield item
            ####配置循环执行####
            # yield Request(url=self.start_urls[0], callback=self.parse,dont_filter=True) #设置不过滤重复网址

        except Exception as e1:
            try:
                # time.sleep(hk_controler.time_interval)
                print '出错,错误1是:',e1  #这里可以输出到控制台

                # 更改状态
                hk_controler.status = '发生错误'
                # 更改最后执行时间
                hk_controler.last_run_time = time.strftime('%Y-%m-%d %H:%M:%S ',time.localtime(time.time()))
                hk_controler.save()

                #记录日志
                LOG_FILE = 'J03_01_C_T60.log'
                handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=1024 * 1024, backupCount=5)  # 实例化handler
                fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s'
                formatter = logging.Formatter(fmt)  # 实例化formatter
                handler.setFormatter(formatter)  # 为handler添加formatter
                logger = logging.getLogger('J03_01_C_T60')  # 获取名为tst的logger
                logger.addHandler(handler)  # 为logger添加handler
                logger.setLevel(logging.INFO)
                logger.info(e1)

                print '退出1'
                # yield Request(url=self.start_urls[0], callback=self.parse,dont_filter=True) #设置不过滤重复网址

            except Exception as e2:
                # yield Request(url=self.start_urls[0], callback=self.parse,dont_filter=True) #设置不过滤重复网址
                print '出错,错误2是:',e2  #这里可以输出到控制台
                print '退出2'