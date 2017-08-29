#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.append("..")
from settings import conf
from imports import Bugdb
from Integrity import IntegrityClient
import os
import datetime

def get_alm_connection():
    try:
        intclient = IntegrityClient(
          wsdl="https://alm.tclcom.com:7003/webservices/10/2/Integrity/?wsdl",
          credential_username=conf.ALMUSERNAME,
          credential_password=conf.ALMPASSWORD,
          proxy=dict(http='172.26.35.84:808', https='172.26.35.84:808'))

        return intclient
    except Exception, error:
        print 'not connect'
        sys.exit(1)

def get_FR_byProject(alm_conn, project_name):
    alm_info = alm_conn.getItemsByFieldValues(fields=['ID','Relate Task'], 
                                        Project=project_name, Type='General FR')
    return alm_info

def insert_FR_relationship(conn, task_number, FR_number):
    conn.cur.execute('replace into task_FR_relationship(task_number,FR_number)\
                    values(%s,%s)' % (task_number, FR_number))
    conn.conn.commit()

def main():
    nowhour = int(datetime.datetime.now().strftime("%H%M"))
    if nowhour in range(300, 400) and not os.path.exists('./fr/'):
        os.mkdir('./fr/')
        for project in conf.PROJECT_DICT.keys():
            pidfile = './fr/%s' % project
            pid = open(pidfile, 'w+')
            pid.close()
    print "The dir is exsit means there still stay some projects's info can't fetch, now continue..."
    projects_list = os.listdir('./fr/')
    print projects_list

    alm_conn = get_alm_connection()
    imp = Bugdb('localhost', conf.MYSQLUSERNAME, conf.MYSQLPASSWORD, 'hades')
    for project in projects_list:
        print "Now get %s FR info..." % project
        FR_info = get_FR_byProject(alm_conn, conf.PROJECT_DICT[project])
        Task_FR = {}
        for fr in FR_info:
            for key in fr.keys():
                if key == 'Relate Task':
                    for i in fr[key][1]:
                        if i:
                            Task_FR[i] = fr.id 
        for key in Task_FR.keys():
            insert_FR_relationship(imp,key,Task_FR[key])
        print 'Now %s FR is inserted, delete the project file' % project
        rpidfile = './fr/%s' % project
        os.remove(rpidfile)

    if not os.listdir('./fr/'):
        print "All projects info have fetched, now delete the fr dir!"
        os.removedirs('./fr/')

if __name__ == '__main__':
    main()
