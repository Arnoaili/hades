#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Integrity import IntegrityClient
from imports import Bugdb
import sys
sys.path.append("..")
from settings import conf
import re

imp = Bugdb('localhost', conf.MYSQLUSERNAME,
            conf.MYSQLPASSWORD, 'hades')

def get_alm_connection():

        """Connect to ALM"""

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

def get_bugusers():
    database_user = {}
    imp.cur.execute('select email,team_id,department,telephone from bugusers')
    bugusers = imp.cur.fetchall()
    for user in bugusers:
        database_user[str(user[0])] = {'team':str(user[1]),
                                    'department':str(user[2]),
                                    'telephone':str(user[3])}
    return database_user

def replace_bugusers(update_dict, insert_dict):
    #print update_dict
    for item in update_dict.keys():
        try:
            imp.cur.execute('update bugusers set \
                section="%s", \
                team_id=(select team_id from team where team="%s"),\
                department="%s",\
                telephone="%s" where email="%s"' % (
                update_dict[item]['section'], 
                update_dict[item]['team'], 
                update_dict[item]['department'], 
                update_dict[item]['telephone'], 
                item))
            imp.conn.commit()
        except Exception, error:
            print "[ERROR]", item, "is not updated to bugusers table"
            continue
    for item in insert_dict.keys():
        try:
            imp.cur.execute('insert into bugusers(email,team_id,section,\
                department,telephone) \
                values("%s",(select team_id from team where team="%s"),"%s","%s","%s")' % (item, 
                insert_dict[item]['team'],
                insert_dict[item]['section'],
                insert_dict[item]['department'], 
                insert_dict[item]['telephone']))
            imp.conn.commit()
        except Exception, error:
            print "[ERROR]", item, "is not inserted to bugusers table"
            continue

def get_databaseteam():
    database_teamlist = []
    imp.cur.execute('select team from team')
    database_team = imp.cur.fetchall()
    for item in database_team:
        if item[0] not in database_teamlist:
            database_teamlist.append(item[0])
    return database_teamlist

def insert_team(team_list):
    for item in team_list:
        #print item
        try:
            imp.cur.execute('insert team(team) values("%s")' % item)
            imp.conn.commit()
        except Exception, error:
            print "[ERROR]", item, "is not inserted to team table"
            continue


def main():
    typelist = ['Defect', 'Task','Stability Defect']
    alm_conn = get_alm_connection()
    buguser_relationship = {}
    database_teamlist = get_databaseteam()
    alm_teamlist =[]
    for project in conf.PROJECT_DICT.keys():
        print project
        for type in typelist:
            info_bug = alm_conn.getItemsByFieldValues(fields=['Assignee E-Mail', 
                                        'Assignee Team Name', 'Assignee Department', 'Assignee Telephone'],
                                        Project=conf.PROJECT_DICT[project], 
                                        Type=type)
            for item in info_bug:
                if item.assigned_email != '':
                    if buguser_relationship.has_key(item.assigned_email):
                        pass
                    else:
                        #.encode("utf-8").decode("latin1")
                        buguser_relationship[item.assigned_email] = {'team':item.assigned_team, 
                                                        'department':item.assigned_department,
                                                        'telephone':item.assigned_telephone}
    database_user = get_bugusers()
    update_dict = {}
    insert_dict = {}
    # section = {'CD_APP':['WMD-PIC CD-SWD1-APP','WMD-PIC CD-SWD1-APP-APP1',
    #             'WMD-PIC CD-SWD1-APP-APP2','WMD-PIC CD-SWD1-APP-APP3','WMD-PIC CD-SWD1-APP-OS-TSCD']
    for user in buguser_relationship.keys():
        if buguser_relationship[user]['team'] not in database_teamlist:
            if buguser_relationship[user]['team'] not in alm_teamlist:
                alm_teamlist.append(buguser_relationship[user]['team'])

        if re.search('WMD-PIC CD-SWD1-APP([-]*[a-zA-Z0-9]*)*', buguser_relationship[user]['team']):
            buguser_relationship[user]['section'] = 'CD_SWD1_APP'

        elif re.search('WMD-PIC CD-SWD1-SYS([-]*[a-zA-Z0-9]*)*', buguser_relationship[user]['team']):
            buguser_relationship[user]['section'] = 'CD_SWD1_SYS'

        elif re.search('WMD-PIC CD-SWD1-MDW([-]*[a-zA-Z0-9]*)*', buguser_relationship[user]['team']):
            buguser_relationship[user]['section'] = 'CD_SWD1_MID'

        elif re.search('WMD-PIC CD-SWD1-INT([-]*[a-zA-Z0-9]*)*', buguser_relationship[user]['team']):
            buguser_relationship[user]['section'] = 'CD_SWD1_INT'

        elif re.search('WMD-PIC CD-SWD1-T[a-zA-Z]*([-]*[a-zA-Z0-9]*)*', buguser_relationship[user]['team']):
            buguser_relationship[user]['section'] = 'CD_SWD1_TELECOM'

        elif re.search('WMD-PIC CD-SWD1-SPM([-]*[a-zA-Z0-9]*)*', buguser_relationship[user]['team']):
            buguser_relationship[user]['section'] = 'CD_SWD1_SPM'

        elif re.search('WMD-PIC CD-SWD2-APP([-]*[a-zA-Z0-9]*)*', buguser_relationship[user]['team']):
            buguser_relationship[user]['section'] = 'CD_SWD2_APP'

        elif re.search('WMD-PIC CD-SWD2-SYS([-]*[a-zA-Z0-9]*)*', buguser_relationship[user]['team']):
            buguser_relationship[user]['section'] = 'CD_SWD2_SYS'
        elif re.search('WMD-PIC CD-SWD2-Security', buguser_relationship[user]['team']):
            buguser_relationship[user]['section'] = 'CD_SWD2_SYS'
        elif re.search('WMD-PIC CD-SWD2-Driver', buguser_relationship[user]['team']):
            buguser_relationship[user]['section'] = 'CD_SWD2_SYS'
        
        elif re.search('WMD-PIC CD-SWD2-Telecom', buguser_relationship[user]['team']):
            buguser_relationship[user]['section'] = 'CD_SWD2_TELECOM'

        elif re.search('WMD-PIC CD-SWD2-F[a-zA-Z]*([-]*[a-zA-Z0-9]*)*', buguser_relationship[user]['team']):
            buguser_relationship[user]['section'] = 'CD_SWD2_FRM'
        elif re.search('WMD-PIC CD-SWD2-MID([-]*[a-zA-Z0-9]*)*', buguser_relationship[user]['team']):
            buguser_relationship[user]['section'] = 'CD_SWD2_FRM'

        elif re.search('WMD-PIC CD-SWD2-SPM([-]*[a-zA-Z0-9]*)*', buguser_relationship[user]['team']):
            buguser_relationship[user]['section'] = 'CD_SWD2_SPM'

        elif re.search('WMD-PIC CD-SWD2-I[a-zA-Z]*([-]*[a-zA-Z0-9]*)*', buguser_relationship[user]['team']):
            buguser_relationship[user]['section'] = 'CD_SWD2_INT'

        else:
            buguser_relationship[user]['section'] = 'OTHERS'

        if database_user.has_key(user):
            #if database_user[user] != buguser_relationship[user]:
            update_dict[user] = buguser_relationship[user]
        else:
            insert_dict[user] = buguser_relationship[user]
    #inset team table
    insert_team(alm_teamlist)
    #replace bugusers table
    replace_bugusers(update_dict, insert_dict)

if __name__ == '__main__':
    main()
