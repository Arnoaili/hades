#!/usr/bin/env python
# -*- coding: utf-8 -*-
from imports import Bugdb
import time
import datetime
import sys
import send_mail
sys.path.append("..")
from settings import conf
reload(sys)
import xlwt
import style
import re

class DepartmentStatis():
    def __init__(self):
        self.imp = Bugdb('localhost', conf.MYSQLUSERNAME, 
                            conf.MYSQLPASSWORD, 'hades')
        #self.open_list = ("New", "Assigned", "Opened", "Resolved")
    def get_base_info(self):
        bug_reg_ref = {}
        self.imp.cur.execute('select bug_id,regression,regression_date,val_refuse,refused_date from base')
        bug_info = self.imp.cur.fetchall()
        for bug in bug_info:
            if bug[0] not in bug_reg_ref.keys():
                bug_reg_ref[bug[0]] = {}
            regression_date=''
            refused_date=''
            if bug[2] is not None:
                regression_date = str(bug[2])
            if bug[4] is not None:
                refused_date = str(bug[4])
            bug_reg_ref[bug[0]] = {'regression':str(bug[1]),'regression_date':regression_date,
                                    'val_refuse':str(bug[3]),'refused_date':refused_date}
        #print bug_reg_ref
        return bug_reg_ref
    
    def get_userid_section(self):
        '''this method : get userid_section={user:section}'''
        userid_section = {}
        self.imp.cur.execute('select id,section from bugusers \
            where department like "WMD-PIC CD-SWD1%" or department like "WMD-PIC CD-SWD2%"')
        userid_info = self.imp.cur.fetchall()
        for userid in userid_info:
            userid_section[str(userid[0])] = str(userid[1])
        return userid_section

    def get_ago_saturday_open_total(self, day_count=7):
        weeks_ago_info = {}
        userid_section = self.get_userid_section()
        for userid in userid_section.keys():
            if userid not in weeks_ago_info.keys():
                weeks_ago_info[userid] = {}
                for project_name in conf.PROJECT_DICT.keys():
                    weeks_ago_info[userid][project_name] = {'saturday_open_total':0}

        weeks_ago_time = datetime.date.today() - datetime.timedelta(days=day_count)
        weeks_ago = weeks_ago_time.strftime("%Y")+'-'+weeks_ago_time.strftime("%W")

        self.imp.cur.execute('select user_id,project_name,saturday_open_total \
            from dep_weekly_person where weeks="%s"' % weeks_ago)
        ago_saturday_open_total = self.imp.cur.fetchall()
        for item in ago_saturday_open_total:
            weeks_ago_info[str(item[0])][str(item[1])]['saturday_open_total'] = int(item[2])
        
        return weeks_ago_info

    def get_base_static(self, day_count=7):
        dep_weekly_person = {}
        week_ago = (datetime.date.today() - datetime.timedelta(days=day_count)).strftime("%Y-%m-%d")
        userid_section = self.get_userid_section()
        for userid in userid_section.keys():
            if userid not in dep_weekly_person.keys():
                dep_weekly_person[userid] = {}
                for project_name in conf.PROJECT_DICT.keys():
                    dep_weekly_person[userid][project_name] = {'open_total':0, 'saturday_open_total':0, 
                                                                'open':0, 'fix':0, 'ref_reg':0}
        ##saturday_open_total static
        self.imp.cur.execute('select assigner,project_name from base \
            where bug_status in ("New", "Assigned", "Opened", "Resolved")')
        saturday_open_total = self.imp.cur.fetchall()
        for bug in saturday_open_total:
            if userid_section.has_key(str(bug[0])): #swd1 person
                if conf.PROJECT_DICT.has_key(bug[1]): #ongoing project
                    dep_weekly_person[str(bug[0])][bug[1]]['saturday_open_total'] += 1
        
        ##open static
        self.imp.cur.execute('select assigner,project_name from base where assigned_date>"%s"' % week_ago)
        open_static = self.imp.cur.fetchall()
        for bug in open_static:
            if userid_section.has_key(str(bug[0])): #swd1 person
                if conf.PROJECT_DICT.has_key(bug[1]):#ongoing project
                    dep_weekly_person[str(bug[0])][bug[1]]['open'] += 1
        
        ##open_total static
        ago_saturday_open_total = self.get_ago_saturday_open_total()
        for user_id in ago_saturday_open_total.keys():
            for project_name in ago_saturday_open_total[user_id].keys():
                #print ago_saturday_open_total[user_id][project_name]
                dep_weekly_person[user_id][project_name]['open_total'] = dep_weekly_person[user_id][project_name]['open']+ago_saturday_open_total[user_id][project_name]['saturday_open_total']

        #fix static
        self.imp.cur.execute('select resolver,project_name \
            from base where bug_status in ("Delivered", "Verified", "Verified_SW", "Closed") \
            and verified_sw_date>"%s"' % week_ago) #Normal Process
        fix1 = self.imp.cur.fetchall()
        for bug in fix1:
            if userid_section.has_key(str(bug[0])): #swd1 person
                if conf.PROJECT_DICT.has_key(bug[1]):#ongoing project
                    dep_weekly_person[str(bug[0])][bug[1]]['fix'] += 1
        self.imp.cur.execute('select long_text_read_only,project_name \
            from base where bug_status in ("Delivered", "Verified", "Verified_SW", "Closed") \
            and verified_sw_date="0000-00-00 00:00:00" and closed_date>"%s";' % week_ago) #abnormal process
        fix2 = self.imp.cur.fetchall()
        for bug in fix2:
            if userid_section.has_key(str(bug[0])): #swd1 person
                if conf.PROJECT_DICT.has_key(bug[1]):#ongoing project
                    dep_weekly_person[str(bug[0])][bug[1]]['fix'] += 1
        
        #ref_reg static
        self.imp.cur.execute('select assigner,project_name from base \
            where regression_date>"%s" or refused_date="%s"' % (week_ago,week_ago))
        ref_reg = self.imp.cur.fetchall()
        for bug in ref_reg:
            if userid_section.has_key(str(bug[0])): #swd1 person
                if conf.PROJECT_DICT.has_key(bug[1]):#ongoing project
                    dep_weekly_person[str(bug[0])][bug[1]]['ref_reg'] += 1
        #print dep_weekly_person
        return dep_weekly_person

    def insert_dep_weekly_person(self, base_static):
        weeks = time.strftime("%Y")+'-'+time.strftime("%W")
        date = time.strftime("%Y-%m-%d")
        userid_section = self.get_userid_section()
        for userid in base_static.keys():
           for project in base_static[userid].keys():
                self.imp.cur.execute('insert into dep_weekly_person(user_id,section,open_total,saturday_open_total,\
                open,fix,ref_reg,project_name,date,weeks) values("%s","%s",%s,%s,%s,%s,%s,"%s","%s","%s")' %(
                userid, userid_section[userid], base_static[userid][project]['open_total'], 
                base_static[userid][project]['saturday_open_total'], base_static[userid][project]['open'], 
                base_static[userid][project]['fix'], base_static[userid][project]['ref_reg'], 
                project, date, weeks))
                self.imp.conn.commit()


    def get_deadline_info(self):
        base_deadline = {}
        '''
        print "select base.bug_id,bugusers.email,base.summary,base.priority,\
            base.deadline,base.created_date from base,bugusers where\
            bug_status in ('New', 'Assigned','Opened', 'Resolved') and base.assigner=bugusers.id\
            and base.priority in ('P0 (Urgent)','P1 (Quick)') and project_name in (",",".join("".join(['\'',project,'\'']) for project in project_list),")"
        '''
        self.imp.cur.execute("select base.bug_id,bugusers.email,base.summary,base.priority,\
            base.deadline,base.created_date,base.project_name,base.bug_status,bugusers.section from base,bugusers where \
            base.type='Defect' and bug_status in ('New', 'Assigned','Opened', 'Resolved') and base.assigner=bugusers.id \
            and (base.priority='P0 (Urgent)' or (base.priority='P1 (Quick)' and ipr_value>300)) and bugusers.department like'WMD-PIC CD-SWD1%'")

        base_info = self.imp.cur.fetchall()
        for bug in base_info:
            if bug[0] not in base_deadline.keys():
                base_deadline[bug[0]] = {'assginer':'', 'summary':'', 'priority':'', 'deadline':'', 
                            'created_date':'', 'project_name':'', 'bug_status':'', 'team':''}
            base_deadline[bug[0]]['bug_id'] = bug[0]
            base_deadline[bug[0]]['assginer'] = str(bug[1])
            base_deadline[bug[0]]['summary'] = str(bug[2])
            base_deadline[bug[0]]['priority'] = str(bug[3])
            if re.search('\[VF\d+\]', str(bug[2])):
                base_deadline[bug[0]]['priority'] = "QC"
            base_deadline[bug[0]]['deadline'] = str(bug[4])
            base_deadline[bug[0]]['created_date'] = str(bug[5])
            base_deadline[bug[0]]['project_name'] = str(bug[6])
            base_deadline[bug[0]]['bug_status'] = str(bug[7])
            base_deadline[bug[0]]['team'] = str(bug[8])

        #print base_deadline
        return base_deadline

    def deal_deadline(self):
        base_deadline = self.get_deadline_info()
        modify_deadline = {}
        P0 = 7
        P1 = 14
        for bugid in base_deadline.keys():
            if base_deadline[bugid]['project_name'] in conf.PROJECT_DICT.keys(): #current project
                if base_deadline[bugid]['priority'] in ['P0 (Urgent)','P1 (Quick)']: #static P0 and P1
                    if bugid not in modify_deadline.keys():
                        modify_deadline[bugid] = base_deadline[bugid]
                    if base_deadline[bugid]['deadline'] == 'None':
                        if base_deadline[bugid]['priority'] == 'P0 (Urgent)':
                            modify_deadline[bugid]['deadline'] = (datetime.datetime.strptime(base_deadline[bugid]['created_date'],
                                '%Y-%m-%d %H:%M:%S') + datetime.timedelta(days=P0)).strftime('%Y-%m-%d %H:%M:%S')
                        if base_deadline[bugid]['priority'] == 'P1 (Quick)':
                            modify_deadline[bugid]['deadline'] = (datetime.datetime.strptime(base_deadline[bugid]['created_date'],
                                '%Y-%m-%d %H:%M:%S') + datetime.timedelta(days=P1)).strftime('%Y-%m-%d %H:%M:%S')
        #print modify_deadline
        return modify_deadline

    def time_compare(self):
        modify_deadline = self.deal_deadline()
        current_time = datetime.datetime.today()
        out_of_deadline = {}
        for project in conf.PROJECT_DICT.keys():
            if project not in out_of_deadline.keys():
                out_of_deadline[project] = []
        for bugid in modify_deadline.keys():
            if datetime.datetime.strptime(modify_deadline[bugid]['deadline'],'%Y-%m-%d %H:%M:%S') < current_time:
                out_of_deadline[modify_deadline[bugid]['project_name']].append(modify_deadline[bugid])
        return out_of_deadline

    def today_time_compare(self):
        modify_deadline = self.deal_deadline()
        today_date = datetime.datetime.today().strftime('%Y-%m-%d')
        out_of_today = {}
        for project in conf.PROJECT_DICT.keys():
            if project not in out_of_today.keys():
                out_of_today[project] = []
        for bugid in modify_deadline.keys():
            if (datetime.datetime.strptime(modify_deadline[bugid]['deadline'],
                '%Y-%m-%d %H:%M:%S')).strftime('%Y-%m-%d') == today_date:
                out_of_today[modify_deadline[bugid]['project_name']].append(modify_deadline[bugid])
        return out_of_today

    def mail_settings(self, content, img_dir, attach_dir, to_mail_list):
        """Send mail if Connect Delay"""
        title = 'SWD1 Delay PR List of ' +datetime.date.today().strftime("%Y-%m-%d")
        MAILTOLIST = to_mail_list #conf.MAILTOLIST
        mailcontent = str(content)
        send_mail.send_mail(conf.MAILUSERNAME, conf.MAILSENDMAIL,
                            title, mailcontent,
                            MAILTOLIST, conf.MAILSENDER,
                            conf.MAILPASSWORD, conf.MAILCCLIST, 
                            img_dir, attach_dir)

    def send_email(self):
        out_of_deadline = self.time_compare()
        title_style = style.get_body_title_style(font_color=0x1, bg_color=0x30)
        workbook = xlwt.Workbook(encoding='utf-8')
        title = ['bug_id','bug_status','summary','assginer','team','priority','deadline']
        for project_name in out_of_deadline.keys():
            table = workbook.add_sheet(project_name, cell_overwrite_ok=True)
            i = 0
            j = 1
            table.col(0).width = 256*10
            table.col(2).width = 256*90
            table.col(3).width = 256*20
            table.col(4).width = 256*20
            table.col(5).width = 256*20
            table.col(6).width = 256*20
            for item in title:
                table.write(0, i, item, title_style)
                i += 1
            all_delay_bugs=sorted(out_of_deadline[project_name],key = lambda x:x['team'],reverse=False)
            for item in all_delay_bugs:
                table.write(j, 0, item['bug_id'])
                table.write(j, 1, item['bug_status'])
                table.write(j, 2, item['summary'])
                table.write(j, 3, item['assginer'])
                table.write(j, 4, item['team'])
                table.write(j, 5, item['priority'])
                table.write(j, 6, item['deadline'])
                j += 1
        path = '../attach/pr_atta/All_Delayed_bugs_of_each_project_before_' + datetime.date.today().strftime("%Y-%m-%d") + '.xls' 
        workbook.save(path)

        to_mail_list = []
        out_of_today = self.today_time_compare()
        html = self.mail_head_content()
        for project in out_of_today.keys():
            if out_of_today[project] != []:
                html += '<p><b>%s</b>' % project
                html += '<table border="1" cellpadding="0" cellspacing="0">'
                html += '<tr><td>bug_id</td>'
                html += '<td>bug_status</td>'
                html += '<td>assginer</td>'
                html += '<td>team</td>'
                html += '<td>priority</td>'
                html += '<td>summary</td>'
                html += '<td>deadline</td>'
                html += '</tr>'
                delay_bugs=sorted(out_of_today[project],key = lambda x:x['team'],reverse=False)
                for item in delay_bugs:
                    if item['assginer'] not in to_mail_list:
                        to_mail_list.append(item['assginer'])
                    html += '<tr><td width="100"><a href="https://alm.tclcom.com:7003/im/issues?selection=%s">%s</a></td>' % (item['bug_id'],item['bug_id'])
                    html += '<td width="100">%s</td>' % item['bug_status']
                    html += '<td width="150">%s</td>' % item['assginer']
                    html += '<td width="150">%s</td>' % item['team']
                    html += '<td width="150">%s</td>' % item['priority']
                    html += '<td width="500">%s</td>' % item['summary']
                    html += '<td width="200">%s</td></tr>' % item['deadline']
                html += '</table></p>'
        html += '<p>You can search the detail information from the bug web link below: </p>'
        html += '<a href="http://172.26.35.69">http://172.26.35.69</a>'
        html += '<p>PS: No table about bug above means there is not any bug delayed today!</p>'
        html += self.mail_bottom_content()
        img_dir = '../img'
        attach_dir = '../attach/pr_atta'
        self.mail_settings(html, img_dir, attach_dir, to_mail_list)

    def mail_head_content(self):
        html = '''<html xmlns="http://www.w3.org/1999/xhtml">
        <head>
        <meta http-equiv="Content-Type" content="text/html;charset=utf-8"/>
        <style type="text/css">
        body {font-family:arial; font-size:10pt;}
        td {font-family:arial; font-size:10pt;}
        </style>
        <title>bugs info</title>
        </head>
        <body>
        <p>Dear All,</p>
        <p>Here is the bugs info which is delay today, if you find the data is not correct, please tell me, thanks!</p>
        <p>In addition, you can get the all delayed bugs of each project from the attachment at the bottom of the email! </p>
        '''
        return html


    def mail_bottom_content(self):
        html = '<br/><img src="cid:image001.gif">'
        html += '<p><font color="gray">'
        html += 'Best Regards,<br />'
        html += 'INT Server' + '<br />'
        html += 'TEL: ' + '028-6988 2660' + '<br />'
        html += 'MAIL: ' + 'cd.int@tcl.com' + '<br />'
        html += 'ADDR: 9 Floor, C11, Tianfu Software Park,number 81 Tian Hua ' + \
                '2nd Road High Tech District, 610041, Chengdu, China'
        html += '</font></p>'
        html += '</body>'
        html += '</html>'
        return html


#test = DepartmentStatis()
#base_static = test.get_base_static()
#test.insert_dep_weekly_person(base_static)
#print test.get_ago_saturday_open_total()
#base_static = test.get_base_static()
#test.insert_dep_weekly_person(base_static)
#test.time_compare()
#print test.send_email()


