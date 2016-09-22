#coding:utf-8
import os

#进入虚拟环境
#####在命令行手动输入 source venv/bin/activate 进入虚拟环境
# os.chdir('/Users/doudou/Documents/jinmeng_prjs/scrapys')
# os.system('pwd')
# os.system('ls')
# os.system('pip list')
# os.system('source venv/bin/activate')
# os.system('pip list')

import time
from peewee import *
from playhouse.db_url import connect
import logging.handlers
import schedule
import threading


#数据库配置,关联数据表'controler'
db = connect('mysql://root:@127.0.0.1:3306/jinmeng_scrapy')  # 连接数据库

#设置连接控制数据表
class CONTROLER(Model):
    id = PrimaryKeyField()
    time_interval = IntegerField()
    time_start = TimeField()
    time_stop = TimeField()
    use_days = CharField()
    holidays_used = BooleanField()
    status = CharField()
    last_run_time = DateTimeField()
    run_or_not = CharField()
    class Meta:
        database = db  # 要连接的数据库
        db_table = 'controler'  # 要映射的数据表,名称与原表一致

# 定义多线程函数
def run_threaded(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()



#####读取爬虫J03_01_C_T60的控制数据
hk_controler = CONTROLER.get(CONTROLER.id == 1)

#####控制爬虫J03_01_C_T60函数#####
tag_J03_01_C_T60 = 1                #设置爬虫J03_01_C_T60是否运行,根据当前时间设置0或1
def scrapy_J03_01_C_T60():
    os.chdir('/Users/doudou/Documents/jinmeng_prjs/scrapys/J03_01_C_T60')
    # # os.system('pwd')
    # # os.system('scrapy list')
    if tag_J03_01_C_T60 :
        hk_controler.run_or_not = '正在运行'
        hk_controler.save()
        os.system('scrapy crawl jinmeng')         #通过屏蔽这句话控制爬虫是否启动
        print '一个定时爬虫任务结束'
    else:
        hk_controler.run_or_not = '停止运行'
        hk_controler.save()
        print '此时不在规定时间,爬虫关闭'

def set_tag_J03_01_C_T60_true():
    global tag_J03_01_C_T60
    tag_J03_01_C_T60 =1
    print '设置爬虫J03_01_C_T60开启'

def set_tag_J03_01_C_T60_false():
    global tag_J03_01_C_T60
    tag_J03_01_C_T60 = 0
    print '设置爬虫J03_01_C_T60关闭'
#####控制爬虫J03_01_C_T60函数结束#####

#####添加J03_01_C_T60的定时任务至多线程#####
schedule.every().day.at(str(hk_controler.time_start)[:-3]).do(set_tag_J03_01_C_T60_true)    #设置定时开启
schedule.every().day.at(str(hk_controler.time_stop)[:-3]).do(set_tag_J03_01_C_T60_false)    #设置定时开启
schedule.every(hk_controler.time_interval).seconds.do(run_threaded,scrapy_J03_01_C_T60)
#####添加J03_01_C_T60的定时任务至多线程语句结束#####



if __name__ == '__main__' :
    while 1:
        schedule.run_pending()





