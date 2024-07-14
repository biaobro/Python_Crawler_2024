# !/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
@File               : demo_sendMail.py
@Project            : S002_ToScrape
@CreateTime         : 2024/7/13 22:59
@Author             : biaobro
@Software           : PyCharm
@Last Modify Time   : 2024/7/13 22:59 
@Version            : 1.0
@Description        : None
"""

import smtplib


def prompt(title):
    return input(title).strip()


from_addr = prompt("From: ")
to_addrs = prompt("To: ").split()
print("Enter message, end with ^D (Unix) or ^Z (Windows):")

# Add the From: and To: headers at the start!
# 'To' 和 'From' 地址必须显式地包括在消息标头中:
lines = [f"From: {from_addr}", f"To: {', '.join(to_addrs)}", "hello world"]
while True:
    try:
        line = input()
    except EOFError:
        break
    else:
        lines.append(line)

msg = "\r\n".join(lines)
print("Message length is", len(msg))

print(from_addr, to_addrs)

server = smtplib.SMTP("smtp.sina.com", 25)

# login()方法用来登录SMTP服务器，sina邮箱需要用第三方授权码，直接登录的密码不可行
server.login('biaobro@sina.com', '454c3e4b484b6222')

# 可以打印出和SMTP服务器交互的所有信息
server.set_debuglevel(1)

# 可以一次发送给多人，所以 to_addrs 是个 list
server.sendmail(from_addr, to_addrs, msg)

# 断开连接
server.quit()
