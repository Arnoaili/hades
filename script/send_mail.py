#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
usage:
    send mail
'''
import smtplib
import glob
import re
import os
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.mime.image import MIMEImage

# 邮件发送模块
# domain_name: 发件人的域账号(代码中会默认在域账号前面加上"ta-cd/")
# sender_mail: 发件人的邮箱
# subject: 邮件标题
# mail_content: 邮件内容(html形式）
# to_list_str: 收件人列表
# sender_name: 发件人的姓名
# sender_passwd: 发件人的邮箱密码
# cc_list_str:　抄送人列表，默认为空
# image_path: 发送图片的路径，如果邮件内容中包含有图片，将所有的图片放在image_path路径下，发送时会从该路径读取所有的图片
# attach_path: 附件的路径，该路径下的所有东西都会当做附件发送　


def send_mail(domain_name, sender_mail, subject, mail_content, to_list, sender_name='',
              sender_passwd='', cc_list=[], image_path=None, attach_path=None):
    msg = MIMEMultipart('mixed')
    msg['Subject'] = subject
    if sender_name:
        msg['From'] = '"%s" <%s>' % (sender_name, sender_mail)
    else:
        msg['From'] = sender_mail

    if to_list:
        for to in to_list:
            msg['To'] = to.strip()
    if cc_list:
        for cc in cc_list:
            msg['Cc'] = cc.strip()
    address_list = set(to_list) | set(cc_list)

    content_part = MIMEMultipart('related')
    html_part = MIMEBase('text', 'html', charset="utf-8")
    html_part.set_payload(mail_content)
    encoders.encode_base64(html_part)
    html_part["Content-Disposition"] = 'filename="%s.html"' % \
            subject.replace(' ', '_')
    content_part.attach(html_part)
    if image_path:
        image_set = set()
        for image_str in re.findall(
                '<\s*img\s+src\s*=\s*\"?\s*cid\s*:\s*[^<>\"]+\s*\"?\s*>',
                mail_content):
            m = re.search(
                '<\s*img\s+src\s*=\s*\"?\s*cid\s*:\s*([^<>\"]+)\s*\"?\s*>',
                image_str)
            if m:
                image_set.add(m.group(1))

        for image_file in list(image_set):
            fo = open(image_path + os.sep + image_file)
            image_part = MIMEImage(fo.read())
            fo.close()
            image_part.add_header('Content-ID', '<%s>' % image_file)
            image_part["Content-Disposition"] = 'filename="%s"' % image_file
            content_part.attach(image_part)
    msg.attach(content_part)

    if attach_path:
        for attach_file in glob.glob(attach_path + os.sep + '*'):
            attach = MIMEBase('application', 'octet-stream')
            fo = open(attach_file, 'rb')
            attach.set_payload(fo.read())
            fo.close()
            encoders.encode_base64(attach)
            attach["Content-Disposition"] = 'attachment; filename="%s"' % \
                    os.path.split(attach_file)[1]
            msg.attach(attach)

    try:
        server = smtplib.SMTP('mailsh.tct.tcl.com')
    except Exception, e:
        print "Error occur while connect to mail server:\n%s" % e
        sys.exit(1)
    #server.set_debuglevel(1)
    if sender_passwd:
        try:
            server.login("ta-cd/%s" % domain_name, sender_passwd)
        except smtplib.SMTPAuthenticationError:
            print "Login mail server failed."
            server.quit()
            sys.exit(1)
    server.sendmail(msg['From'], list(address_list), msg.as_string())
    server.quit()