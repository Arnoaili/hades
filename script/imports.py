#!/usr/bin/env python
# -*- coding: utf-8 -*-
import MySQLdb
import sys
reload(sys)
#sys.setdefaultencoding('utf-8')
'''
This module connect to mysql database
Date：2015-11-18 
Author：Yang Mei
'''

class Bugdb:
    '''This is Bugdb class'''
    def __init__(self, host, user, passwd, db):
        '''this method : init method, you should give 4 parameters: host user passwd db'''
        self.host = host
        self.user = user
        self.passwd = passwd
        self.port = 3306
        #self.charset = charset
        self.db = db

        try:
            self.conn = MySQLdb.connect(
                host=self.host, port=self.port, 
                user=self.user, passwd=self.passwd)
            self.conn.select_db(self.db)
            self.cur = self.conn.cursor()
            #self.autocommit(False)  # protect sql error import & update
            #self.conn.set_character_set(self.charset)
        except MySQLdb.Error as error:
            print("Mysql error %d: %s" % (error.args[0], error.args[1]))

    def close(self):
        '''this method : connection close'''
        self.cur.close()
        self.conn.close()

    def query(self, sql):
        '''this method : search from database and return result'''
        try:
            result = self.cur.execute(sql)
            return result
        except MySQLdb.Error as error:
            print("Mysql ERROR: %s\nSQL:%s" % (error, sql))

    def fetchall(self):
        '''this method : Traversal every result and save to dictionary'''
        result = self.cur.fetchall()
        desc = self.cur.description
        resultlist = []
        for inv in result:
            _d = {}
            for i in range(0, len(inv)):
                _d[desc[i][0]] = str(inv[i])
            resultlist.append(_d)
        return resultlist

    def replace(self, tbname, data):
        '''this method : replace into database table'''
        columns = data.keys()
        _prefix = "".join(['REPLACE INTO `', tbname, '`'])
        _fields = ",".join(["".join(['`', column, '`']) for column in columns])
        _values = ",".join(["".join
            (['\'',str(data[key]), '\'']) for key in columns])
        _sql = "".join([_prefix, "(", _fields, ") VALUES (", _values, ");"])
        print _sql
        self.cur.execute(_sql)
        self.conn.commit()