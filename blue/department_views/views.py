import os
import time
import datetime
import sys
sys.path.append('../..')
from settings import conf
from flask import render_template, request
from . import department_views
from project_investment import ExportProjectInvestment
from script import disqualified_data
import json

@department_views.route('/investment/<department>/<value>',methods=['GET', 'POST'])
def invest(department,value):

    if request.method == 'POST':
        post_date = str(request.form['date']).split("/")
    else:
        get_list = request.args
        post_date = {}
        if get_list.has_key('date') == True:
            date_get = get_list.get('date')
            post_date = str(date_get).split("/")
    if post_date:
        datetime_date = datetime.datetime(int(post_date[2]),int(post_date[0]),int(post_date[1]))
        date = datetime_date.strftime("%W") + '/' + datetime_date.strftime("%Y")
        week = datetime_date.strftime("%Y") + '-' + datetime_date.strftime("%W")
    else:
        day_ago = datetime.date.today() - datetime.timedelta(days=7)
        date = day_ago.strftime("%W") + '/' + day_ago.strftime("%Y")
        week = day_ago.strftime("%Y") + '-' + day_ago.strftime("%W")

    project_name = []
    if value in conf.CD_SWD1_PROJECT or value == "CD_SWD1_All_projects":
        project_name.append({'cls':'','item':'CD_SWD1_All_projects'})
        for project in conf.CD_SWD1_PROJECT:
            project_tmp = {'cls':'','item':project}
            project_name.append(project_tmp)
    if value in conf.CD_SWD2_PROJECT or value == "CD_SWD2_All_projects":
        project_name.append({'cls':'','item':'CD_SWD2_All_projects'})
        for project in conf.CD_SWD2_PROJECT:
            project_tmp = {'cls':'','item':project}
            project_name.append(project_tmp)
    #print '*'*100
    #print project_name[0]['item']
    #print '*'*100
    teams_sort = ()
    department_default = ""
    if value in conf.CD_SWD1_PROJECT or value == "CD_SWD1_All_projects":
        teams_sort = ('CD_SWD1','CD_SWD1_APP', 'CD_SWD1_SYS', 'CD_SWD1_MID', 'CD_SWD1_TELECOM', 'CD_SWD1_SPM', 'CD_SWD1_INT')
        department_default = "CD_SWD1_All_projects"
    if value in conf.CD_SWD2_PROJECT or value == "CD_SWD2_All_projects":
        teams_sort = ('CD_SWD2','CD_SWD2_APP', 'CD_SWD2_SYS', 'CD_SWD2_FRM', 'CD_SWD2_TELECOM', 'CD_SWD2_SPM', 'CD_SWD2_INT')
        department_default = "CD_SWD2_All_projects"
    ExportProject = ExportProjectInvestment()
    #print '*'*100
    #print week
    if ExportProject.week_record_yes_no(week, value):
        (personal_investment,list_rate, section_investment, projects_list) = ExportProject.get_project_investment(week, value)
        (team_investment,week_list) = ExportProject.get_team_investment(week, value)

        if request.method == 'GET':
            return render_template('investment.html', teams_sort=teams_sort, date=date,
                personal_investment=personal_investment, list_rate=list_rate,
                section_investment=section_investment, team_investment=team_investment,
                project_name=project_name, projects_list=projects_list, week_list=week_list,
                default=project_name[0]['item'],
                department_default = department_default,
                department = department,
                cd_swd1_project = conf.CD_SWD1_PROJECT, 
                cd_swd2_project = conf.CD_SWD2_PROJECT)
        else:
            return_list = {'code':200,'msg':'success','data':{}}
            return json.dumps(return_list)
    else:
        if request.method == 'GET':
            correct_week = ExportProject.get_recent_week(week, value)
            return render_template('error.html',coodate = correct_week, date=week, project_name = project_name,
                                    default=project_name[0]['item'],
                                    department_default = department_default,
                                    department = department,
                                    cd_swd1_project = conf.CD_SWD1_PROJECT, 
                                    cd_swd2_project = conf.CD_SWD2_PROJECT)
        else:
            return_list = {'code':100,'msg':'No data of this week!','data':{}}
            return json.dumps(return_list)

@department_views.route('/export',methods=['GET', 'POST'])
def export():
    startdate = (datetime.date.today() - datetime.timedelta(days=30)).strftime("%Y-%m-%d")
    enddate = datetime.date.today().strftime("%Y-%m-%d")
    attach_path = os.path.join(os.getcwd(), "attach/atta/Disqualified_Data.xls")
    image_path = os.path.join(os.getcwd(), "img/")
    if request.method == 'POST':
        startdate = str(request.form['date1'])
        enddate = str(request.form['date2'])
        Substand = disqualified_data.SubstandardKPI(startdate, enddate, attach_path, image_path)
        Substand.send_email()
    return render_template('export.html', startdate=startdate, enddate=enddate)
