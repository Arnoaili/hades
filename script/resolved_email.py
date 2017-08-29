#!/usr/bin/env python
# -*- coding: utf-8 -*-
from imports import Bugdb
import datetime
import send_mail
import sys
sys.path.append("..")
from settings import conf
import os
import re
import redis


class ResolvedEmail():
    def __init__(self):
        self.imp = Bugdb('localhost', conf.MYSQLUSERNAME, 
                            conf.MYSQLPASSWORD, 'hades')
	self.red = redis.Redis(host='localhost', port=6379, db=1)
        self.day = datetime.date.today().strftime("%Y-%m-%d")
        self.yesterday = (datetime.date.today() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")		

    def get_base_infos(self):
        self.imp.cur.execute("select base.bug_id,bugusers.email,base.priority,base.bug_status,\
            base.project_name,bugusers.section,base.summary from base,bugusers where \
            base.type='Defect' and base.bug_status ='Resolved' and base.assigner=bugusers.id \
            and (base.priority='P0 (Urgent)' or (base.priority='P1 (Quick)' and ipr_value>300)) \
            and bugusers.department like 'WMD-PIC CD-SWD1%'")
        base_infos = self.imp.cur.fetchall()        
        item = ["bug_id", "assigner", "priority", "bug_status", "project_name",
                 "section", "summary"]
        infos_list = []
        for info in base_infos:
            one_info = {}
            for i in xrange(len(item)):
                one_info[item[i]] = info[i]
            infos_list.append(one_info)
        return infos_list

    def write_yesterday_bugid(self):
        if self.red.exists(self.yesterday):
            self.red.delete(self.yesterday)
        all_infos = self.get_base_infos()
        for info in all_infos:
            self.red.rpush(self.day, info["bug_id"]) 

    def mail_settings(self, content, img_dir, to_mail_list):
        """Send mail if Connect Delay"""
        title = 'SWD1 Resolved PR List of ' +datetime.date.today().strftime("%Y-%m-%d")
        if to_mail_list:
            MAILTOLIST = to_mail_list
            MAILCCLIST = conf.MAILCCLIST
        else:
            MAILTOLIST = conf.MAILTOLIST
            MAILCCLIST = conf.MAILCC
        # MAILTOLIST = conf.MAILTOLIST    
        mailcontent = str(content)
        send_mail.send_mail(conf.MAILUSERNAME, conf.MAILSENDMAIL,
                            title, mailcontent,
                            MAILTOLIST, conf.MAILSENDER,
                            conf.MAILPASSWORD, MAILCCLIST, 
                            img_dir)

    def send_resolved_email(self):
        all_infos = self.get_base_infos()
        to_mail_list = []
        resolved_bugs = []
        bugid_yesterday = self.red.lrange(self.yesterday, 0, -1)
        for info in all_infos:
            if str(info["bug_id"]) in bugid_yesterday:
                resolved_bugs.append(info)
        resolved_bugs=sorted(resolved_bugs,key = lambda x:x['section'],reverse=False)
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
        '''
        if resolved_bugs:
            html += """
            <p>Dear All,</p>
            <p>Here is the bug information at the state of resolved more than one day, which you should modify the state.<br/></p> 
            <p>If you find the data is not correct, please tell me, thanks!</p> 
            """
            html += '<table border="1" cellpadding="0" cellspacing="0">'
            html += '<tr><td>bug_id</td>'
            html += '<td>assigner</td>'
            html += '<td>priority</td>'
            html += '<td>bug_status</td>'
            html += '<td>project_name</td>'
            html += '<td>section</td>'
            html += '<td>summary</td>'
            html += '</tr>'

            for bug in resolved_bugs:
                if bug["assigner"] not in to_mail_list:
                    to_mail_list.append(bug["assigner"])
                html += '<tr><td width="100"><a href="https://alm.tclcom.com:7003/im/issues?selection=%s">%s</a></td>' % (bug['bug_id'],bug['bug_id'])
                html += '<td width="150">%s</td>' % bug["assigner"]
                html += '<td width="100">%s</td>' % bug["priority"]
                html += '<td width="100">%s</td>' % bug["bug_status"]
                html += '<td width="100">%s</td>' % bug["project_name"]
                html += '<td width="100">%s</td>' % bug["section"]
                html += '<td width="500">%s</td>' % bug["summary"]
                html += '</tr>'
            html += '</table>'
        else:
            html += """
            <p>Dear,</p>
            <p>Today, there is not any bug at the state of resolved more than one day!</p>
            """
        html += '<br/><img src="cid:image001.gif">'
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
        img_dir = '../img'
        self.mail_settings(html, img_dir, to_mail_list)


if __name__ == "__main__":
    test = ResolvedEmail()
    test.send_resolved_email()
    test.write_yesterday_bugid()
