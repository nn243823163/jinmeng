#coding:utf-8
import time
from peewee import *
from playhouse.db_url import connect

print time.strftime('%Y-%m-%d %H:%M:%S ',time.localtime(time.time()))

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
    class Meta:
        database = db  # 要连接的数据库
        db_table = 'controler'  # 要映射的数据表,名称与原表一致

hk_controler = CONTROLER.get(CONTROLER.id == 1)

time1 = str(hk_controler.time_start)[:-3]

print time1

