#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.append("../..")
from script.imports import Bugdb
from script.Almfunc import Almfunc
from settings import conf
import datetime
import time
import re
reload(sys)
sys.setdefaultencoding('utf-8')

class ExportStc:

    def __init__(self):
        self.imp = Bugdb(
            'localhost', conf.MYSQLUSERNAME,
            conf.MYSQLPASSWORD, 'hades')

    #获取选择的时间前最靠近的一个
    def get_recent_date(self, errdate):
        self.imp.cur.execute(
                'select MAX(date) from project_static where date < "%s"'
                % errdate)
        recent_date = self.imp.cur.fetchall()
        value = recent_date[0][0]
        return value


    def get_project_static(self, project_name):
        project_static = []
        type_list = ['open', 'fixed', 'regression']
        for item in type_list:
            date_record = []
            one_record = {'data': date_record, 'name': item, 'type': 'line'}
            self.imp.cur.execute(
                'select date,%s from project_static where project_name="%s"'
                % (item, project_name))
            item_info = self.imp.cur.fetchall()
            for info in item_info:
                a = str(info[0])
                b = str(info[1])
                c = [a, b]
                date_record.append(c)
            project_static.append(one_record)
        return project_static

    def get_team_name(self):
        teamid_team = {}
        self.imp.cur.execute('select team,team_id from team')
        team_info = self.imp.cur.fetchall()
        for team in team_info:
            teamid_team[str(team[1])] = str(team[0])
        return teamid_team

    def get_team_static(self, date, project_name):
        big_team_list = []
        if project_name in conf.CD_SWD1_PROJECT:
            big_team_list = ['CD_SWD1_APP', 'CD_SWD1_SYS', 'CD_SWD1_MID', 'CD_SWD1_TELECOM', 
                'CD_SWD1_SPM', 'CD_SWD1_INT', 'OTHERS']
        if project_name in conf.CD_SWD2_PROJECT:
            big_team_list = ['CD_SWD2_APP', 'CD_SWD2_SYS', 'CD_SWD2_FRM', 'CD_SWD2_TELECOM', 
                'CD_SWD2_SPM', 'CD_SWD2_INT', 'OTHERS']

        team_static = {}
        teamid_team = self.get_team_name()
        #big team statis
        for item in big_team_list:
            self.imp.cur.execute(
                'select P0_open,P0_fixed,P0_regression,\
                 P1_open,P1_fixed,P1_regression \
                 from team_static where team_id= \
                 (select team_id from team where team="%s")\
                 and date="%s" and project_name="%s"'
                % (item, date, project_name))
            team_static_p0 = []
            team_static_p1 = []
            little_team_static_p0 = []
            little_team_static_p1 = []
            priority = {'P0': team_static_p0, 'P1': team_static_p1}

            if item not in team_static.keys():
                team_static[item] = priority
            item_info = self.imp.cur.fetchall()
            type_stic_p0 = {'open': 0, 'fixed': 0, 'reg': 0}
            type_stic_p1 = {'open': 0, 'fixed': 0, 'reg': 0}

            for info in item_info:
                type_stic_p0['open'] = int(info[0])
                type_stic_p0['fixed'] = int(info[1])
                type_stic_p0['reg'] = int(info[2])
                type_stic_p1['open'] = int(info[3])
                type_stic_p1['fixed'] = int(info[4])
                type_stic_p1['reg'] = int(info[5])
            team_static_p0.append(type_stic_p0)
            team_static_p1.append(type_stic_p1)

            item_member = ()
            if item == 'CD_SWD1_APP':
                item_member = (
                    'WMD-PIC CD-SWD1-APP Team', 'WMD-PIC CD-SWD1-APP Team-APP1',
                    'WMD-PIC CD-SWD1-APP Team-APP2', 'WMD-PIC CD-SWD1-APP Team-APP3',
                    'WMD-PIC CD-SWD1-APP-OS-TSCD','WMD-PIC CD-SWD1-APP-OS-SURCD')
            elif item == 'CD_SWD1_SYS':
                item_member = (
                    'WMD-PIC CD-SWD1-SYS Team', 'WMD-PIC CD-SWD1-SYS Team-SYS',
                    'WMD-PIC CD-SWD1-SYS Team-DRIVER1', 'WMD-PIC CD-SWD1-SYS Team-DRIVER2',
                    'WMD-PIC CD-SWD1-System-OS-TSCD','WMD-PIC CD-SWD1-System-OS-SURCD')
            elif item == 'CD_SWD1_MID':
                item_member = (
                    'WMD-PIC CD-SWD1-MDW Team', 'WMD-PIC CD-SWD1-MDW Team-CONNECT',
                    'WMD-PIC CD-SWD1-MDW Team-MM', 'WMD-PIC CD-SWD1-MDW Team-FRM',
                    'WMD-PIC CD-SWD1-MDWR-OS-TSCD','WMD-PIC CD-SWD1-MDWR-OS-SURCD')
            elif item == 'CD_SWD1_TELECOM':
                item_member = (
                    'WMD-PIC CD-SWD1-TEL Team','WMD-PIC CD-SWD1-Telecom-OS-SURCD',
                    'WMD-PIC CD-SWD1-Telecom-OS-HOPERUN','WMD-PIC CD-SWD1-Telecom-OS-TSCD')
            elif item == 'CD_SWD1_SPM':
                item_member = ('WMD-PIC CD-SWD1-SPM Team')
            elif item == 'CD_SWD1_INT':
                item_member = ('WMD-PIC CD-SWD1-INT Team','WMD-PIC CD-SWD1-INT-OS-TS')
            elif item == 'CD_SWD2_APP':
                item_member = (
                    'WMD-PIC CD-SWD2-APP Team','WMD-PIC CD-SWD2-APP-OS-SURCD',
                    'WMD-PIC CD-SWD2-APP-OS-TSCD'
                    )
            elif item == 'CD_SWD2_SYS':
                item_member = (
                    'WMD-PIC CD-SWD2-SYS Team','WMD-PIC CD-SWD2-Security Team',
                    'WMD-PIC CD-SWD2-Driver Team','WMD-PIC CD-SWD2-Driver-OS-SURCD',
                    'WMD-PIC CD-SWD2-Driver-OS-TSCD'   
                    )
            elif item == 'CD_SWD2_FRM':
                item_member = (
                    'WMD-PIC CD-SWD2-FRM Team','WMD-PIC CD-SWD2-Framework-OS-TSCD',
                    'WMD-PIC CD-SWD2-Framework-OS-SURCD','WMD-PIC CD-SWD2-MID-OS-TSCD',
                    'WMD-PIC CD-SWD2-MID-OS-SURCD'
                    )
            elif item == 'CD_SWD2_TELECOM':
                item_member = (
                    'WMD-PIC CD-SWD2-Telecom Team','WMD-PIC CD-SWD2-Telecom-OS-TSCD',
                    'WMD-PIC CD-SWD2-Telecom-OS-SURCD'
                    )
            elif item == 'CD_SWD2_SPM':
                item_member = ('WMD-PIC CD-SWD2-SPM Team')
            elif item == 'CD_SWD2_INT':
                item_member = (
                    'WMD-PIC CD-SWD2-INT Team','WMD-PIC CD-SWD2-Integration-OS-SURCD')
            elif item == 'OTHERS':
                item_member = ('T2Mobile-SW','OTHERS_CD','OTHERS_SZ',
                    'OTHERS_HZ','OTHERS_SH','OTHERS_NB','OTHERS_WX','OTHERS_TCT')

            type_list_p0 = ['P0_open', 'P0_fixed', 'P0_regression']
            type_list_p1 = ['P1_open', 'P1_fixed', 'P1_regression']
            #search open fixed regression 
            for t in range(3):
                little_team_data_one_p0 = {}
                little_team_data_one_p1 = {}
                little_team_data_p0 = {
                    'data': little_team_data_one_p0,
                    'name': type_list_p0[t]
                    }
                little_team_data_p1 = {
                    'data': little_team_data_one_p1,
                    'name': type_list_p1[t]
                    }
                #more than one member
                if item in ['CD_SWD1_APP', 'CD_SWD1_SYS', 'CD_SWD1_MID', 'CD_SWD1_TELECOM', 
                            'CD_SWD1_INT', 'OTHERS', 'CD_SWD2_APP', 'CD_SWD2_SYS', 'CD_SWD2_FRM', 
                            'CD_SWD2_TELECOM', 'CD_SWD2_INT']:
                    self.imp.cur.execute(
                        "select team_id,%s,%s from team_static \
                         where team_id in(select team_id from team \
                         where team in %s) and date='%s' and project_name='%s'"
                        % (
                            type_list_p0[t], type_list_p1[t],
                            item_member, date, project_name)
                        )
                else:
                    self.imp.cur.execute(
                        'select team_id,%s,%s from team_static \
                         where team_id in(select team_id from team \
                         where team="%s") and date="%s" and project_name="%s"'
                        % (
                            type_list_p0[t], type_list_p1[t],
                            item_member, date, project_name)
                        )
                type_info = self.imp.cur.fetchall()
                for i in type_info:
                    little_team_data_one_p0[teamid_team[str(i[0])]] = int(i[1])
                    little_team_data_one_p1[teamid_team[str(i[0])]] = int(i[2])

                little_team_static_p0.append(little_team_data_p0)
                little_team_static_p1.append(little_team_data_p1)
            team_static_p0.append(little_team_static_p0)
            team_static_p1.append(little_team_static_p1)
        return team_static

    def get_big_team_static(self, date, project_name):
        # teamid_team = self.get_team_name()
        big_team_static = {}
        big_team_list = []
        if project_name in conf.CD_SWD1_PROJECT:
            big_team_list = ['CD_SWD1_APP', 'CD_SWD1_SYS', 'CD_SWD1_MID', 'CD_SWD1_TELECOM', 
                'CD_SWD1_SPM', 'CD_SWD1_INT', 'OTHERS']
        if project_name in conf.CD_SWD2_PROJECT:
            big_team_list = ['CD_SWD2_APP', 'CD_SWD2_SYS', 'CD_SWD2_FRM', 'CD_SWD2_TELECOM', 
                'CD_SWD2_SPM', 'CD_SWD2_INT', 'OTHERS']
        for team in big_team_list:
            self.imp.cur.execute(
                'select P0_open,P1_open,P0_fixed,P1_fixed,P0_regression,P1_regression\
                 from team_static \
                 where team_id in (select team_id from team \
                 where team="%s") and date="%s" and project_name="%s"'
                % (team, date, project_name))
            type_info = self.imp.cur.fetchall()
            for info in type_info:
                if team not in big_team_static.keys():
                    big_team_static[team] = []
                big_team_static[team].append(str(int(info[0])+int(info[1])))
                big_team_static[team].append(str(int(info[2])+int(info[3])))
                big_team_static[team].append(str(int(info[4])+int(info[5])))
        return big_team_static

    def get_bug_list(self, project_name):
        self.imp.cur.execute(
            'select base.bug_id,base.branch,\
             bugusers.email,base.priority,base.bug_status,\
             base.comment_from_cea,base.type,base.regression,base.val_refuse,\
             base.deadline,base.summary,base.resolver, \
             base.long_text_read_only,base.verified_sw_date,base.comments,base.level from base,bugusers \
             where project_name="%s" and base.assigner=bugusers.id'
            % project_name)
        bug_tulpe = self.imp.cur.fetchall()
        bug_list = []
        bug_infos = ["bug_id","branch","assigner","priority","bug_status",
            "comment_from_cea","type","regression","val_refuse","deadline",
            "summary","resolver","long_text_read_only","verified_sw_date",
            'comments', 'level']
        for info in bug_tulpe:
            one_list = {}
            for i in xrange(len(bug_infos)):
                one_list[bug_infos[i]] = info[i]
            bug_list.append(one_list)

        self.imp.cur.execute('select id,email from bugusers \
             where department like "WMD-PIC CD-SWD1%" or department like "WMD-PIC CD-SWD2%"')
        user_infos = self.imp.cur.fetchall()
        swd1 = []
        user_dict = {}
        for info in user_infos:
            user_dict[info[0]] = info[1]
            swd1.append(info[1])

        for info in bug_list:
            # 如果assigner不属于SWD1，从comments里面选取最后一个属于SWD1的人
            # if info["bug_status"] == "Closed" and info["verified_sw_date"] == None:
            #     if info["assigner"] not in swd1 and info["long_text_read_only"] in user_dict.keys():
            #         info["assigner"] = user_dict[info["long_text_read_only"]]
            # elif info["bug_status"] == "Closed" and info["assigner"] not in swd1:
            #     if info["long_text_read_only"] in user_dict.keys():
            #         info["assigner"] = user_dict[info["long_text_read_only"]]
            if info["comments"]:
                comments = " ".join(info['comments'].split("\n"))
                comment_list = re.findall('(Comments.*?)---+', comments)
                for comment in comment_list:
                    # 选取最后一个属于SWD1的comment
                    # if "SWD1" in comment:
                    if "###%%%" in comment:
                        tmp = "</br>###%%%".join(comment.split("###%%%"))
                        info["comments"] = "</br>Branch".join(tmp.split("Branch"))
                    else:
                        info["comments"] = comment+'</br>'
                    break
                # if info["assigner"] == "other@tcl.com":
                #     print "$$$$$$$$$$$$$$$$$$$$$$$$$$$"
                #     comments = " ".join(info['comments'].split("\n"))
                #     print comments
                #     comment_list = re.findall('(Comments.*?)---+', comments)
                #     info["comments"] = "</br></br>".join(comment_list)
                #     print info["comments"]
        return bug_list

    def insert_level_into_db(self, level, bugid):
        self.imp.cur.execute('update base set level="%s" where bug_id=%s' % (level, bugid))
        self.imp.conn.commit()

    def deliver_comments_to_alm(self, bug_id, add_comment, assigner=None):
        alm = Almfunc("")
        alm_conn = alm.get_alm_connection()
        if assigner:
            arg = {
                'Additional Comments': add_comment,
                'Assigned User': assigner
                }
        else:
            arg = {
                    'Additional Comments': add_comment,
                    }
        resp = alm_conn.editItem(item_id=bug_id, **arg)
        print "**********************YES"

    def get_project_total(self, project_list):
        total_project = {}
        for project in project_list:
            alm_project = project
            if project not in total_project.keys():
                total_project[project] = {}
            one_project_total = {'Total Num': 0, 'Task Num': 0, 'Defect Num': 0}
            self.imp.cur.execute(
                'select count(*) from base where project_name="%s"'
                % alm_project)
            result_row = self.imp.cur.fetchall()
            total_count = result_row[0][0]
            one_project_total['Total Num'] = int(total_count)

            self.imp.cur.execute(
                'select count(*) from base where project_name="%s" and type="Defect"'
                #'where project_name="%s" and type="Defect"'
                % alm_project)
            result_row = self.imp.cur.fetchall()
            defect_count = result_row[0][0]
            one_project_total['Defect Num'] = int(defect_count)

            task_count = int(total_count)-int(defect_count)
            one_project_total['Task Num'] = task_count

            total_project[project] = one_project_total
        return total_project

    def get_project_status(self, project_list):
        today = datetime.date.today()
        project_status = {}
        status = ['progress-bar-striped', 'progress-bar-warning',
                'progress-bar-info', 'progress-bar-danger', 'progress-bar-success']
        i = 0
        for project in project_list:
            alm_project = project
            if project not in project_status.keys():
                project_status[project] = []
            self.imp.cur.execute(
                'select dr0,dr1,dr2,dr3,fsr,dr4 from project_status where project_name="%s"'
                #'where project_name="%s"'
                % alm_project)
            result_row = self.imp.cur.fetchall()
            start_time = result_row[0][0]
            end_time = result_row[0][5]

            start_date = str(start_time).split('-')
            end_date = str(end_time).split('-')
            today_date = str(today).split('-')

            total_days = (
                datetime.datetime(
                    int(end_date[0]),
                    int(end_date[1]),
                    int(end_date[2])) -
                datetime.datetime(
                    int(start_date[0]),
                    int(start_date[1]),
                    int(start_date[2]))).days
            now_days = (datetime.datetime(
                int(today_date[0]),
                int(today_date[1]),
                int(today_date[2])) -
                datetime.datetime(
                    int(start_date[0]),
                    int(start_date[1]),
                    int(start_date[2]))).days

            if now_days > total_days:
                project_status[project].append('100')
            else:
                project_status[project].append(str(now_days*100/total_days))
            project_status[project].append(status[i])
            field = []
            for field_desc in self.imp.cur.description:
                field.append(field_desc[0])
            for row in result_row:
                for r in range(5):
                    dr_date = datetime.datetime(
                        int(str(row[r]).split('-')[0]),
                        int(str(row[r]).split('-')[1]),
                        int(str(row[r]).split('-')[2])
                        )
                    if time.mktime(dr_date.timetuple()) > time.time():
                        project_status[project].append(field[r])
                        break
            if len(project_status[project]) == 2:
                project_status[project].append(field[5])

            i += 1
            if i == 5:
                i = 0
        return project_status

    def date_record_yes_no(self, date, project):
        self.imp.cur.execute(
            'select * from project_static \
             where date="%s" and project_name="%s"'
            % (date, project))
        result_date = self.imp.cur.fetchall()
        '''
        self.imp.cur.execute(
            'select * from project_static \
             where date="%s" and project_name="%s"'
            % (yesterday_date, project))
        result_yesterday_date = self.imp.cur.fetchall()
        '''
        if result_date:
            return True
        else:
            return False

    def get_person_static(self, date, project_name):
        big_team_list = []
        if project_name in conf.CD_SWD1_PROJECT:
            big_team_list = ['CD_SWD1_APP', 'CD_SWD1_SYS', 'CD_SWD1_MID', 'CD_SWD1_TELECOM', 
                'CD_SWD1_SPM', 'CD_SWD1_INT']
        if project_name in conf.CD_SWD2_PROJECT:
            big_team_list = ['CD_SWD2_APP', 'CD_SWD2_SYS', 'CD_SWD2_FRM', 'CD_SWD2_TELECOM', 
                'CD_SWD2_SPM', 'CD_SWD2_INT']
        #get today data
        person_dict_today = {}
        for team in big_team_list:
            if team not in person_dict_today.keys():
                person_dict_today[team] = {}
        self.imp.cur.execute(
            'select person_static.section, bugusers.email, person_static.P0_open,\
             person_static.P1_open, person_static.P0_fixed, person_static.P1_fixed,\
             person_static.P0_regression, person_static.P1_regression \
             from person_static,bugusers where date="%s" and project_name="%s" \
             and bugusers.id=person_static.user_id'
            % (date, project_name))
        result_today_data = self.imp.cur.fetchall()
        for row in result_today_data:
            if person_dict_today.has_key(row[0]):
                if row[1] not in person_dict_today[row[0]].keys():
                    person_dict_today[row[0]][row[1]] = {}
                person_dict_today[row[0]][row[1]] = {'P0_open':str(row[2]), 'P1_open':str(row[3]), 'P0_fixed':str(row[4]),
                                        'P1_fixed':str(row[5]), 'P0_regression':str(row[6]), 'P1_regression':str(row[7])}
        person_dict_sort = {}           
        for section in person_dict_today.keys():
            person_dict_sort[section] = sorted(person_dict_today[section].iteritems(), key=lambda d:(d[1]['P0_open']+d[1]['P1_open'],d[1]['P0_open'],d[1]['P1_open'],d[1]['P0_fixed']+d[1]['P1_fixed'],d[1]['P0_fixed'],d[1]['P1_fixed']), reverse = True)
        return person_dict_sort

    def get_functon_id(self):

        """Get a dictionary about function's name and function's id"""

        function_functionid = {}
        self.imp.cur.execute('select function_name,function_id from function')
        function_info = self.imp.cur.fetchall()
        for function in function_info:
            function_functionid[function[0]] = str(function[1])
        return function_functionid

    def get_functions(self, fun_name_id, function_all, sta):

        """Get a dictionary about function'name and bug's number'"""

        functions = {}
        length = len(function_all)
        for i in xrange(0, length):
            one_function = function_all[i]
            for key in fun_name_id.keys():
                if one_function['function_id'] == fun_name_id[key]:
                    functions[key] = int(one_function[sta])
        return functions

    def function_sort(self, fun): 

        """Get a dictionary of top-ten functions on the basis of bug's number"""

        ten_function = {}       
        function_sorted = sorted(fun.items(), key=lambda d:d[1], reverse = True)
        for i in xrange(0, 10):
            ten_function[function_sorted[i][0]] = function_sorted[i][1]
        return ten_function

    def get_function_data(self, date, project_name):

        """Get function's data from function_static table"""

        sql = 'select * from function_static where date="%s" and \
               project_name="%s"' % (date, project_name)
        self.imp.query(sql)
        function_data = self.imp.fetchall()
        return function_data

    def get_one_module(self, ten_function, status, color):

        """Get a dictionary about bug's number, status, color of top-ten functions"""

        one_module = {}
        one_module['data'] = ten_function  
        one_module['name'] = status 
        one_module['color'] = color
        return one_module

    def ten_fun_module(self, date, project_name):

        """Get a list obtain three states of bug and three colors of top-ten functions"""

        function_data_1 = self.get_function_data(date, project_name)
        #print function_data_1
        module = []
        status_list = ['open', 'fixed', 'regression']
        color_list = ['#F6BD0F', '#AFD8F8', '#8BBA00']

        top_ten_fun = {}
        for i in xrange(0, 3):
            fun_1 = self.get_functions(self.get_functon_id(), function_data_1, status_list[i])
            if i is 0:
                top_ten_fun = self.function_sort(fun_1)
                module.append(self.get_one_module(top_ten_fun, status_list[i], color_list[i]))
            else:
                fun = {}
                for key in fun_1.keys():
                    if key in top_ten_fun.keys():
                        fun[key] = fun_1[key]
                module.append(self.get_one_module(fun, status_list[i], color_list[i]))

        #self.imp.close()
        return module

    def get_daily_bugs(self, project_name):
        self.imp.cur.execute("select date,daily_open,daily_fix from person_static \
                     where date>='2016-08-05' and project_name='%s'" % (project_name))
        daily_bugs = self.imp.cur.fetchall()
        list1 = []
        list2 = []
        daily_data = [{"data":list1, "name":"daily_open"}, {"data":list2, "name":"daily_fix"}]
        daily_date = ''
        flag = 0
        for bug in daily_bugs:
            if str(bug[0]) != daily_date:
                if flag == 1:
                    list1.append([daily_date, open_count])
                    list2.append([daily_date, fix_count])
                daily_date = str(bug[0])
                open_count = 0
                fix_count = 0
                open_count += int(bug[1])
                fix_count += int(bug[2])
            else:
                open_count += int(bug[1])
                fix_count += int(bug[2])
                flag = 1
        list1.append([daily_date, open_count])
        list2.append([daily_date, fix_count])
        list1.sort(key=lambda x:x[0])
        list2.sort(key=lambda x:x[0])
        return daily_data


#test = ExportStc()
#print test.get_project_static('Simba6_na')
#test.ten_fun_module('2017-04-25','Simba6_na')
#print test.date_record_yes_no('2017-03-13','Catwoman')
# print 'big_team_static','*'*100
#print test.get_team_static('2017-04-25','Simba6_na')
#print test.get_person_static('2017-04-25','Simba6_na')
# print 'team_static','*'*100
# print test.get_team_static('2017-03-13','SAM')
#aa = test.get_bug_list("Smeagol")
#test.get_daily_bugs('Aragorn')

# a = test.get_team_static('2017-03-14','Simba6_na')
# for i in a.keys():
#     print i, a[i]

# print 'fun_module','*'*100
# print test.ten_fun_module('2017-03-14','Simba6_na')
# print 'person_static','*'*100
# print test.get_person_static('2017-03-14','Simba6_na')

