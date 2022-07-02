#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2021/11/25 15:43
# @Author  : ZEV
# @File    : send_email.py
# @Content : 发送邮件
# !/usr/bin/env python
# -*- coding=utf-8 -*-
import smtplib
from email.mime.text import MIMEText
import threading
import time, datetime

from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

mailto_list = ["1652620697@qq.com"]  # 里面是对方的邮箱
# -----------QQ邮箱发送设置----------------------
mail_server = "smtp.163.com"  # 以qq邮箱为例子，里面是QQ邮箱的服务，换成其他邮箱需要更改服务
mail_user = "18169240419@163.com"  # 这是QQ邮箱的账号
mail_pass = "1137362935.zc"  # 如果是其他的可以直接填上密码，如果用qq之类的，或者邮箱未开服务，会提醒你打开下面的链接


# QQ邮箱需要去官方打开服务：http://service.mail.qq.com/cgi-bin/help?subtype=1&&id=28&&no=1001256
def send_mail(sub, content, my_msg):
    to_list = mailto_list
    # 以内嵌资源的方式存储在邮件中
    msg = MIMEMultipart('related')

    Info = MIMEText(content, 'html', 'utf-8')  # plain
    msg.attach(Info)
    msg["Accept-Language"] = "zh-CN"
    msg["Accept-Charset"] = "ISO-8859-1,utf-8"
    msg['Subject'] = sub
    msg['From'] = mail_user
    msg['To'] = ";".join(to_list)

    # 读取图片
    pic_path = "./pic"
    for k in my_msg.keys():
        file = open(f"{pic_path}/{my_msg[k][0]}.jpg", "rb")
        img_data = file.read()
        file.close()

        img = MIMEImage(img_data)
        img.add_header('Content-ID', f"{my_msg[k][0]}")
        msg.attach(img)

    try:
        server = smtplib.SMTP()
        server.connect(mail_server)
        server.starttls()
        server.login(mail_user, mail_pass)
        server.sendmail(mail_user, to_list, msg.as_string())
        server.close()
        return True
    except Exception as e:
        print(str(e))
        return False


def getDate():
    return str(datetime.datetime.utcfromtimestamp(time.time()) + datetime.timedelta(hours=8))


def send_warning_mail(title, info):
    nowTime = getDate()
    try:
        t = threading.Thread(target=send_mail, args=(mailto_list, title, str(nowTime) + " | " + str(info)))
        print()
        t.start()
    except Exception as e:
        print(e)
    # send_mail(mailto_list, "mysql异常", info)


if __name__ == "__main__":
    send_mail("运行完成提示!", str(getDate()) + " | " + "运行成功", {})
