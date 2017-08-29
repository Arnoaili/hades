#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import query_ldap
import os
from Integrity import IntegrityClient
from Almfunc import Almfunc

class Almread:
    def __init__(self, bug_id = None):
        self.fields= ["Project", "Summary", "Priority", "Assigned User",
                        "SW Release", "Perso ID", 'State', 'Component', 
                        "Function", "Severity", "Frequency", "Detection",
                        "Regression", "Description", "CC","Reported By",
                        "LongTextReadOnly"]
        self.almquery = ['project', 'summary', 'priority', 'branch',
                            'sw_release', 'state', 'function', 'regression',
                            'description', 'assigned_user',
                            'sw_owner', 'long_text_read_only']
        self.bug_id = bug_id
        self.alm = Almfunc("").get_alm_connection()

    def get_item(self, alm_conn):
        item = alm_conn.getItem(item_id=self.bug_id, fields=self.fields)
        return item

    def get_version(self, alm_conn, item):
        item_id = []
        version_dict = {}
        if item.type == 'Defect':
            item_id.append(str(item.sw_release.IBPL[0]))
        versions = alm_conn.getItemsByIDs(item_ids=item_id,
                                          fields=['ID', 'Project', 'Version'])
        for version in versions:
            version_dict[version.id] = version.Version.shorttext.value
        return version_dict

    def get_branch(self, alm_conn, item):
        item_id = []
        branch_dict = {}
        if item.has_key('singleBranch'):
            item_id.append(item.singleBranch.IBPL[0])
        branchs = alm_conn.getItemsByIDs(item_ids=item_id,
                                        fields=['ID', 'Summary'])
        for item in branchs:
            branch_dict[item.id] = item.Summary.shorttext.value
        return branch_dict

    def get_bug_info(self, result, version, branch):
        bug_info = {}
        cc_email_list = []
        for query in self.almquery:
            if query in ('assigned_user'):
                if result.reporter is None or result.assigned_user is None:
                    bug_info[query] = 'other@tcl.com'
                else:
                    bug_info[query] = str(getattr(result, query).email)
            elif query in ('sw_release'):
                if result.type == 'Defect':
                    bug_info[query] = version[result.sw_release.IBPL[0]]
                else:
                    bug_info[query] = ''
            elif query in ('branch'):
                if result.has_key('singleBranch'):
                    bug_info[query] = branch[result.singleBranch.IBPL[0]]
                else:
                    bug_info[query] = 'None'
            elif query in ('cc_email'):
                for i in xrange(len(result.cc_email)):
                    cc_email_list.append(result.cc_email[i].email.value)
                bug_info[query] = cc_email_list
            elif query in ('sw_owner'):
                bug_info[query] = ''
            else:
                bug_info[query] = str(getattr(result, query))
        return bug_info

    def read_defect(self):
        item = self.get_item(self.alm)
        version = self.get_version(self.alm, item)
        branch = self.get_branch(self.alm, item)
        bug = self.get_bug_info(item, version, branch)
        return bug

class Almwrite:
    def __init__(self, bug_dict):
        self.bug_dict = bug_dict
        self.alm = Almfunc("").get_alm_connection()

    def create_defect(self):
        for key in ('Reported By', 'Assigned User', 'CC'):
            if key in ('Reported By', 'Assigned User'):
                to_name = query_ldap.search_ldap(self.bug_dict[key], 'sAMAccountName')
                self.bug_dict[key] = to_name
            elif key in ('CC'):
                name = []
                for mail in self.bug_dict[key]:
                    to_name = query_ldap.search_ldap(mail, 'sAMAccountName')
                    name.append(to_name)
                self.bug_dict[key] = ",".join(name)
        print self.bug_dict
        # ret = self.alm.createDefect(**self.bug_dict)
        # return ret.id

    def get_project(self):
        pro = self.alm.getProjects(fields=['Description', 'Name'])
        project = []
        for p in pro:
            project.append(p)
            #print p,p.name
        return project

    def get_branch(self, project):
        branch = []
        item_id = []
        big_item_id = []
        bra = self.alm.getItemsByCustomQuery(fields=['Description','Summary', 'Involved Projects'], query="(field[Type]=Branch)")
        # print bra
        for b in bra:
            if hasattr(b, 'Involved Projects') and str(b['Involved Projects'].IBPL[0]) not in ("2390598", "1856662", "1032979", "497102","546129","288144", "193157"):
                ## "2390598", "1856662", "1032979", "497102","546129","288144","193157" These bugs are invalid ! ##
                if len(item_id) <= 100:
                    item_id.append(b['Involved Projects'].IBPL[0])
                else:
                    big_item_id.append(item_id)
                    item_id = []
                    item_id.append(b['Involved Projects'].IBPL[0])

        # print big_item_id[3]
        # print len(big_item_id)
        # item_id = [1784580, 2466287, 1200891, 1912811, 1200891, 1200891, 3077795, 3044641, 3078102, 2655843, 2124300, 1200891, 1200891, 1200891, 1784580]
        for item_id in big_item_id:
            In_project = self.alm.getItemsByIDs(fields=['ID','Summary','Project'], item_ids=item_id)
            # print In_project

            for p in In_project:
                if p.Project.project.value == project:
                    print p.Project.project.value
                    branch.append(b.Summary.shorttext.value)
        return branch


if __name__ == '__main__':

    # alm = get_alm_connection()
    bug_id = 2157416
    tt = Almread(bug_id)
    print tt.alm
    # bug = tt.read_defect()
    # for key in bug.keys():
    #     print key,"#####",bug[key] 

    # project_id = None
    # dictt = {'Function': 'Google CTS / GTS / Verifier', 'Priority': 'P2 (Normal)', 'Description':'test for alm', 'Component': 'Google / Platform Issues', 'Summary': '[SWD_TEST][CTS Verifier]OTHER->Screen Pinning Test:Fail', 'In Project': '/TCT/MTK MT6572M/PIXI3-3.5 3G VF', 'CC': ['ke-feng@jrdcom.com', 'li.ai@tcl.com'], 'State': 'New', 'frequency': '8 - easy to reproduce->about 1 time out of 5', 'singleBranch': 'pixi3-3.5-3g-vf-l-v1.0-dint', 'Regression': 'NO', 'SW Owner': '', 'Assigned User': 'ke-feng@jrdcom.com', 'Perso ID': 'ZZ', 'Severity': '8 - high gravity->long loss of service(but not permanent)', 'SW Release': 'SWAK2J', 'Detection': '2 - very difficult to detect-> <1%', 'Reported By': 'li.ai@tcl.com'}
    # tt = Almwrite(dictt)
    # projects = tt.get_project()
    # for project in projects:
    #     print project.Name
    
    # for project in projects:
    #     # print project.id
    #     if project.Name == "/TCT/MTK MT6755M/SHINE PLUS VF":

    #         print project.ID
    #         project_id = int(project.ID)

    # # projects = alm.getItemsByProject(fields=['ID'],project = "SHINE PLUS")
    # # projects = alm.getProductsByName(fields=['ID', 'Summary',], name='/TCT/MTK MT6755M/SHINE PLUS VF')
    # # print projects


    # bra = alm.getItemsByCustomQuery(fields=['Description','Summary', 'Involved Projects'], query="(field[Type]=Branch)")

    # # print bra
    # # print project_id
    # for b in bra:
    #     # print b
    #     if hasattr(b, 'Involved Projects'):
    #         # print type(b['Involved Projects'].IBPL[0]), type(project_id)
    #         # print b['Involved Projects'].IBPL[0]
    #         # os.system("echo %s >> /home/liai/Desktop/log.log" % b['Involved Projects'].IBPL[0]) 
    #         # print b['Involved Projects']
    #         project_id = b['Involved Projects'].IBPL[0]
    #         query = '((field[ID]=%s))' % (str(project_id))
    #         project = alm.getItemsByCustomQuery(fields=['Project'],query=query)[0]

    #         # if b['Involved Projects'].IBPL[0] == project_id:
    #         #     print b.Summary.shorttext.value
    #         # print str(project.project)
    #         if str(project.project) == "/TCT/MTK MT6755M/SHINE PLUS VF":
    #             print b['Summary']
    # # print tt.create_defect()

    # # print tt.get_branch("/TCT/MTK MT6755M/SHINE PLUS VF")

    # """  
    # alm = get_alm_connection()
    # #x = alm.getItemsByFieldValues(fields=['ID', 'Summary'], State='Delivered')
    # #print x

    # j = alm.getItemsByCustomQuery(fields=['Description'], query="(field[Type]=Priority)")
    # print j

    # #x = alm.getItemsByNamedQuery(name="All Defects", fields=['Type', 'Description'])
    # #print x
    # j = alm.getItemsByCustomQuery(fields=['Description'], query="(field[Type]=Function)")
    # print j
    # """
    # alm = get_alm_connection()

    # # bra = alm.getItemsByCustomQuery(fields=['Description','Summary', 'Involved Projects'], query="(field[Type]=Project)")
    # # for b in bra:
    # #     print b
    # # #     if b.id not in (2242714, 1875832):
    # # #         # for value in b:
    # # #         #     print value

    # # #         if hasattr(b, 'Involved Projects'):
    # # #             print b,b["Summary"].shorttext.value, b['Involved Projects'].IBPL[0]

    #         # if b['Involved Projects'].IBPL[0] == project id:
    #         #    print b.Summary.shorttext.value

    # # pp = alm.getItemsByIDs(fields=['ID','Summary','Project'], item_ids=231600)
    # # print pp[0].Project.project.value
    # # "/TCT/MTK MT6755M/SHINE PLUS VF" 
    # print "begin search project name"
    # x = alm.getItemsByCustomQuery(fields=['Description'], query="(field[Project]=/TCT/MTK MT6755M/SHINE PLUS VF)")
    # # x = alm.getItemsByCustomQuery(fields=['Description','Summary', 'Involved Projects'], query="(field[Project]=/TCT/MTK MT6755M/SHINE PLUS VF)")
    # print x


