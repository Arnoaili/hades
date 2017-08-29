#!/usr/bin/env python
# -*- coding: utf-8 -*-
from imports import Bugdb
import time
import datetime
import re
import sys
sys.path.append("..")
from settings import conf
reload(sys)

"""
This module use to count bug, The result statistics write to project_static,function_static,team_static
Date：2015-11-18 
Author：Yang Mei
"""

class Bugstatistics:
    '''This is Bugstatistics class'''
    def __init__(self, bug_info):
        '''this method : init method, you should give 1 parameter: bug_info'''
        self.bug_info = bug_info
        self.imp = Bugdb('localhost', conf.MYSQLUSERNAME, 
                            conf.MYSQLPASSWORD, 'hades')
        self.open_bug_type_list = ["New", "Assigned", 
                                "Opened", "Resolved"]
        self.resolve_bug_type_list = ["Delivered", "Verified", 
                                    "Verified_SW", "Closed"]
        self.regression = "YES"
        #datetime.date.today()
        self.today = time.strftime("%Y-%m-%d", time.localtime())

    def judgment_funcion(self, function_list):
        '''this method: Analyzing module exists or not? if not exist, add to database'''
        function_functionid = {}
        function_functionid = self.get_functon_id()
        for function in function_list:
            if function_functionid.has_key(function):
                pass
            else:
                self.imp.cur.execute('insert into function(function_name) values("%s")' % function)

    def get_team_id(self, department):
        '''this method : get user_teamid={user:teamid}'''
        user_teamid = {}
        self.imp.cur.execute('select email,team_id from bugusers \
            where department like "%s"' % department)
        team_info = self.imp.cur.fetchall()
        for team in team_info: 
            user_teamid[team[0]] = str(team[1])
        return user_teamid

    def get_functon_id(self):
        '''this method : get function_functionid={function:functinid}'''
        function_functionid = {}
        self.imp.cur.execute('select function_name,function_id from function')
        function_info = self.imp.cur.fetchall()
        for function in function_info:
            function_functionid[function[0]] = str(function[1])
        return function_functionid

    def get_team_name(self, department):
        '''this method : get function_functionid={function:functinid}'''
        team_teamid = {}

        self.imp.cur.execute('select team,team_id from team where \
            team like "%s"' % department)
        team_info = self.imp.cur.fetchall()
        for team in team_info:
            team_teamid[team[0]] = str(team[1])

        self.imp.cur.execute('select team,team_id from team where team like "CD_%"\
            or team="T2Mobile-SW" or team like "OTHERS%"')
        team_info = self.imp.cur.fetchall()
        for team in team_info:
            team_teamid[team[0]] = str(team[1])

        return team_teamid

    def insert_project_static(self, tname, data, project_name):
        '''this method : insert data to project_static table'''
        self.imp.cur.execute('replace into %s(project_name,date,total,open,fixed,regression) \
            values("%s", "%s", %s, %s, %s, %s)' % (tname, project_name, self.today, 
                data['total'], data['open'], data['fixed'], data['regression']))
        self.imp.conn.commit()

    def insert_function_static(self, tname, data, insert_id, project_name):
        '''this method : insert data to function_static table'''
        self.imp.cur.execute('replace into %s \
            values(%s, "%s", %s, %s, %s, %s, "%s")' % (tname, insert_id, self.today, data['total'], 
                data['open'], data['fixed'], data['regression'], project_name))
        self.imp.conn.commit()

    def insert_team_static(self, data, insert_id, project_name):
        '''this method : insert data to team_static table'''
        self.imp.cur.execute('replace into team_static values(%s, "%s", %s, %s, %s, %s, %s, %s, "%s")' 
            % (insert_id, self.today, data['P0_open'], data['P0_fixed'], data['P0_regression'], 
                data['P1_open'], data['P1_fixed'], data['P1_regression'], project_name))
        self.imp.conn.commit()

    def get_category(self, info):
        '''this method : count every type'''
        category_dict = {'open':0, 'fixed':0, 'regression':0, 'total':0}
        for bug in info:
            if bug.state in self.open_bug_type_list:
                category_dict['open'] += 1
            elif bug.state in self.resolve_bug_type_list:
                category_dict['fixed'] += 1
            if bug.regression == self.regression:
                category_dict['regression'] += 1
        category_dict['total'] = category_dict['open']+category_dict['fixed']
        return category_dict

    def function_get_category(self, info):
        '''this method : count every type'''
        category_dict = {'open':0, 'fixed':0, 'regression':0, 'total':0}
        for bug in info:
            if bug.state in self.open_bug_type_list:
                category_dict['open'] += 1
            if bug.verified_sw_date:
                verified_sw_date = re.search('[0-9]{4}-[0-9]{2}-[0-9]{2}', bug.verified_sw_date).group(0)
                if verified_sw_date == self.today:
                    category_dict['fixed'] += 1
            if bug.regression_date == self.today:
                category_dict['regression'] += 1
        #category_dict['total'] = category_dict['open']+category_dict['fixed']
        return category_dict

    def get_team_statistics(self, info):
        '''this method: count team type'''
        team_dict = {'P0_open':0, 'P0_fixed':0, 'P0_regression':0, 
                    'P1_open':0, 'P1_fixed':0, 'P1_regression':0}
        for bug in info:
            if bug.state in self.open_bug_type_list:
                if bug.priority == 'P0 (Urgent)':
                    team_dict['P0_open'] += 1
                elif bug.priority == 'P1 (Quick)':
                    team_dict['P1_open'] += 1
            if bug.verified_sw_date:
                verified_sw_date = re.search('[0-9]{4}-[0-9]{2}-[0-9]{2}', bug.verified_sw_date).group(0)
                if verified_sw_date == self.today:
                    if bug.priority == 'P0 (Urgent)':
                        team_dict['P0_fixed'] += 1
                    elif bug.priority == 'P1 (Quick)':
                        team_dict['P1_fixed'] += 1
            if bug.regression_date == self.today:
                if bug.priority == 'P0 (Urgent)':
                    team_dict['P0_regression'] += 1
                elif bug.priority == 'P1 (Quick)':
                    team_dict['P1_regression'] += 1
        return team_dict

    def get_other_group(self, department):
        '''this method : get other user_teamid={user:teamid}'''
        other_user_teamid = {}
        other_team_id = {}

        self.imp.cur.execute('select team_id,team from team where team like "OTHERS%" or team="T2Mobile-SW"')
        other_team = self.imp.cur.fetchall()
        for team in other_team:
            other_team_id[str(team[1])] = str(team[0])

        self.imp.cur.execute('select bugusers.email,team.team\
         from bugusers,team where bugusers.team_id=team.team_id and department \
         not in (select department from bugusers where department like "%s")' % department)
        team_info = self.imp.cur.fetchall()
        for team in team_info: 
            if re.search('(-)*(\s)*NB', str(team[1])):
                other_user_teamid[str(team[0])] = other_team_id['OTHERS_NB']
            elif re.search('NingBo', str(team[1])):
                other_user_teamid[str(team[0])] = other_team_id['OTHERS_NB']

            elif re.search('(-)*(\s)*CD', str(team[1])):
                other_user_teamid[str(team[0])] = other_team_id['OTHERS_CD']

            elif re.search('(-)*(\s)*HZ', str(team[1])):
                other_user_teamid[str(team[0])] = other_team_id['OTHERS_HZ']
            elif re.search('(?i)huizhou', str(team[1])):
                other_user_teamid[str(team[0])] = other_team_id['OTHERS_HZ']

            elif re.search('(-)*(\s)*SZ', str(team[1])):
                other_user_teamid[str(team[0])] = other_team_id['OTHERS_SZ']
            elif re.search('SHENZHEN', str(team[1])):
                other_user_teamid[str(team[0])] = other_team_id['OTHERS_SZ']

            elif re.search('(-)*(\s)*SH', str(team[1])):
                other_user_teamid[str(team[0])] = other_team_id['OTHERS_SH']
            elif re.search('ShangHai', str(team[1])):
                other_user_teamid[str(team[0])] = other_team_id['OTHERS_SH']
            
            elif re.search('(-)*(\s)*Wuxi', str(team[1])):
                other_user_teamid[str(team[0])] = other_team_id['OTHERS_WX']

            elif re.search('T2Mobile-SW', str(team[1])):
                other_user_teamid[str(team[0])] = other_team_id['T2Mobile-SW']
            else:
                other_user_teamid[str(team[0])] = other_team_id['OTHERS_TCT']
        return other_user_teamid

    def statistics(self, project_name, logger):
        '''this method: statistics project data, function data, team data'''
        function_daily_statistics = {}
        team_daily_statistics = {}
        team_daily_bug_dict = {}
        function_list = []

        #project daily counts
        logger.info("Now insert %s's project_static data to MySQL!" % project_name)
        project_daily_statistics = self.get_category(self.bug_info)
        self.insert_project_static('project_static', project_daily_statistics, project_name)
        print '*'*100
        print self.today
        print project_name+' Bug_statistics, please follow as below'
        print project_daily_statistics

        #function daily counts
        logger.info("Now insert %s's function_static data to MySQL!" % project_name)
        for bug in self.bug_info:
            function_list.append(bug.function)
        function_list = list(set(function_list))

        self.judgment_funcion(function_list)

        function_functionid = self.get_functon_id()
        for function_name in function_list:
            onefunction_statistics = []
            for bug in self.bug_info:
                if bug.function == function_name:
                    onefunction_statistics.append(bug)
            function_daily_statistics[function_functionid[function_name]] = self.function_get_category(onefunction_statistics)

        print '*'*100
        print function_daily_statistics
        for key in function_daily_statistics.keys():
            self.insert_function_static('function_static', function_daily_statistics[key], key, project_name)

        #team daily counts
        logger.info("Now insert %s's team_static data to MySQL!" % project_name)
        #get email_teamid
        user_teamid_swd = {}
        user_teamid_other = {}
        user_teamid = {}
        if project_name in conf.CD_SWD1_PROJECT:
            user_teamid_swd = self.get_team_id('WMD-PIC CD-SWD1%')
            user_teamid_other = self.get_other_group('WMD-PIC CD-SWD1%')
        if project_name in conf.CD_SWD2_PROJECT:
            user_teamid_swd = self.get_team_id('WMD-PIC CD-SWD2%')
            user_teamid_other = self.get_other_group('WMD-PIC CD-SWD2%')
        user_teamid = dict(user_teamid_swd, **user_teamid_other)

        for bug in self.bug_info:
            if bug.assigned_user.email in user_teamid.keys(): #WMD-PIC CD-SWD1%
                if user_teamid[bug.assigned_user.email] not in team_daily_bug_dict.keys():
                    team_daily_bug_dict[user_teamid[bug.assigned_user.email]] = []
                team_daily_bug_dict[user_teamid[bug.assigned_user.email]].append(bug)
            else:
                if '226' not in team_daily_bug_dict.keys():
                    team_daily_bug_dict['226'] = []
                team_daily_bug_dict['226'].append(bug)

        for teamid in team_daily_bug_dict.keys():
            if teamid not in team_daily_statistics.keys():
                team_daily_statistics[teamid] = {}
            team_daily_statistics[teamid] = self.get_team_statistics(team_daily_bug_dict[teamid])
        team_teamid = {}
        if project_name in conf.CD_SWD1_PROJECT:
            team_teamid = self.get_team_name('WMD-PIC CD-SWD1%')
        if project_name in conf.CD_SWD2_PROJECT:
            team_teamid = self.get_team_name('WMD-PIC CD-SWD2%')
        for teamname in team_teamid.keys():
            if team_teamid[teamname] not in team_daily_statistics.keys():
                print teamname
                team_daily_statistics[team_teamid[teamname]] = {'P0_open':0, 'P0_fixed':0, 
                'P0_regression':0, 'P1_open':0, 'P1_fixed':0, 'P1_regression':0}
        if project_name in conf.CD_SWD1_PROJECT:
            for teamid in team_daily_statistics.keys():
                for p in team_daily_statistics[teamid].keys():
                    team_daily_statistics[team_teamid['CD_SWD1_APP']][p] = team_daily_statistics[team_teamid['WMD-PIC CD-SWD1-APP Team']][p] \
                    + team_daily_statistics[team_teamid['WMD-PIC CD-SWD1-APP Team-APP1']][p] + team_daily_statistics[team_teamid['WMD-PIC CD-SWD1-APP Team-APP2']][p] \
                    + team_daily_statistics[team_teamid['WMD-PIC CD-SWD1-APP Team-APP3']][p] + team_daily_statistics[team_teamid['WMD-PIC CD-SWD1-APP-OS-TSCD']][p] \
                    + team_daily_statistics[team_teamid['WMD-PIC CD-SWD1-APP-OS-SURCD']][p]

                    team_daily_statistics[team_teamid['CD_SWD1_SYS']][p] = team_daily_statistics[team_teamid['WMD-PIC CD-SWD1-SYS Team']][p] \
                    + team_daily_statistics[team_teamid['WMD-PIC CD-SWD1-SYS Team-SYS']][p] + team_daily_statistics[team_teamid['WMD-PIC CD-SWD1-SYS Team-DRIVER1']][p] \
                    + team_daily_statistics[team_teamid['WMD-PIC CD-SWD1-SYS Team-DRIVER2']][p] + team_daily_statistics[team_teamid['WMD-PIC CD-SWD1-System-OS-TSCD']][p] \
                    + team_daily_statistics[team_teamid['WMD-PIC CD-SWD1-System-OS-SURCD']][p]

                    team_daily_statistics[team_teamid['CD_SWD1_MID']][p] = team_daily_statistics[team_teamid['WMD-PIC CD-SWD1-MDW Team']][p] \
                    + team_daily_statistics[team_teamid['WMD-PIC CD-SWD1-MDW Team-CONNECT']][p] + team_daily_statistics[team_teamid['WMD-PIC CD-SWD1-MDW Team-MM']][p] \
                    + team_daily_statistics[team_teamid['WMD-PIC CD-SWD1-MDW Team-FRM']][p] + team_daily_statistics[team_teamid['WMD-PIC CD-SWD1-MDWR-OS-TSCD']][p] \
                    + team_daily_statistics[team_teamid['WMD-PIC CD-SWD1-MDWR-OS-SURCD']][p]
                    
                    team_daily_statistics[team_teamid['CD_SWD1_INT']][p] = team_daily_statistics[team_teamid['WMD-PIC CD-SWD1-INT Team']][p] \
                    + team_daily_statistics[team_teamid['WMD-PIC CD-SWD1-INT-OS-TS']][p]

                    team_daily_statistics[team_teamid['CD_SWD1_TELECOM']][p] = team_daily_statistics[team_teamid['WMD-PIC CD-SWD1-TEL Team']][p] \
                    + team_daily_statistics[team_teamid['WMD-PIC CD-SWD1-Telecom-OS-SURCD']][p] + team_daily_statistics[team_teamid['WMD-PIC CD-SWD1-Telecom-OS-HOPERUN']][p] \
                    + team_daily_statistics[team_teamid['WMD-PIC CD-SWD1-Telecom-OS-TSCD']][p]

                    team_daily_statistics[team_teamid['CD_SWD1_SPM']][p] = team_daily_statistics[team_teamid['WMD-PIC CD-SWD1-SPM Team']][p]

                    team_daily_statistics[team_teamid['OTHERS']][p] = team_daily_statistics[team_teamid['T2Mobile-SW']][p] \
                    + team_daily_statistics[team_teamid['OTHERS_CD']][p] + team_daily_statistics[team_teamid['OTHERS_SZ']][p] \
                    + team_daily_statistics[team_teamid['OTHERS_HZ']][p] + team_daily_statistics[team_teamid['OTHERS_SH']][p] \
                    + team_daily_statistics[team_teamid['OTHERS_NB']][p] + team_daily_statistics[team_teamid['OTHERS_WX']][p] \
                    + team_daily_statistics[team_teamid['OTHERS_TCT']][p]
                break

        if project_name in conf.CD_SWD2_PROJECT:
            for teamid in team_daily_statistics.keys():
                for p in team_daily_statistics[teamid].keys():
                    team_daily_statistics[team_teamid['CD_SWD2_APP']][p] = team_daily_statistics[team_teamid['WMD-PIC CD-SWD2-APP Team']][p] \
                    + team_daily_statistics[team_teamid['WMD-PIC CD-SWD2-APP-OS-SURCD']][p] + team_daily_statistics[team_teamid['WMD-PIC CD-SWD2-APP-OS-TSCD']][p]

                    team_daily_statistics[team_teamid['CD_SWD2_SYS']][p] = team_daily_statistics[team_teamid['WMD-PIC CD-SWD2-SYS Team']][p] \
                    + team_daily_statistics[team_teamid['WMD-PIC CD-SWD2-Security Team']][p] + team_daily_statistics[team_teamid['WMD-PIC CD-SWD2-Driver Team']][p] \
                    + team_daily_statistics[team_teamid['WMD-PIC CD-SWD2-Driver-OS-SURCD']][p] + team_daily_statistics[team_teamid['WMD-PIC CD-SWD2-Driver-OS-TSCD']][p]

                    team_daily_statistics[team_teamid['CD_SWD2_TELECOM']][p] = team_daily_statistics[team_teamid['WMD-PIC CD-SWD2-Telecom Team']][p] \
                    + team_daily_statistics[team_teamid['WMD-PIC CD-SWD2-Telecom-OS-TSCD']][p] + team_daily_statistics[team_teamid['WMD-PIC CD-SWD2-Telecom-OS-SURCD']][p]

                    team_daily_statistics[team_teamid['CD_SWD2_FRM']][p] = team_daily_statistics[team_teamid['WMD-PIC CD-SWD2-FRM Team']][p] \
                    + team_daily_statistics[team_teamid['WMD-PIC CD-SWD2-Framework-OS-TSCD']][p] + team_daily_statistics[team_teamid['WMD-PIC CD-SWD2-Framework-OS-SURCD']][p] \
                    + team_daily_statistics[team_teamid['WMD-PIC CD-SWD2-MID-OS-TSCD']][p] + team_daily_statistics[team_teamid['WMD-PIC CD-SWD2-MID-OS-SURCD']][p]

                    team_daily_statistics[team_teamid['CD_SWD2_SPM']][p] = team_daily_statistics[team_teamid['WMD-PIC CD-SWD2-SPM Team']][p]

                    team_daily_statistics[team_teamid['CD_SWD2_INT']][p] = team_daily_statistics[team_teamid['WMD-PIC CD-SWD2-INT Team']][p] \
                    + team_daily_statistics[team_teamid['WMD-PIC CD-SWD2-Integration-OS-SURCD']][p]

                    team_daily_statistics[team_teamid['OTHERS']][p] = team_daily_statistics[team_teamid['T2Mobile-SW']][p] \
                    + team_daily_statistics[team_teamid['OTHERS_CD']][p] + team_daily_statistics[team_teamid['OTHERS_SZ']][p] \
                    + team_daily_statistics[team_teamid['OTHERS_HZ']][p] + team_daily_statistics[team_teamid['OTHERS_SH']][p] \
                    + team_daily_statistics[team_teamid['OTHERS_NB']][p] + team_daily_statistics[team_teamid['OTHERS_WX']][p] \
                    + team_daily_statistics[team_teamid['OTHERS_TCT']][p]
                break

        print '*'*100
        print team_daily_statistics
        for key in team_daily_statistics:
            self.insert_team_static(team_daily_statistics[key], key, project_name)


    def get_user_userid(self):
        '''this method : get user_teamid={user:userid}'''
        user_userid = {}
        self.imp.cur.execute('select email,id from bugusers \
            where department like "WMD-PIC CD-SWD1%" or department like "WMD-PIC CD-SWD2%"')
        user_info = self.imp.cur.fetchall()
        for user in user_info: 
            user_userid[user[0]] = str(user[1])
        return user_userid

    def get_userid_section(self):
        '''this method : get userid_section={user:section}'''
        userid_section = {}
        self.imp.cur.execute('select id,section from bugusers \
            where department like "WMD-PIC CD-SWD1%" or department like "WMD-PIC CD-SWD2%"')
        userid_info = self.imp.cur.fetchall()
        for userid in userid_info:
            userid_section[str(userid[0])] = str(userid[1])
        #print userid_section
        return userid_section

    def person_statistics(self, project_name, logger):
    #def person_statistics(self, project_name):
        '''this method: insert into person_static table'''
        #p0,p1
        logger.info("Now insert %s's person_static data to MySQL!" % project_name)
        person_dict = {}
        email_userid = self.get_user_userid()

        for email in email_userid.keys():
            if email not in person_dict.keys():
                person_dict[email_userid[email]] = {'P0_open':0, 'P1_open':0, 'P0_fixed':0, 
                                                    'P1_fixed':0, 'P0_regression':0, 'P1_regression':0, 
                                                    'daily_open':0, 'daily_fix':0}
        for bug in self.bug_info:
            if bug.assigned_user.email in email_userid.keys():
                if bug.state in self.open_bug_type_list:
                    if bug.priority == 'P0 (Urgent)':
                        person_dict[email_userid[bug.assigned_user.email]]['P0_open'] += 1
                    elif bug.priority == 'P1 (Quick)':
                        person_dict[email_userid[bug.assigned_user.email]]['P1_open'] += 1
                if bug.verified_sw_date:
                    verified_sw_date = re.search('[0-9]{4}-[0-9]{2}-[0-9]{2}', bug.verified_sw_date).group(0)
                    if verified_sw_date == self.today:
                        if bug.priority == 'P0 (Urgent)':
                            person_dict[email_userid[bug.assigned_user.email]]['P0_fixed'] += 1
                        elif bug.priority == 'P1 (Quick)':
                            person_dict[email_userid[bug.assigned_user.email]]['P1_fixed'] += 1
                if bug.regression_date == self.today:
                    if bug.priority == 'P0 (Urgent)':
                        person_dict[email_userid[bug.assigned_user.email]]['P0_regression'] += 1
                    elif bug.priority == 'P1 (Quick)':
                        person_dict[email_userid[bug.assigned_user.email]]['P1_regression'] += 1
                assignedDate = ''
                verifiedSWDate = ''
                if bug.assigned_date:
                    assignedDate = datetime.datetime.strptime(bug.assigned_date,'%Y-%m-%d %H:%M:%S').strftime("%Y-%m-%d")
                if bug.verified_sw_date:
                    verifiedSWDate = datetime.datetime.strptime(bug.verified_sw_date,'%Y-%m-%d %H:%M:%S').strftime("%Y-%m-%d")
                if assignedDate == self.today:
                    person_dict[email_userid[bug.assigned_user.email]]['daily_open'] += 1
                if verifiedSWDate == self.today:
                    person_dict[email_userid[bug.assigned_user.email]]['daily_fix'] += 1

                    
        print '*'*100
        print person_dict
        self.insert_person_static(person_dict, project_name)


    def insert_person_static(self, person_dict, project_name):
        '''this method : insert data to person_static table'''

        userid_section = self.get_userid_section()
        for key in person_dict.keys():
            self.imp.cur.execute('replace into person_static(user_id, section, P0_open, P1_open, P0_fixed,\
                        P1_fixed, P0_regression, P1_regression, project_name, date, daily_open, daily_fix) \
                        values(%s, "%s", %s, %s, %s, %s, %s, %s, "%s", "%s", %s, %s)'
                        % (key, userid_section[key], person_dict[key]['P0_open'], person_dict[key]['P1_open'], 
                            person_dict[key]['P0_fixed'], person_dict[key]['P1_fixed'], person_dict[key]['P0_regression'], 
                            person_dict[key]['P1_regression'], project_name, self.today, 
                            person_dict[key]['daily_open'], person_dict[key]['daily_fix']))
            self.imp.conn.commit()


#from Almfunc import Almfunc
#alm = Almfunc('/TCT/QCT MSM8909/MICKEY6 TF UMTS')
#conn = alm.get_alm_connection()
#info = alm.fetch_bug_id(conn, '/TCT/QCT MSM8909/MICKEY6 TF UMTS')
#test = Bugstatistics(info)
#test.statistics('Mickey6_tf_umts')
#test.person_statistics('Mickey6_tf_umts')



