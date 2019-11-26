#!/usr/bin/Python-3.6.2
import smtplib
import os
from email.mime.text import MIMEText
from email.utils import formataddr
from email.mime.multipart import MIMEMultipart


def get_mail(title, content, recipients):     # 不带附件邮件
    my_sender = 'guodisgao@foxmail.com'  # 发件人邮箱账号
    my_pass = 'sqbeggtyhkrdceba'  # 发件人邮箱密码/授权码
    my_user = recipients  # 收件人邮箱账号，我这边发送给自己
    res = True
    try:
        msg = MIMEText(content, 'plain', 'utf-8')  # 正文
        msg['From'] = formataddr([my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To'] = formataddr(["FK", my_user])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject'] = title  # 邮件的主题，也可以说是标题

        server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是25
        server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
        server.sendmail(my_sender, my_user, msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()  # 关闭连接
    except Exception:  # 如果 try 中的语句没有执行，则会执行下面的 res=False
        res = False
    if res:
        print("邮件发送成功")
    else:
        print("邮件发送失败")


def send_email(title, content, recipients, accessory):     # 带附件
    smtpserver = "smtp.qq.com"  # 发送服务器
    port = 465  # 端口
    sender = "1983496818@qq.com"  # 寄件人账号
    psw = "sqbeggtyhkrdceba"  # 授权码密码（在邮箱设置里面设置）
    receiver = recipients  # 接受者
    subject = title  # 标题

    # 创建一个带附件的实例
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = ';'.join(receiver)  # 多人接受时写法
    msg['Subject'] = subject

    # 构造附件：
    # 先读附件
    test_report = os.path.join(accessory)
    with open(test_report, "rb") as fp:
        mail_body = fp.read()
    # 邮件正文内容：
    msg.attach(MIMEText(content, 'plain', 'utf-8'))  # 正文是以文字存在时
    # mail_body = '邮件'     # 正文
    # msg.attach(MIMEText(mail_body, 'html', 'utf-8'))  # 正文以html存在时
    # 以下是写附件的格式：
    att = MIMEText(mail_body, "base64", 'utf-8')
    att["Content-Type"] = 'application/octet-stream'
    att["Content-Disposition"] = 'attachment;filename="report_test.html"'  # filename是重名附件名字
    msg.attach(att)
    # 同时兼容163和QQ邮箱的登录方法
    try:
        smtp = smtplib.SMTP()
        smtp.connect(smtpserver)
        smtp.login(sender, psw)  # 登录
    except:
        smtp = smtplib.SMTP_SSL(smtpserver, port)
        smtp.login(sender, psw)   # 登录
    smtp.sendmail(sender, receiver, msg.as_string())  # 发送 as_string 作为字符串类型发送msg['to'].split(",")
    smtp.quit()


# filename = r'E:\work\exc\jiekou\report\2019-04-01 14_49_28_result.html'
# send_email('接口自动化测试报告', '用例执行情况,见附件', ['1983496818@qq.com', '447397151@qq.com'], filename)


get_mail('蒙哥收', '蒙哥哈哈哈', '370192371@qq.com')
