#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Configure file"""

# MySQL conf
MYSQLUSERNAME = "root"
MYSQLPASSWORD = "Aa123456"


# connect ALM conf
ALMUSERNAME = "cd.int"
ALMPASSWORD = "Cd123456"

# query bug info from ALM
ALMQUERY = {'id':'bug_id', 'state':'bug_status', 
            'modified_date': 'changeddate',
            'deadline':'deadline', 'summary': 'summary', 
            'ipr_value': 'ipr_value',
            'regression':'regression', 'created_date':'created_date', 
            'closed_date':'closed_date','val_refuse':'val_refuse', 
            'priority':'priority', 'function':'function_id',
            'branch':'branch', 'type':'type','resolution':'resolution', 
            'comment_from_cea':'comment_from_cea',
            'reporter':'reporter_email', 'assigned_user':'assigner',
            'sw_release':'version', 'homo':'homologation',
            'verified_sw_date':'verified_sw_date',
            'refused_date':'refused_date',
            'regression_date':'regression_date',
            'new_date':'new_date', 'assigned_date':'assigned_date',
            'resolver':'resolver','long_text_read_only':'long_text_read_only',
            'isCR':'isCR'
            }


# sent mail conf
MAILUSERNAME = "cd.int"
MAILPASSWORD = "Cd123456"
MAILSENDER = "BugWeb"
MAILSUBJECT = "Error from BugWeb"
MAILCONTENT = "<strong>Please check the log from BugWeb</strong>"
MAILTOLIST = ["li.ai@tcl.com"]
MAILSENDMAIL = "cd.int@tcl.com"
MAILCCLIST = ["li.ai@tcl.com","cd.swd1.spm@tcl.com","cd.swd1.tl@tcl.com","yuanzu.tang@tcl.com"]
MAILTO = ["yun.ling@tcl.com"]
MAILCC = ["li.ai@tcl.com","mei.yang@tcl.com"]

#project_list
PROJECT_DICT = {'SAM2':'/TCT/MTK MT6570/BUZZ6 3G VF',
                'Gandalf':'/TCT/QCT MSM8976/Idol4 S VF',
                'SAM':'/TCT/MTK MT6580M/PIXI4-4 3G VF', 
                'Frodo':'/TCT/MTK MT6735M/Pixi4-5 4G VF',
                'Aragorn':'/TCT/MTK MT6755M/SHINE PLUS VF',
                'Smeagol' : '/TCT/MTK MT6572M/PIXI3-3.5 3G VF',
                'Catwoman': '/TCT/MTK MT6737/MICKEY6 VF',
                'Simba6_na':'/TCT/QCT MSM8953/SIMBA6 NA',
                'Mickey6_tf_umts':'/TCT/QCT MSM8909/MICKEY6 TF UMTS',
                'Mickey6_cc':'/TCT/QCT MSM8909/MICKEY6 CC',
                'Buzz6t_4g_gophone':'/TCT/QCT MSM8909/BUZZ6T 4G GOPHONE',
                'Buzz6t_4g_tf_umts':'/TCT/QCT MSM8909/BUZZ6T 4G TF UMTS',
                'Mickey6_tf_umts_5046g':'/TCT/QCT MSM8909/MICKEY6 TF UMTS(5046G)',
                'Simba6_cricket':'/TCT/MTK MT6757C/SIMBA6 CRICKET',
                'Buzz6t_4g_telus':'/TCT/QCT MSM8909/BUZZ6T 4G TELUS'}

NEW_PROJECT_DICT = {
                        'Catwoman': '/TCT/MTK MT6737/MICKEY6 VF',
                        'Simba6_na': '/TCT/QCT MSM8953/SIMBA6 NA'}
                        
CD_SWD1_PROJECT = ['SAM2','Catwoman','Simba6_na','Gandalf','SAM','Frodo','Aragorn','Smeagol']

CD_SWD2_PROJECT = ['Mickey6_cc','Mickey6_tf_umts','Mickey6_tf_umts_5046g',
                    'Buzz6t_4g_gophone','Buzz6t_4g_tf_umts','Buzz6t_4g_telus',
                    'Simba6_cricket']

TEAM = {
                "CD_app":["WMD-PIC CD-SWD1-APP Team", "WMD-PIC CD-SWD1-APP Team-APP1", 
                        "WMD-PIC CD-SWD1-APP Team-APP2", "WMD-PIC CD-SWD1-APP Team-APP3",
                        "WMD-PIC CD-SWD1-APP-OS-TSCD","WMD-PIC CD-SWD1-APP-OS-SURCD"],
                "CD_mid":["WMD-PIC CD-SWD1-MDW Team", "WMD-PIC CD-SWD1-MDW Team-CONNECT", 
                        "WMD-PIC CD-SWD1-MDW Team-MM", "WMD-PIC CD-SWD1-MDW Team-FRM",
                        "WMD-PIC CD-SWD1-MDWR-OS-TSCD","WMD-PIC CD-SWD1-MDWR-OS-SURCD"],
                "CD_sys":["WMD-PIC CD-SWD1-SYS Team", "WMD-PIC CD-SWD1-SYS Team-SYS", 
                        "WMD-PIC CD-SWD1-SYS Team-DRIVER1", "WMD-PIC CD-SWD1-SYS Team-DRIVER2",
                        "WMD-PIC CD-SWD1-System-OS-TSCD","WMD-PIC CD-SWD1-System-OS-SURCD"],
                "CD_INT":["WMD-PIC CD-SWD1-INT Team","WMD-PIC CD-SWD1-INT-OS-TS"],
                "CD_Telecom":["WMD-PIC CD-SWD1-TEL Team","WMD-PIC CD-SWD1-Telecom-OS-SURCD",
                        "WMD-PIC CD-SWD1-Telecom-OS-HOPERUN","WMD-PIC CD-SWD1-Telecom-OS-TSCD"],
                "CD_SPM":["WMD-PIC CD-SWD1-SPM Team"]
 }
