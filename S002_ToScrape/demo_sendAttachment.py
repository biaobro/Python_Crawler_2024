# !/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
@File               : demo_sendAttachment.py
@Project            : S002_ToScrape
@CreateTime         : 2024/7/14 17:26
@Author             : biaobro
@Software           : PyCharm
@Last Modify Time   : 2024/7/14 17:26 
@Version            : 1.0
@Description        : None
"""

# !/usr/bin/env python
# coding:utf-8

import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
from email.mime.multipart import MIMEMultipart


def email(message):
    srcAddr = "biaobro@sina.com"
    authCode = '454c3e4b484b6222'
    targetAddrs = ["weibiao.wb@alibaba-inc.com"]

    msg = MIMEMultipart()
    msg['From'] = formataddr(["管理员", 'biaobro@sina.com'])
    msg['To'] = formataddr(["Whatever", 'weibiao.wb@alibaba-inc.com'])
    msg['Subject'] = "A mail with attached file!"
    msg.attach(MIMEText(message, 'plain', 'utf-8'))

    # ---这是附件部分---
    # 构造附件1,文本类型附件
    # att1 = MIMEText(open('text.txt', 'rb').read(), 'base64', 'utf-8')
    # att1["Content-Type"] = 'application/octet-stream'
    # # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
    # att1["Content-Disposition"] = 'attachment; filename="books.csv"'
    # msg.attach(att1)

    # 构造附件2,jpg类型附件
    from email.mime.application import MIMEApplication
    # att2 = MIMEApplication(open('001.jpg', 'rb').read())
    # att2.add_header('Content-Disposition', 'attachment', filename="001.jpg")
    # msg.attach(att2)
    # # 构造附件3,pdf类型附件
    # att3 = MIMEApplication(open('test.pdf', 'rb').read())
    # att3.add_header('Content-Disposition', 'attachment', filename="test.pdf")
    # msg.attach(att3)
    # # 构造附件4,xlsx类型附件
    att4 = MIMEApplication(open('books.csv', 'rb').read())
    att4.add_header('Content-Disposition', 'attachment', filename="books.csv")
    msg.attach(att4)
    # # 构造附件5,mp3类型附件
    # att5 = MIMEApplication(open('test.mp3', 'rb').read())
    # att5.add_header('Content-Disposition', 'attachment', filename="test.mp3")
    # msg.attach(att5)

    try:
        server = smtplib.SMTP("smtp.sina.com", 25)
        # set_debuglevel(1)可以打印出和SMTP服务器交互的所有信息
        # server.set_debuglevel(1)
        # login()方法用来登录SMTP服务器
        server.login(srcAddr, authCode)
        # sendmail()方法就是发邮件，由于可以一次发给多个人，所以传入一个list，邮件正文是一个str，as_string()把MIMEText对象变成str
        server.sendmail(srcAddr, targetAddrs, msg.as_string())
        print("邮件发送成功!")
        server.quit()
    except smtplib.SMTPException:
        print("Error: 无法发送邮件")


if __name__ == '__main__':
    cpu = 100
    disk = 500
    mem = 50
    for i in range(1):
        if cpu > 90:
            alert = u"CPU出问题！"
            email(alert)
        if disk > 90:
            alert = u"硬盘出问题！"
            email(alert)
        if mem > 80:
            alert = u"内存出问题！"
            email(alert)
