#!/usr/bin/env python
# -*- coding=UTF-8 -*-
import sys

import pymysql

class BaseModel(object):

    def __init__(self,config):
        self.config = config
        self.conn = self.to_connect(self.config)
        self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)

    def __del__(self):
        self.conn.close()
        pass

    def to_connect(self,config):
        MYSQL_HOST = config.get('host')
        MYSQL_PORT = int(config.get('port',3306))
        MYSQL_USER = config.get('user')
        MYSQL_PASSWORD = str(config.get('password'))
        MYSQL_DATABASE = config.get('database')
        MYSQL_CHARSET = config.get('charset')
        MYSQL_TIMEOUT = int(config.get('timeout'))
        return pymysql.connect(host=MYSQL_HOST, port=MYSQL_PORT, user=MYSQL_USER, password=MYSQL_PASSWORD, database= MYSQL_DATABASE, charset= MYSQL_CHARSET, connect_timeout=MYSQL_TIMEOUT)

    def is_connected(self):
        """Check if the server is alive"""
        try:
            self.conn.ping(reconnect=True)
        except Exception as e:
            # print('重连mysql:{}'.format(str(e)))
            self.conn = self.to_connect(self.config)
            self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)

    # 获取一条
    def getOne(self, sql):
        self.is_connected()
        self.cursor.execute(sql)
        return self.cursor.fetchone()


    # 获取列表
    def getAll(self, sql):
        self.is_connected()
        self.cursor.execute(sql)
        return list(self.cursor.fetchall())


    # 插入更新一条
    def update_One(self, sql,data = []):
        self.is_connected()
        r = self.cursor.execute(sql,data)
        self.conn.commit()
        return r

    def update(self, table='news_c7f', data={} , where_data = {} , limit = 1):

        set_field = ','.join('`{}` = %s'.format(str(i)) for i in data)
        where_field = ','.join('`{}` = %s'.format(str(i)) for i in where_data)

        field_data = list(data[i] for i in data)
        field_data = field_data + list(where_data[i] for i in where_data)

        sql = """update {} set {} where {} limit {}""".format(table,set_field,where_field,limit)
        return self.update_One(sql, list(str(i) for i in field_data))

    def save(self, table='news_c7f', data={}):
        field_str = '`,`'.join(str(i) for i in data)
        field_val = ','.join('%s' for i in data)
        field_data = list(data[i] for i in data)
        sql = """INSERT IGNORE INTO {}(`{}`)  VALUE({})""".format(table, field_str, field_val)
        return self.update_One(sql, list(str(i) for i in field_data))

    # 插入更新多条
    def update_more(self, sql, items):
        self.is_connected()
        r = self.cursor.executemany(sql, items)
        self.conn.commit()
        return


    # 创建查询更新事务
    def select_and_update(self, s_sql, u_sql):
        self.is_connected()
        self.conn.begin()
        self.cursor.execute(s_sql)
        a = list(self.cursor.fetchall())
        b = tuple([i[-1] for i in a])
        if len(b) == 1:
            b = str(b).replace(',', '')
        elif len(b) > 1:
            b = str(b)
        else:
            return []
        self.cursor.execute(u_sql + b)
        self.conn.commit()
        return a

if __name__=='__main__':
    A = BaseModel()
    # print(A.getOne('select * from download_docs_list limit 1 for update;'))

    # print(A.getAll('select * from download_docs_list limit 2 for update;'))

    # A.update_One("INSERT IGNORE INTO `lyl`.`download_docs_list`(`url`, `doc_url`, `title`, `status`, `md5id`, `ref`, `ext`, `doc_dir`, `type`, `created_at`, `download_at`) VALUES ('1', '8', '6', '0', '4', '5', '6', '7', 8, 9, 0);")

    # A.update_more("INSERT IGNORE INTO `lyl`.`download_docs_list`(`url`, `doc_url`, `title`, `status`, `md5id`, `ref`, `ext`, `doc_dir`, `type`, `created_at`, `download_at`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);", [('1', '12', '6', '0', '4', '5', '6', '7', 8, 9, 0), ('1', '11', '6', '0', '4', '5', '6', '7', 8, 9, 0)])

    #print(A.select_and_update("select doc_url, filename, status, ext, site_url, id from download_docs_list where status in ('0', '1', '2') order by id limit 100 for update;", "UPDATE download_docs_list SET status = 'R' where id in "))
