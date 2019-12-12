#!/usr/bin/python
# -*- coding: UTF-8 -*-

import json

import MySQLdb
import requests

# 打开数据库连接
db = MySQLdb.connect("localhost", "root", "123456", "stock", charset='utf8')


def get_url(begin):
    return "http://73.push2.eastmoney.com/api/qt/clist/get?cb=jQuery112409664470739603184_1576045911335&pn=%d&pz=20&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:0+t:6,m:0+t:13,m:0+t:80,m:1+t:2,m:1+t:23&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152&_=1576045911336" % (
        begin)


# 使用cursor()方法获取操作游标
cursor = db.cursor()


def get_insert_sql():
    return 'INSERT INTO sha_stock(NAME, NUMCODE, rank_num)VALUES(%s,%s, %s)'


def get_sha_stock():
    return 'select * from sha_stock'


def print_msg():
    sql = get_sha_stock()
    cursor.execute(sql)
    results = cursor.fetchall()
    for row in results:
        id = row[0]
        name = row[1]
        numcode = row[2]
        rank_num = row[3]
        print('id=%s,name=%s,numcode=%s,rank_num=%s' % (id, name, numcode, rank_num))


if __name__ == '__main__':
    for i in range(1, 195):
        #     # 发送get请求
        #    r = requests.get(get_url(i))
        #     print("第%s次,内容是%s" %(i,r.json()))
        r = requests.get(get_url(i))
        dict_str = json.loads(r.text[42:-2])
        diff = dict_str['data']['diff']
        for o in diff:
            name = o['f14']
            numcode = o['f12']
            sql = 'INSERT INTO sha_stock(NAME, NUMCODE, rank_num) values(\'%s\', \'%s\',%s)' % (name, numcode, 0)
            print(sql)
            cursor.execute(sql)
            print('第%s 次输出,股票名字  %s,  代码为   %s' % (i, o['f14'], o['f12']))
            db.commit()
    db.close()
