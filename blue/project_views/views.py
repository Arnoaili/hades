#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import render_template,request,redirect,url_for
import sys
#sys.path.append('..')
sys.path.append('../..')
from export_statistics import ExportStc
from store_redis import StoreRedis
import datetime
from settings import conf
from script.bugmatch.model import BugMatch
import json
import os
from . import project_views

@project_views.route('/',methods=['GET', 'POST'])
def home():
    return redirect(url_for('project_views.index',department='cd_swd1'))

@project_views.route('/<department>/',methods=['GET', 'POST'])
def index(department):
    date = ""
    if request.method == 'POST':
        date = request.form['date']
    else:
        get_list = request.args
        if get_list.has_key('date') == True:
            date = get_list.get('date')
    if date == "":
		date = (datetime.date.today() - datetime.timedelta(days=1)).strftime("%m/%d/%Y")

    project_name = []
    if department == 'cd_swd1':
        for project in conf.CD_SWD1_PROJECT:
            project_name.append(project)
        department_default = "CD_SWD1_All_projects"
    if department == 'cd_swd2':
        for project in conf.CD_SWD2_PROJECT:
            project_name.append(project)
        department_default = "CD_SWD2_All_projects"

    daily_statistics = ExportStc()
    projects = daily_statistics.get_project_total(project_name)
    total_sort = ('Total Num', 'Task Num', 'Defect Num')
    project_status = daily_statistics.get_project_status(project_name)
    if request.method == 'GET':
        return render_template('index.html', total_sort = total_sort,
                           projects = projects, project_name = project_name,
                           project_status = project_status, date = date,
                           default = project_name[0],department_default = department_default,
                           department = department,
                           cd_swd1_project = conf.CD_SWD1_PROJECT, 
                           cd_swd2_project = conf.CD_SWD2_PROJECT)
    else:
        return_list = {'code':200,'msg':'success','data':{}}
        return json.dumps(return_list)

# @project_views.route('/cd_swd2/',methods=['GET', 'POST'])
# def index_swd2():
#     date = ""
#     if request.method == 'POST':
#         date = request.form['date']
#     else:
#         get_list = request.args
#         if get_list.has_key('date') == True:
#             date = get_list.get('date')
#     if date == "":
#         date = (datetime.date.today() - datetime.timedelta(days=1)).strftime("%m/%d/%Y")

#     project_name = []
#     for project in conf.CD_SWD2_PROJECT:
#         project_name.append(project)

#     daily_statistics = ExportStc()
#     projects = daily_statistics.get_project_total(project_name)
#     total_sort = ('Total Num', 'Task Num', 'Defect Num')
#     project_status = daily_statistics.get_project_status(project_name)

#     if request.method == 'GET':
#         return render_template('index.html', total_sort = total_sort,
#                            projects = projects, project_name = project_name,
#                            project_status = project_status, date = date,
#                            default = project_name[0],department_default = "All_projects",
#                            cd_swd1_project = conf.CD_SWD1_PROJECT, 
#                            cd_swd2_project = conf.CD_SWD2_PROJECT)
#     else:
#         return_list = {'code':200,'msg':'success','data':{}}
#         return json.dumps(return_list)

@project_views.route('/flot/<department>/<value>',methods = ['GET', 'POST'])
def flot(department,value):

    date = ""
    if request.method == 'POST':
        date = request.form['date']
    else:
        get_list = request.args
        if get_list.has_key('date') == True:
            date = get_list.get('date')
    if date == "":
        date = (datetime.date.today() - datetime.timedelta(days=1)).strftime("%m/%d/%Y")
    date_list = date.split('/')
    year = date_list[2]
    day = date_list[1]
    month = date_list[0]
    display_date = year+'-'+month+'-'+day

    project_name = []
    if value in conf.CD_SWD1_PROJECT:
        for project in conf.CD_SWD1_PROJECT:
            tmp = ''
            if value == project:
                tmp = 'active'
            project_tmp = {'cls':tmp,'item':project}
            project_name.append(project_tmp)
    if value in conf.CD_SWD2_PROJECT:
        for project in conf.CD_SWD2_PROJECT:
            tmp = ''
            if value == project:
                tmp = 'active'
            project_tmp = {'cls':tmp,'item':project}
            project_name.append(project_tmp)
    print project_name

    daily_statistics = ExportStc()
    daily_redis = StoreRedis()
    teams_sort = ()
    department_default = ""
    if value in conf.CD_SWD1_PROJECT:
        teams_sort = ('CD_SWD1_APP', 'CD_SWD1_SYS', 'CD_SWD1_MID', 'CD_SWD1_TELECOM', 
                'CD_SWD1_SPM', 'CD_SWD1_INT', 'OTHERS')
        department_default = "CD_SWD1_All_projects"
    if value in conf.CD_SWD2_PROJECT:
        teams_sort = ('CD_SWD2_APP', 'CD_SWD2_SYS', 'CD_SWD2_FRM', 'CD_SWD2_TELECOM', 
                'CD_SWD2_SPM', 'CD_SWD2_INT', 'OTHERS')
        department_default = "CD_SWD2_All_projects"

    if daily_statistics.date_record_yes_no(display_date, value):
        print 'enter if record_yes_no'
        if daily_redis.get_redis(display_date, value):
            print 'enter if'
            daily = daily_redis.get_redis(display_date, value)['project_static']
            module = daily_redis.get_redis(display_date, value)['function_static']
            teams_total = daily_redis.get_redis(display_date, value)['big_team_static']
            teams = daily_redis.get_redis(display_date, value)['team_static']
            team_detail = daily_redis.get_redis(display_date, value)['person_static']
            daily_data = daily_redis.get_redis(display_date, value)['daily_static']

        else:
            print 'enter else'
            daily = daily_statistics.get_project_static(value)
            module = daily_statistics.ten_fun_module(display_date, value)
            teams_total = daily_statistics.get_big_team_static(display_date, value)
            teams = daily_statistics.get_team_static(display_date, value)
            team_detail = daily_statistics.get_person_static(display_date, value)
            daily_data = daily_statistics.get_daily_bugs(value)
           
        if request.method == 'GET':
            return render_template('flot.html', teams_sort = teams_sort, daily_data=daily_data,
                               daily = daily, module = module, teams = teams, teams_total=teams_total,
                               project_name = project_name, date = date, team_detail = team_detail,
                               default = project_name[0]['item'],department_default = department_default,
                               department = department,
                               cd_swd1_project = conf.CD_SWD1_PROJECT,
                               cd_swd2_project = conf.CD_SWD2_PROJECT)
        else:
            return_list = {'code':200,'msg':'success','data':{}}
            return json.dumps(return_list)
    else:
        if request.method == 'GET':
            correct_date = daily_statistics.get_recent_date(display_date)
            return render_template('error.html', date=date, coodate = correct_date, project_name = project_name,
                    default = project_name[0]['item'],
                    department_default = department_default,
                    department = department,
                    cd_swd1_project = conf.CD_SWD1_PROJECT,
                    cd_swd2_project = conf.CD_SWD2_PROJECT)
        else:
            return_list = {'code':100,'msg':'No data of this date!','data':{}}
            return json.dumps(return_list)

@project_views.route('/table/<department>/<value>',methods=['GET', 'POST'])
def table(department,value):

    date = ""
    if request.method == 'POST':
        date = request.form['date']
    else:
        get_list = request.args
        if get_list.has_key('date') == True:
            date = get_list.get('date')

    if date == "":
		date = (datetime.date.today() - datetime.timedelta(days=1)).strftime("%m/%d/%Y")

    project_name = []
    department_default = ""
    if value in conf.CD_SWD1_PROJECT:
        department_default = "CD_SWD1_All_projects"
        for project in conf.CD_SWD1_PROJECT:
            tmp = ''
            if value == project:
                tmp = 'active'
            project_tmp = {'cls':tmp,'item':project}
            project_name.append(project_tmp)
    if value in conf.CD_SWD2_PROJECT:
        department_default = "CD_SWD2_All_projects"
        for project in conf.CD_SWD2_PROJECT:
            tmp = ''
            if value == project:
                tmp = 'active'
            project_tmp = {'cls':tmp,'item':project}
            project_name.append(project_tmp)
    daily_statistics = ExportStc()
    result = daily_statistics.get_bug_list(value)

    if request.method == 'GET':
        return render_template('tables.html', result = result,
                            project_name = project_name, date = date,
                            default = project_name[0]['item'],department_default = department_default,
                            department = department,
                            cd_swd1_project = conf.CD_SWD1_PROJECT,
                            cd_swd2_project = conf.CD_SWD2_PROJECT)
    else:
        return_list = {'code':200,'msg':'success','data':{}}
        return json.dumps(return_list)

@project_views.route('/tableforspm/<value>',methods=['GET', 'POST'])
def tableforspm(value):

    date = ""
    level = ""
    bug_id = ""
    assigner = ""
    comment = ""
    if request.method == 'POST':
        level = request.values.get('level', 0)
        bug_id = request.values.get('bug_id', 0)
        assigner = request.values.get('assigner',None)
        comment = request.values.get('comment',None)

    if date == "":
        date = (datetime.date.today() - datetime.timedelta(days=1)).strftime("%m/%d/%Y")

    project_name = []
    for project in conf.PROJECT_DICT.keys():
        tmp = ''
        if value == project:
            tmp = 'active'
        project_tmp = {'cls':tmp,'item':project}
        project_name.append(project_tmp)
    daily_statistics = ExportStc()
    result = daily_statistics.get_bug_list(value)

    if level and bug_id:
        daily_statistics.insert_level_into_db(level, bug_id)
    if bug_id and (assigner or comment):
        daily_statistics.deliver_comments_to_alm(bug_id, comment, assigner)

    # if request.method == 'POST' and level!=0 and bug_id!=0:
    #     return_list = {'code':200,'msg':'success','data':{}}
    #     return json.dumps(return_list)

    return render_template('tableforspm.html', result = result,
                            project_name = project_name, date = date,
                            default = project_name[0]['item'],department_default = "All_projects")

@project_views.route('/<department>/window',methods=['GET', 'POST'])
def window(department):
    bugid = request.form['bugid']
    print "***********", bugid
    if bugid == "bug id":
        return "<font color='#FF0000'><strong>Please Input A Bug Id !</strong></font>"
    work_dir = os.getcwd() + '/script/bugmatch'
    default_fname = work_dir + '/all_bugs_RC.txt'
    match_fname = work_dir + '/new_add_bugs_RC.txt'
    model = "tfidf"
    a = datetime.datetime.now()
    match = BugMatch(work_dir, model, default_fname, match_fname)
    result = match.web_result_display(bugid)
    if result == "Error":
        return "<font color='#FF0000'><strong>Please Input A Right Bug Id !</strong></font>"
    b = datetime.datetime.now()
    time = str((b-a).seconds)
    print "Time cast: ", time + "s"
    result += "\nPS: it takes about %s seconds to get the result!" % (time)
    return result

