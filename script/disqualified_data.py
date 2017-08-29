#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
import os
import re
import sys
sys.path.append("..")
from settings import conf
from imports import Bugdb
import datetime
import send_mail
import xlwt
import style
from dep_statistics import DepartmentStatis

class SubstandardKPI():
    def __init__(self, TIMEBEGIN, TIMEEND, attach_path, image_path):
        self.imp = Bugdb('localhost', conf.MYSQLUSERNAME,conf.MYSQLPASSWORD, 'hades')
        self.TIMEBEGIN = TIMEBEGIN
        self.TIMEEND = TIMEEND
        self.attach_path = attach_path
        self.image_path = image_path

    def get_all_infos(self):
        # self.imp.cur.execute("select base.summary, base.priority, base.bug_status, base.created_date,\
        #         base.closed_date, base.verified_sw_date, bugusers.section,team.team,base.val_refuse,base.regression,\
        #         base.project_name,base.bug_id,base.type,base.bug_status,base.assigned_date,base.ipr_value,base.regression_date,\
        #         base.refused_date,bugusers.email from base,bugusers,team where base.assigner=bugusers.id and bugusers.department='swd1' and \
        #         bugusers.team_id=team.team_id and (base.priority='P0 (Urgent)' or (base.priority='P1 (Quick)' and ipr_value>300))")
        self.imp.cur.execute("select base.summary, base.priority, base.bug_status, base.created_date,\
                base.closed_date, base.verified_sw_date, bugusers.section,team.team,base.val_refuse,base.regression,\
                base.project_name,base.bug_id,base.type,base.assigned_date,base.ipr_value,base.regression_date,\
                base.refused_date,bugusers.email from base,bugusers,team \
                where ((base.assigner=bugusers.id or base.resolver=bugusers.id or base.long_text_read_only=bugusers.id) and bugusers.department like 'WMD-PIC CD-SWD1%') and \
                bugusers.team_id=team.team_id and bugusers.section!='OTHERS' and base.type ='Defect' and (base.priority='P0 (Urgent)' or (base.priority='P1 (Quick)' and ipr_value>300))")

        all_infos = self.imp.cur.fetchall()
        item = ["summary", "priority", "bug_status", "created_date", "closed_date", 
                 "verified_sw_date", "section", "team", "val_refuse", "regression", 
                 "project_name", "bug_id", "type", "assigned_date","ipr_value", 
                 "regression_date", "refused_date", "assigner"]
        infos_list = []
        for info in all_infos:
            one_info = {}
            for i in xrange(len(item)):
                one_info[item[i]] = info[i]
            infos_list.append(one_info)
        return infos_list

    def original_data(self):
        infos_list = self.get_all_infos()
        complete_bugs = []
        for info in infos_list:
            if info["verified_sw_date"] != None:
                resolved_date = info["verified_sw_date"].strftime("%Y-%m-%d")
            elif info["closed_date"] != None:
                resolved_date = info["closed_date"].strftime("%Y-%m-%d")
            else:
                continue
            if resolved_date >= self.TIMEBEGIN and resolved_date <= self.TIMEEND:
                date_list = ["assigned_date", "verified_sw_date", "refused_date", "regression_date"]
                for date_type in date_list:
                    if info[date_type] is not None:
                        info[date_type] = info[date_type].strftime("%Y-%m-%d %H:%M:%S")
                if '[Ergo]' in info["summary"] and '[CR]' not in info["summary"]:
                    info["isCR"] = "YES"
                else:
                    info["isCR"] = "NO"
                if re.search('\[VF\d+\]', info["summary"]):
                    info["priority"] = "QC"
                complete_bugs.append(info)
        return complete_bugs

    def create_dict(self, *args):
        personal_dict = {}
        team_dict = {}
        project_dict = {}
        infos_list = self.get_all_infos()
        for section in conf.TEAM.keys():
            team_dict[section] = {}
            personal_dict[section] = {}
            for arg in args:
                team_dict[section][arg] = 0
            if conf.TEAM[section] != []:
                for team in conf.TEAM[section]:
                    team_dict[section][team] = {}
                    for arg in args:
                        team_dict[section][team][arg] = 0
        for project in conf. PROJECT_DICT.keys():
            project_dict[project] = {}
            for arg in args:
                project_dict[project][arg] = 0
        for info in infos_list:
            if info["assigner"] not in personal_dict[info["section"]].keys():
                personal_dict[info["section"]][info["assigner"]] = {}
                for arg in args:
                    personal_dict[info["section"]][info["assigner"]][arg] = 0
        return team_dict, project_dict, personal_dict

    def feature_quality(self):
        infos_list = self.get_all_infos()
        (quality, quality_project, personal_quality) = self.create_dict("total_defect", "Ergo_defect")
        for info in infos_list:
            created_date = info["created_date"].strftime("%Y-%m-%d")
            if created_date >= self.TIMEBEGIN and created_date <= self.TIMEEND:
                quality[info["section"]]["total_defect"] += 1
                quality_project[info["project_name"]]["total_defect"] += 1
                personal_quality[info["section"]][info["assigner"]]["total_defect"] += 1
                if '[Ergo]' in info["summary"] and '[CR]' not in info["summary"]:
                    quality[info["section"]]["Ergo_defect"] += 1
                    quality_project[info["project_name"]]["Ergo_defect"] += 1
                    personal_quality[info["section"]][info["assigner"]]["Ergo_defect"] += 1
                if info["team"] != info["section"]:
                    quality[info["section"]][info["team"]]["total_defect"] += 1
                    if '[Ergo]' in info["summary"] and '[CR]' not in info["summary"]:
                        quality[info["section"]][info["team"]]["Ergo_defect"] += 1

        for section in personal_quality.keys():
            for assigner in personal_quality[section].keys():
                if personal_quality[section][assigner]["total_defect"] != 0:
                    personal_quality[section][assigner]["FR_Quality"] = str(round(personal_quality[section][assigner]["Ergo_defect"]/personal_quality[section][assigner]["total_defect"],3)) + "%"
                else:
                    personal_quality[section][assigner]["FR_Quality"] = "0.0%"

        for key in quality.keys():
            if quality[key]["total_defect"] != 0:
                quality[key]["FR_Quality"] = str(round(quality[key]["Ergo_defect"]/quality[key]["total_defect"],3)) + "%"
            else:
                quality[key]["FR_Quality"] = "0.0%"
            if len(quality[key].keys()) > 3: 
                for key2 in quality[key].keys():
                    if key2 not in ("Ergo_defect","total_defect","FR_Quality"):
                        if quality[key][key2]["total_defect"] != 0:
                            quality[key][key2]["FR_Quality"] = \
                                str(round(quality[key][key2]["Ergo_defect"]/quality[key][key2]["total_defect"],3)) + "%"
                        else:
                            quality[key][key2]["FR_Quality"] = "0.0%"
        for key in quality_project.keys():
            if quality_project[key]["total_defect"] != 0:
                quality_project[key]["FR_Quality"] = \
                    str(round(quality_project[key]["Ergo_defect"]/quality_project[key]["total_defect"],3)) + "%"
            else:
                quality_project[key]["FR_Quality"] = "0.0%"
        return quality, quality_project, personal_quality

    def refuse_defect(self):
        infos_list = self.original_data()
        (refuse, refuse_project, personal_refuse) = self.create_dict("resolved_defect", "refused_defect", "regression_defect")
        for info in infos_list:
            refuse[info["section"]]["resolved_defect"] += 1
            refuse_project[info["project_name"]]["resolved_defect"] += 1
            personal_refuse[info["section"]][info["assigner"]]["resolved_defect"] += 1
            if info["val_refuse"] == "YES":
                refuse[info["section"]]["refused_defect"] += 1
                refuse_project[info["project_name"]]["refused_defect"] += 1
                personal_refuse[info["section"]][info["assigner"]]["refused_defect"] += 1
            if info["regression"] == "YES":
                refuse[info["section"]]["regression_defect"] += 1
                refuse_project[info["project_name"]]["regression_defect"] += 1
                personal_refuse[info["section"]][info["assigner"]]["regression_defect"] += 1
            if info["team"] != info["section"]:
                refuse[info["section"]][info["team"]]["resolved_defect"] += 1   
                if info["val_refuse"] == "YES":
                    refuse[info["section"]][info["team"]]["refused_defect"] += 1 
                if info["regression"] == "YES":
                    refuse[info["section"]][info["team"]]["regression_defect"] += 1               
        for section in  personal_refuse.keys()            :
            for assigner in personal_refuse[section].keys():
                if personal_refuse[section][assigner]["resolved_defect"] != 0:
                    personal_refuse[section][assigner]["refused_rate"] = str(round(personal_refuse[section][assigner]["refused_defect"]/personal_refuse[section][assigner]["resolved_defect"],3)) + "%"
                    personal_refuse[section][assigner]["regression_rate"] = str(round(personal_refuse[section][assigner]["regression_defect"]/personal_refuse[section][assigner]["resolved_defect"],3)) + "%"
                else:
                    personal_refuse[section][assigner]["refused_rate"] = "0.0%"
                    personal_refuse[section][assigner]["regression_rate"] = "0.0%"
        for key in refuse.keys():
            if refuse[key]["resolved_defect"] != 0:
                refuse[key]["refused_rate"] = str(round(refuse[key]["refused_defect"]/refuse[key]["resolved_defect"],3)) + "%"
                refuse[key]["regression_rate"] = str(round(refuse[key]["regression_defect"]/refuse[key]["resolved_defect"],3)) + "%"
            else:
                refuse[key]["refused_rate"] = "0.0%"
                refuse[key]["regression_rate"] = "0.0%"
            if len(refuse[key].keys()) > 3: 
                for key2 in refuse[key].keys():
                    if key2 not in ("resolved_defect","refused_defect","refused_rate","regression_defect","regression_rate"):
                        if refuse[key][key2]["resolved_defect"] != 0:
                            refuse[key][key2]["refused_rate"] = \
                                str(round(refuse[key][key2]["refused_defect"]/refuse[key][key2]["resolved_defect"],3)) + "%"
                            refuse[key][key2]["regression_rate"] = \
                                str(round(refuse[key][key2]["regression_defect"]/refuse[key][key2]["resolved_defect"],3)) + "%"
                        else:
                            refuse[key][key2]["refused_rate"] = "0.0%"
                            refuse[key][key2]["regression_rate"] = "0.0%"
        for key in refuse_project.keys():
            if refuse_project[key]["resolved_defect"] != 0:
                refuse_project[key]["refused_rate"] = \
                    str(round(refuse_project[key]["refused_defect"]/refuse_project[key]["resolved_defect"],3)) + "%"
                refuse_project[key]["regression_rate"] = \
                    str(round(refuse_project[key]["regression_defect"]/refuse_project[key]["resolved_defect"],3)) + "%"
            else:
                refuse_project[key]["refused_rate"] = "0.0%"
                refuse_project[key]["regression_rate"] = "0.0%"
        return refuse, refuse_project, personal_refuse

    def pr_process_cycle(self, pr_type):
        infos_list = self.original_data()
        (process, process_project, personal_process) = self.create_dict("<=7D", ">7D&<=10D", ">10D&<=14D", ">14D", "days", "total")
        for info in infos_list:
            if pr_type == "QC":
                condition = re.search('\[VF\d+\]', info["summary"])
            elif pr_type in ("P0 (Urgent)", "P1 (Quick)"):
                condition = (info["priority"] == pr_type)
            if condition and info["verified_sw_date"] != None:
                verified_sw_date = datetime.datetime.strptime(info["verified_sw_date"],'%Y-%m-%d %H:%M:%S')
                days = (verified_sw_date - info["created_date"]).days
                # if days >100:
                #     print info
                if days <= 7:
                    process[info["section"]]["<=7D"] += 1
                elif days > 7 and days <= 10:
                    process[info["section"]][">7D&<=10D"] += 1
                elif days > 10 and days <= 14:
                    process[info["section"]][">10D&<=14D"] += 1
                else:
                    process[info["section"]][">14D"] += 1
                process[info["section"]]["total"] += 1
                process[info["section"]]["days"] += days#.append(days)
                process_project[info["project_name"]]["total"] += 1
                process_project[info["project_name"]]["days"] += days
                personal_process[info["section"]][info["assigner"]]["total"] += 1
                personal_process[info["section"]][info["assigner"]]["days"] += days
                if info["team"] != info["section"]:
                    process[info["section"]][info["team"]]["total"] += 1
                    process[info["section"]][info["team"]]["days"] += days
        for section in personal_process.keys():
            for assigner in personal_process[section].keys():
                if personal_process[section][assigner]["total"] != 0:
                    personal_process[section][assigner]["average"] = str(round(personal_process[section][assigner]["days"]/personal_process[section][assigner]["total"], 3)) + "D"
                else:
                    personal_process[section][assigner]["average"] = "0.0D"
        for key in process.keys():
            if process[key]["total"] != 0:
                process[key]["average"] = str(round(process[key]["days"]/process[key]["total"], 3)) + "D"
            else:
                process[key]["average"] = "0.0D"
            if len(process[key].keys()) > 7: 
                for key2 in process[key].keys():
                    if key2 not in ("<=7D",">7D&<=10D",">10D&<=14D",">14D","average","days","total"):
                        if process[key][key2]["total"] != 0:
                            process[key][key2]["average"] = str(round(process[key][key2]["days"]/process[key][key2]["total"], 3)) + "D"
                        else:
                            process[key][key2]["average"] = "0.0D"
        for key in process_project.keys():
            if process_project[key]["total"] != 0:
                process_project[key]["average"] = str(round(process_project[key]["days"]/process_project[key]["total"], 3)) + "D"
            else:
                process_project[key]["average"] = "0.0D"
        return process, process_project, personal_process

    def send_email(self):
        depa = DepartmentStatis()
        html = self.css_style()
        html += '各team不达标项的详细数据分析 (%s到%s)<br/>' % (self.TIMEBEGIN, self.TIMEEND) 

        # html += '<h4>1. QC处理周期(Target:7D): 数据为处理周期>7D的defect</h4>' 
        # html += '''
        #     <table class="gridtable">
        #     <tr><th>处理周期分布</th>
        #         <th><=7D</th>
        #         <th>>7D&<=10D</th>
        #         <th>>10D&<=14D</th>
        #         <th>>14D</th>
        #         <th>平均处理周期</th>
        #     </tr>
        # '''
        (process, process_project, personal_process) = self.pr_process_cycle("QC")
        # for section in process.keys():
        #     if float(process[section]["average"][:-1]) >7:
        #         html += '<tr><th>%s</th>' % section
        #         html += '<td>%s</td>' % process[section]["<=7D"]
        #         html += '<td>%s</td>' % process[section][">7D&<=10D"]
        #         html += '<td>%s</td>' % process[section][">10D&<=14D"]
        #         html += '<td>%s</td>' % process[section][">14D"]
        #         html += '<td class="col">%s</td></tr>' % process[section]["average"]
        # html += '</table>'
        # html += '<br/><h4>2. 各team的refuse defect数据:<h4>'
        # html += '''
        #     <table class="gridtable">
        #     <tr><th>Defect数据</th>
        #         <th>Resolved defect个数</th>
        #         <th>Refused defect个数</th>
        #         <th>Refused Rate</th>
        #     </tr>
        # '''
        (refuse, refuse_project, personal_refuse) = self.refuse_defect()
        # for section in refuse.keys():
        #     html += '<tr><th>%s</th>' % section
        #     html += '<td>%s</td>' % refuse[section]["resolved_defect"]
        #     html += '<td>%s</td>' % refuse[section]["refused_defect"]
        #     html += '<td class="col">%s</td></tr>' % refuse[section]["refused_rate"]
        # html += '</table>'
        # html += '<br/><h4>3. 各team的Feature Quality:<h4>'
        # html += '''
        #     <table class="gridtable">
        #     <tr><th>Feature Quality</th>
        #         <th>Total defect个数</th>
        #         <th>Ergo defect个数</th>
        #         <th>FR Quality</th>
        #     </tr>
        # '''
        (quality, quality_project, personal_quality) = self.feature_quality()
        # for section in quality.keys():
        #     html += '<tr><th>%s</th>' % section
        #     html += '<td>%s</td>' % quality[section]["total_defect"]
        #     html += '<td>%s</td>' % quality[section]["Ergo_defect"]
        #     html += '<td class="col">%s</td></tr>' % quality[section]["FR_Quality"]
        # html += '</table>'
        html += depa.mail_bottom_content()
        self.add_attach(process, refuse, quality, process_project, refuse_project, quality_project,
                            personal_process, personal_refuse, personal_quality)
        img_dir = self.image_path
        attach_dir = os.path.split(self.attach_path)[0]
        self.mail_sending(html, img_dir, attach_dir)

    def work_book(self, name, workbook, titles):
        title_style = style.get_body_title_style(font_color=0x1, bg_color=0x30)
        table = workbook.add_sheet(name, cell_overwrite_ok=True)
        j = 0
        for title in titles:
            table.write(0, j, title, title_style)
            table.col(j).width = 256*13
            j += 1   
        return table

    def add_attach(self, process, refuse, quality, pro_project, ref_project, qua_project, 
                       personal_process, personal_refuse, personal_quality):
        (p0_process, p0_project, p0_personal) = self.pr_process_cycle("P0 (Urgent)")
        (p1_process, p1_project, p1_personal) = self.pr_process_cycle("P1 (Quick)")
        workbook = xlwt.Workbook(encoding='utf-8')
        titles = ["Project", "Resolved个数", "P0", "P0处理周期", "P1>300", "P1>300处理周期",
                    "QC", "QC处理周期", "Refused个数", "Refused Rate", "Regression 个数",
                    "Regression rate", "Ergo defect个数", "FR Quality"]
        info_style = style.get_body_info_style(color=0x0, is_horz_center=True,font_size=200)
        info_sty = style.get_body_info_style(color=0x0, is_horz_center=True,font_size=150)
        table = self.work_book("Project Data Distribution", workbook, titles)
        i = 1
        for project in ref_project.keys():
            table.write(i, 0, project, info_style)
            table.write(i, 1, ref_project[project]["resolved_defect"], info_sty)
            table.write(i, 2, p0_project[project]["total"], info_sty)
            table.write(i, 3, p0_project[project]["average"], info_sty)
            table.write(i, 4, p1_project[project]["total"], info_sty)
            table.write(i, 5, p1_project[project]["average"], info_sty)
            table.write(i, 6, pro_project[project]["total"], info_sty)
            table.write(i, 7, pro_project[project]["average"], info_sty)
            table.write(i, 8, ref_project[project]["refused_defect"], info_sty)
            table.write(i, 9, ref_project[project]["refused_rate"], info_sty)
            table.write(i, 10, ref_project[project]["regression_defect"], info_sty)
            table.write(i, 11, ref_project[project]["regression_rate"], info_sty)
            table.write(i, 12, qua_project[project]["Ergo_defect"], info_sty)
            table.write(i, 13, qua_project[project]["FR_Quality"], info_sty)
            i += 1
        titles = ["Team", "Resolved个数", "P0", "P0处理周期", "P1>300", "P1>300处理周期",
                    "QC", "QC处理周期", "Refused个数", "Refused Rate", "Regression 个数",
                    "Regression rate", "Ergo defect个数", "FR Quality"]  
        table = self.work_book("Team Data Distribution", workbook, titles)
        i = 1
        for section in refuse.keys():
            table.write(i, 0, section, info_style)
            table.write(i, 1, refuse[section]["resolved_defect"], info_sty)
            table.write(i, 2, p0_process[section]["total"], info_sty)
            table.write(i, 3, p0_process[section]["average"], info_sty)
            table.write(i, 4, p1_process[section]["total"], info_sty)
            table.write(i, 5, p1_process[section]["average"], info_sty)
            table.write(i, 6, process[section]["total"], info_sty)
            table.write(i, 7, process[section]["average"], info_sty)
            table.write(i, 8, refuse[section]["refused_defect"], info_sty)
            table.write(i, 9, refuse[section]["refused_rate"], info_sty)
            table.write(i, 10, refuse[section]["regression_defect"], info_sty)
            table.write(i, 11, refuse[section]["regression_rate"], info_sty)
            table.write(i, 12, quality[section]["Ergo_defect"], info_sty)
            table.write(i, 13, quality[section]["FR_Quality"], info_sty)
            if section in ("CD_app", "CD_mid", "CD_sys", 'CD_INT', 'CD_Telecom'):
                for team in refuse[section].keys():
                    if type(refuse[section][team]) == dict and "leader" not in team:
                        i += 1
                        table.write(i, 0, team, info_style)
                        table.write(i, 1, refuse[section][team]["resolved_defect"], info_sty)
                        table.write(i, 2, p0_process[section][team]["total"], info_sty)
                        table.write(i, 3, p0_process[section][team]["average"], info_sty)
                        table.write(i, 4, p1_process[section][team]["total"], info_sty)
                        table.write(i, 5, p1_process[section][team]["average"], info_sty)
                        table.write(i, 6, process[section][team]["total"], info_sty)
                        table.write(i, 7, process[section][team]["average"], info_sty)
                        table.write(i, 8, refuse[section][team]["refused_defect"], info_sty)
                        table.write(i, 9, refuse[section][team]["refused_rate"], info_sty)
                        table.write(i, 10, refuse[section][team]["regression_defect"], info_sty)
                        table.write(i, 11, refuse[section][team]["regression_rate"], info_sty)
                        table.write(i, 12, quality[section][team]["Ergo_defect"], info_sty)
                        table.write(i, 13, quality[section][team]["FR_Quality"], info_sty)
            i += 1

        titles = ["bug_id", "project_name", "type", "bug_status", "assigner", "assigned_date",
                    "verified_sw_date","team", "priority", "ipr_value", "isCR", "val_refuse",
                    "refused_date", "regression", "regression_date", "summary"]
        table = self.work_book("original data", workbook, titles)
        infos = self.original_data()
        i = 1
        for info in infos:
            j = 0
            for key in titles:
                table.write(i, j, info[key], info_sty)
                j += 1
            i += 1

        titles = ["Team", "Assigner", "Resolved个数", "P0", "P0处理周期", "P1>300", "P1>300处理周期",
                    "QC", "QC处理周期", "Refused个数", "Refused Rate", "Regression 个数",
                    "Regression rate", "Ergo defect个数", "FR Quality"]  
        table = self.work_book("Personal Data Distribution", workbook, titles)
        i = 1
        for section in personal_refuse.keys():
            table.write(i, 0, section, info_style)
            for assigner in personal_refuse[section].keys():
                table.write(i, 1, assigner, info_style)
                table.write(i, 2, personal_refuse[section][assigner]["resolved_defect"], info_style)
                table.write(i, 3, p0_personal[section][assigner]["total"], info_style)
                table.write(i, 4, p0_personal[section][assigner]["average"], info_style)
                table.write(i, 5, p1_personal[section][assigner]["total"], info_style)
                table.write(i, 6, p1_personal[section][assigner]["average"], info_style)
                table.write(i, 7, personal_process[section][assigner]["total"], info_style)
                table.write(i, 8, personal_process[section][assigner]["average"], info_style)
                table.write(i, 9, personal_refuse[section][assigner]["refused_defect"], info_style)
                table.write(i, 10, personal_refuse[section][assigner]["refused_rate"], info_style)
                table.write(i, 11, personal_refuse[section][assigner]["regression_defect"], info_style)
                table.write(i, 12, personal_refuse[section][assigner]["regression_rate"], info_style)
                table.write(i, 13, personal_quality[section][assigner]["Ergo_defect"], info_style)
                table.write(i, 14, personal_quality[section][assigner]["FR_Quality"], info_style)
                i += 1
        workbook.save(self.attach_path)

    def mail_sending(self, content, img_dir, attach_dir):
        mailcontent = str(content)
        send_mail.send_mail(conf.MAILUSERNAME, conf.MAILSENDMAIL,
                            '各team不达标项的详细数据', mailcontent,
                            conf.MAILTO, conf.MAILSENDER,
                            conf.MAILPASSWORD, conf.MAILCC, 
                            img_dir, attach_dir)

    def css_style(self):
        html = '''
            <head>
            <meta http-equiv="Content-Type" content="text/html; charset=gb2312">
            </head>
            <style type="text/css">
            table.gridtable {
                font-family: Times New Roman,verdana,arial,sans-serif;
                font-size:15px;
                border-width: 1px;
                border-color: #FFFFFF;
                border-collapse: collapse;
            }
            table.gridtable th {
                border-width: 3px;
                color:#EEE9E9;
                padding: 8px;
                border-style: solid;
                border-color: #EDEDED;
                background-color: #00AEAE;
            }
            table.gridtable td {
                font-family:arial;
                font-size:13px;
                text-align: center;
                border-width:3px;
                padding: 8px;
                border-style: solid;
                border-color: #EDEDED;
                background-color: #A6FFFF;
            }
            table tr td.col{
                color:red;
            }
            table.gridtable tr {
                background-color:#d4e3e5;
            }

            </style>
        '''
        return html

if __name__ == "__main__":
    TIMEBEGIN = "2016-09-01"
    TIMEEND = datetime.date.today().strftime("%Y-%m-%d")
    attach_path = "../attach/atta/Disqualified_Data.xls"
    image_path = "../img"
    test = SubstandardKPI(TIMEBEGIN, TIMEEND, attach_path, image_path)
    test.send_email()
    # print test.create_dict()
    # (b,bb) = test.refuse_defect() #refuse_defect feature_quality
    # for k in b.keys():
    #     print k, b[k]
    # f = test.pr_process_cycle("QC") #"P1 (Quick)" "QC"
    # for k in f[0].keys():
    #     print k,f[0][k]
    # g = test.original_data()
    # for i in g:
    #     if i["val_refuse"] == "YES":
    #         print i
    
