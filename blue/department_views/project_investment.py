from __future__ import division
import sys
sys.path.append("../..")
from settings import conf
from script.imports import Bugdb
import time
import datetime

MAIN_PROJECT_NUM = 5

class ExportProjectInvestment():
    def __init__(self):
        self.imp = Bugdb('localhost', conf.MYSQLUSERNAME, 
                            conf.MYSQLPASSWORD, 'hades')

    def get_recent_week(self, errweek, value):
        if value == "All_projects":
            self.imp.cur.execute(
                'select MAX(weeks) from dep_weekly_person where weeks <= "%s"' % errweek)
        else:
            self.imp.cur.execute(
                'select MAX(weeks) from dep_weekly_person where weeks <= "%s" and project_name="%s"' % (errweek,value))
        recent_week = self.imp.cur.fetchall()
        value = recent_week[0][0]
        return value

    def week_record_yes_no(self, week, value):
        if value == "CD_SWD1_All_projects":
            self.imp.cur.execute('select * from dep_weekly_person where weeks="%s"\
             and project_name="%s"' % (week, conf.CD_SWD1_PROJECT[0]))
        elif value == "CD_SWD2_All_projects":
            self.imp.cur.execute('select * from dep_weekly_person where weeks="%s"\
             and project_name="%s"' % (week, conf.CD_SWD2_PROJECT[0]))
        else:
            self.imp.cur.execute('select * from dep_weekly_person where weeks="%s" and project_name="%s"' % (week,value))
        result_week = self.imp.cur.fetchall()
        if result_week:
            return True
        else:
            return False

    def get_team_investment(self, week, value):
        team_investment = {}
        big_list1 = []
        big_list2 = []
        department_investment = [{"data":big_list1, "name":"finish_rate"}, {"data":big_list2, "name":"ref_reg_rate"}]
        if (value in conf.CD_SWD1_PROJECT) or (value == 'CD_SWD1_All_projects'):
            team_investment["CD_SWD1"] = department_investment
        if (value in conf.CD_SWD2_PROJECT) or (value == 'CD_SWD2_All_projects'):
            team_investment["CD_SWD2"] = department_investment
        swd1_week = {}
        date_tuple = {}
        all_team = []
        if (value in conf.CD_SWD1_PROJECT) or (value == 'CD_SWD1_All_projects'):
            all_team = ['CD_SWD1_APP', 'CD_SWD1_SYS', 'CD_SWD1_MID', 'CD_SWD1_TELECOM', 'CD_SWD1_SPM', 'CD_SWD1_INT']
        if (value in conf.CD_SWD2_PROJECT) or (value == 'CD_SWD2_All_projects'):
            all_team = ['CD_SWD2_APP', 'CD_SWD2_SYS', 'CD_SWD2_FRM', 'CD_SWD2_TELECOM', 'CD_SWD2_SPM', 'CD_SWD2_INT']

        for team in all_team:
            if value == "CD_SWD1_All_projects":
                self.imp.cur.execute('select open_total, fix, ref_reg, date, \
                                weeks from dep_weekly_person where section="%s" \
                                and project_name in %s' % (team, tuple(conf.CD_SWD1_PROJECT)))
            elif value == "CD_SWD2_All_projects":
                self.imp.cur.execute('select open_total, fix, ref_reg, date, \
                                weeks from dep_weekly_person where section="%s" \
                                and project_name in %s' % (team, tuple(conf.CD_SWD2_PROJECT)))
            else:
                self.imp.cur.execute('select open_total, fix, ref_reg, date, \
                                weeks from dep_weekly_person where section="%s" and project_name="%s"' % (team,value))
            bugsinfo_tuple = self.imp.cur.fetchall()
            item = ["open_total","fix","ref_reg","date","weeks"]     
            bugs_list = [] 
            for one_bug in bugsinfo_tuple:
                one_info = {}
                for i in xrange(len(item)):
                    one_info[item[i]] = one_bug[i]
                bugs_list.append(one_info)
            one_team_data = []
            team_investment[team] = one_team_data
            list1 = []
            list2 = []
            finish_data = {"data":list1, "name":"finish_rate"}
            ref_reg_data = {"data":list2, "name":"ref_reg_rate"}
            one_team_data.append(finish_data)
            one_team_data.append(ref_reg_data)
            every_week = {}
            for bug in bugs_list:
                if team == 'CD_SWD1_APP' or team == 'CD_SWD2_APP':
                    if bug["weeks"] == week and bug["weeks"] not in date_tuple.keys():
                        date_tuple[bug["weeks"]] = bug["date"]
                else:
                    pass
                if bug["date"] not in every_week.keys():
                    every_week[bug["date"]] = {}
                    every_week[bug["date"]]["total"] = 0
                    every_week[bug["date"]]["fix"] = 0
                    every_week[bug["date"]]["ref_reg"] = 0
                total = bug["open_total"] + bug["fix"]
                every_week[bug["date"]]["total"] += total
                every_week[bug["date"]]["fix"] += bug["fix"]
                every_week[bug["date"]]["ref_reg"] += bug["ref_reg"]
            for key in every_week.keys():
                if key not in swd1_week.keys():
                    swd1_week[key] ={}
                    swd1_week[key]["total"] = 0
                    swd1_week[key]["fix"] = 0
                    swd1_week[key]["ref_reg"] = 0                    
                swd1_week[key]["total"] += every_week[key]["total"]
                swd1_week[key]["fix"] += every_week[key]["fix"]
                swd1_week[key]["ref_reg"] += every_week[key]["ref_reg"]

            for key in every_week.keys():
                if every_week[key]["total"] != 0:
                    finish_rate = round(every_week[key]["fix"]/every_week[key]["total"], 2)
                    ref_reg_rate = round(every_week[key]["ref_reg"]/every_week[key]["total"], 2)
                else:
                    finish_rate = 0.0
                    ref_reg_rate = 0.0
                key = key.strftime("%Y-%m-%d")
                list1.append([key, finish_rate])
                list2.append([key, ref_reg_rate])

        for key in swd1_week.keys():
            if swd1_week[key]["total"] != 0:
                finish_rate = round(swd1_week[key]["fix"]/swd1_week[key]["total"], 2)
                ref_reg_rate = round(swd1_week[key]["ref_reg"]/swd1_week[key]["total"], 2)
            else:
                finish_rate = 0.0
                ref_reg_rate = 0.0
            key = key.strftime("%Y-%m-%d")
            big_list1.append([key, finish_rate])
            big_list2.append([key, ref_reg_rate])

        date_list = []
        date_list.append((date_tuple.values()[0] - datetime.timedelta(days=7)).strftime("%Y-%m-%d"))
        date_list.append(date_tuple.values()[0].strftime("%Y-%m-%d"))
        print '*'*50
        return team_investment, date_list

    def get_project_investment(self, week, value):
        if value == 'CD_SWD1_All_projects':
            self.imp.cur.execute('select bugusers.email,dep_weekly_person.section,\
            dep_weekly_person.open_total,dep_weekly_person.fix,dep_weekly_person.ref_reg,\
            dep_weekly_person.project_name,dep_weekly_person.date,dep_weekly_person.weeks \
            from dep_weekly_person,bugusers where dep_weekly_person.user_id=bugusers.id \
            and dep_weekly_person.weeks="%s" and dep_weekly_person.section like "%s"' % (week, 'CD_SWD1%'))
        elif value == 'CD_SWD2_All_projects':
            self.imp.cur.execute('select bugusers.email,dep_weekly_person.section,\
            dep_weekly_person.open_total,dep_weekly_person.fix,dep_weekly_person.ref_reg,\
            dep_weekly_person.project_name,dep_weekly_person.date,dep_weekly_person.weeks \
            from dep_weekly_person,bugusers where dep_weekly_person.user_id=bugusers.id \
            and dep_weekly_person.weeks="%s" and dep_weekly_person.section like "%s"' % (week, 'CD_SWD2%'))
        elif value in conf.CD_SWD1_PROJECT:
            self.imp.cur.execute('select bugusers.email,dep_weekly_person.section,\
            dep_weekly_person.open_total,dep_weekly_person.fix,dep_weekly_person.ref_reg,\
            dep_weekly_person.project_name,dep_weekly_person.date,dep_weekly_person.weeks \
            from dep_weekly_person,bugusers where dep_weekly_person.user_id=bugusers.id \
            and dep_weekly_person.weeks="%s" and dep_weekly_person.section like "%s" and project_name="%s"' % (week,'CD_SWD1%',value))
        elif value in conf.CD_SWD2_PROJECT:
            self.imp.cur.execute('select bugusers.email,dep_weekly_person.section,\
            dep_weekly_person.open_total,dep_weekly_person.fix,dep_weekly_person.ref_reg,\
            dep_weekly_person.project_name,dep_weekly_person.date,dep_weekly_person.weeks \
            from dep_weekly_person,bugusers where dep_weekly_person.user_id=bugusers.id \
            and dep_weekly_person.weeks="%s" and dep_weekly_person.section like "%s" and project_name="%s"' % (week,'CD_SWD2%',value))
        bugsinfo_tuple = self.imp.cur.fetchall()
        item = ["email","section","open_total","fix","ref_reg","project_name","date","weeks"]     
        bugs_list = [] 
        for one_bug in bugsinfo_tuple:
            one_info = {}
            for i in xrange(len(item)):
                one_info[item[i]] = one_bug[i]
            bugs_list.append(one_info)

        weekly  = []
        personal_investment = {}
        personal_bug_num = {}
        section_investment = {}
        department_investment = {}
        department_investment["open"] = {}
        department_investment["fix"] = {}
        main_projects = {}

        for bug in bugs_list:
            if bug["email"] not in personal_investment.keys():
                personal_investment[bug["email"]] = {}
                personal_investment[bug["email"]]["section"] = bug["section"]
            if bug["email"] not in personal_bug_num.keys():
                personal_bug_num[bug["email"]] = {}
                personal_bug_num[bug["email"]]["total"] = 0
                personal_bug_num[bug["email"]]["fix"] = 0
                personal_bug_num[bug["email"]]["ref_reg"] = 0
            if bug["project_name"] not in personal_investment[bug["email"]].keys():
                personal_investment[bug["email"]][bug["project_name"]] = {}

            personal_investment[bug["email"]][bug["project_name"]]["open"] = bug["open_total"]
            personal_investment[bug["email"]][bug["project_name"]]["fix"] = bug["fix"]

            total = bug["open_total"] + bug["fix"]
            personal_bug_num[bug["email"]]["total"] += total
            personal_bug_num[bug["email"]]["fix"] += bug["fix"]
            personal_bug_num[bug["email"]]["ref_reg"] += bug["ref_reg"]

            if bug["section"] not in section_investment.keys():
                section_investment[bug["section"]] = {}
                section_investment[bug["section"]]["open"] = {}
                section_investment[bug["section"]]["fix"] = {}
            if bug["project_name"] not in section_investment[bug["section"]]["open"].keys():
                section_investment[bug["section"]]["open"][bug["project_name"]] = 0
            if bug["project_name"] not in section_investment[bug["section"]]["fix"].keys():
                section_investment[bug["section"]]["fix"][bug["project_name"]] = 0
            section_investment[bug["section"]]["open"][bug["project_name"]] += int(bug["open_total"])
            section_investment[bug["section"]]["fix"][bug["project_name"]] += int(bug["fix"])

            if bug["project_name"] not in department_investment["open"].keys():
                department_investment["open"][bug["project_name"]] = 0
            if bug["project_name"] not in department_investment["fix"].keys():
                department_investment["fix"][bug["project_name"]] = 0
            if bug["project_name"] not in main_projects.keys():
                main_projects[bug["project_name"]] = 0
            department_investment["open"][bug["project_name"]] += int(bug["open_total"])
            department_investment["fix"][bug["project_name"]] += int(bug["fix"])
            main_projects[bug["project_name"]] += (int(bug["open_total"]) + int(bug["fix"]))

        if (value in conf.CD_SWD1_PROJECT) or (value == 'CD_SWD1_All_projects'):
            section_investment["CD_SWD1"] = department_investment
        if (value in conf.CD_SWD2_PROJECT) or (value == 'CD_SWD2_All_projects'):
            section_investment["CD_SWD2"] = department_investment

        for key in personal_bug_num.keys():
            if personal_bug_num[key]["total"] != 0:
                personal_bug_num[key]["finish_rate"] = \
                            round(personal_bug_num[key]["fix"]/personal_bug_num[key]["total"],2)
                personal_bug_num[key]["ref_reg_rate"] = \
                            round(personal_bug_num[key]["ref_reg"]/personal_bug_num[key]["total"],2)
            else:
                personal_bug_num[key]["finish_rate"] = 0.0
                personal_bug_num[key]["ref_reg_rate"] = 0.0
        list_rate = sorted(personal_bug_num.iteritems(), key=lambda d: (d[1]["finish_rate"],d[1]["total"]), reverse = True)
        sorted_list = sorted(main_projects.items(), key=lambda d: d[1], reverse = True)
        main_projects_list = []
        for i in range(len(sorted_list)):
            if i < MAIN_PROJECT_NUM:
                main_projects_list.append(sorted_list[i][0])
            else:
                break
        project_name = []
        for project in conf.PROJECT_DICT.keys():
            project_name.append(project)
        other_project_list = [i for i in project_name if i not in main_projects_list]

        for key in personal_investment.keys():
            personal_investment[key]["Others"] = {}
            personal_investment[key]["Others"]["open"] = 0
            personal_investment[key]["Others"]["fix"] = 0
            for project in personal_investment[key].keys():
                if project in other_project_list:
                    personal_investment[key]["Others"]["open"] += personal_investment[key][project]["open"]
                    personal_investment[key]["Others"]["fix"] += personal_investment[key][project]["fix"]
        main_projects_list.append("Others")

        main_section_investment ={}
        for section in section_investment.keys():
            main_section_investment[section] = {}
            for status in section_investment[section].keys():
                main_section_investment[section][status] = {}
                main_section_investment[section][status]["Others"] = 0
                for project in section_investment[section][status].keys():
                    if project not in other_project_list:
                        main_section_investment[section][status][project] = section_investment[section][status][project]
                    else:
                        main_section_investment[section][status]["Others"] += section_investment[section][status][project]

        # if value == "All_projects":
        #     return personal_investment, list_rate, main_section_investment, main_projects_list
        # else:
        #     projects_list = [value]
        #     return personal_investment, list_rate, section_investment, projects_list
        if value in conf.PROJECT_DICT.keys():
            projects_list = [value]
            return personal_investment, list_rate, section_investment, projects_list
        else:
            return personal_investment, list_rate, main_section_investment, main_projects_list


#ExportProject = ExportProjectInvestment()
#print ExportProject.get_project_investment('2017-18', 'CD_SWD1_All_projects')
#print ExportProject.get_team_investment('2017-18', 'Catwoman')
