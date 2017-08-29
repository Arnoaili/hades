# -*- coding:utf-8 -*-
import MySQLdb
import os
import datetime

def removeChinese(file_):
    # 去掉乱码 中文，全部转成小写
    with open(file_,'r') as f:
        ls1 = f.readlines()
    ls2 = []
    for li in ls1:
        flag = True
        for lj in li:
            try:
                t = lj.decode('utf8')
                # print 'len(t) is:'+str(len(t))
                if len(t) > 1:
                    flag = False
                    break
            except:
                flag = False
                break
        if flag:
            ls2.append(li.lower())
    return ls2

def get_data(cursor, dir_name):
    today = datetime.date.today().strftime("%Y-%m-%d") + " 00:00:00"
    fobj1=open(dir_name + "/new_add_bugs.txt",'w+')
    cursor.execute("select bug_id,project_name,summary from base where created_date>'%s'" % (today))
    for row in cursor.fetchall():
        fobj1.write(str(row[0]) + "\t" + row[1] + '\t' + row[2] + '\n')
    fobj1.close()

    rc_data = removeChinese(dir_name+ "/new_add_bugs.txt")
    with open(dir_name + '/new_add_bugs_RC.txt', 'w') as f:
        f.writelines(rc_data)
    # ------------------------------------------------------------------------------
    fobj2=open(dir_name + "/all_bugs.txt",'w+')
    cursor.execute("select bug_id,project_name,summary from base")
    for row in cursor.fetchall():
        fobj2.write(str(row[0]) + "\t" + row[1] + '\t' + row[2] + '\n')
    fobj2.close()

    rc_data = removeChinese(dir_name+ "/all_bugs.txt")
    with open(dir_name + '/all_bugs_RC.txt', 'w') as f:
        f.writelines(rc_data)
    if os.path.isfile(dir_name + "/deerwester.dict"):
        os.remove(dir_name + "/deerwester.dict")


if __name__ == "__main__":
    conn = MySQLdb.connect(host='localhost', user="root", passwd="admin0", db="hades", port=3306)
    cursor = conn.cursor()
    dir_name = os.getcwd()
    get_data(cursor, dir_name)
