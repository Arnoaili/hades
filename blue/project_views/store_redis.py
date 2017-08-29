#!/usr/bin/env python
# -*- coding: utf-8 -*-
import redis
import datetime
from export_statistics import ExportStc
import sys
sys.path.append("..")
from settings import conf
reload(sys)
sys.setdefaultencoding('utf-8')

class StoreRedis:

    def __init__(self):
        self.r = redis.Redis(host='localhost', port=6379, db=0)

    def set_redis(self, logger):
        day = datetime.date.today().strftime("%Y-%m-%d")
        '''
        date2 = (datetime.date.today() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        date3 = (datetime.date.today() - datetime.timedelta(days=2)).strftime("%Y-%m-%d")
        date4 = (datetime.date.today() - datetime.timedelta(days=3)).strftime("%Y-%m-%d")
        date5 = (datetime.date.today() - datetime.timedelta(days=4)).strftime("%Y-%m-%d")
        date6 = (datetime.date.today() - datetime.timedelta(days=5)).strftime("%Y-%m-%d")
        date7 = (datetime.date.today() - datetime.timedelta(days=6)).strftime("%Y-%m-%d")
        '''
        daily_statistics = ExportStc()
        for project_name in conf.PROJECT_DICT.keys():
            #for date in [date1, date2, date3, date4, date5, date6, date7]:
            try:
                project_static = daily_statistics.get_project_static(project_name)
                function_static = daily_statistics.ten_fun_module(day, project_name)
                team_static = daily_statistics.get_team_static(day, project_name)
                person_static = daily_statistics.get_person_static(day, project_name)
                big_team_static = daily_statistics.get_big_team_static(day, project_name)
                daily_static = daily_statistics.get_daily_bugs(project_name)
                project_sta = {'project_static':'', 'function_static':'', 'daily_static':'',
                                'team_static':'', 'person_static':'', 'big_team_static':''}
                project_sta['project_static'] = project_static
                project_sta['function_static'] = function_static
                project_sta['team_static'] = team_static
                project_sta['person_static'] = person_static
                project_sta['big_team_static'] = big_team_static
                project_sta['daily_static'] = daily_static

                self.r.hset(day, project_name, project_sta)
            except Exception, e:
                logger.info('Warning!! %s %s statistical data is none.' %(day, project_name))
    
    def get_redis(self, day, project_name):
        if self.r.hgetall(day).has_key(project_name):
            data = (self.r.hgetall(day)[project_name]).replace('\'', '\"')
            dict_data = eval(data)
            return dict_data
        else:
            return {}
        
    def flush_redis(self):
        self.r.flushdb()

    def delete_expire(self, logger):
        redis_datelist = self.r.keys()
        logger.info('redis_datelist: %s' % redis_datelist)
        need_datelist = []
        for i in range(0,7):
            date = (datetime.date.today() - datetime.timedelta(days=i)).strftime("%Y-%m-%d")
            need_datelist.append(date)
        logger.info('need_datelist: %s' % need_datelist)
        exprie_datelist = list(set(redis_datelist)-set(need_datelist))
        logger.info('exprie_datelist: %s' % exprie_datelist)
        for item in exprie_datelist:
            logger.info('Now delete %s redis record' % item)
            self.r.delete(item)

"""
test = StoreRedis()
data_reids = test.get_redis('2016-08-18','Frodo')
for key in data_reids.keys():
    print key
ds = ExportStc()
print ds.get_daily_bugs("SAM")
person_static = data_reids['daily_static']
print person_static

"""
