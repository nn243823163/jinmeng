#coding:utf-8
from __future__ import unicode_literals
from django.db import models
import time

# Create your models here.

class HK_JYS(models.Model):
    time_hk = models.TimeField()
    data1 = models.IntegerField()
    data2 = models.IntegerField()
    data3 = models.CharField(max_length=4)
    save_date = models.DateTimeField(default=time.time())
    class Meta:
        db_table = 'J03_01_C_T60'
        verbose_name = '香港交易所'

    def __str__(self):
        return str(self.time_hk)