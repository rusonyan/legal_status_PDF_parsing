import smtplib
from email.mime.text import MIMEText

from win10toast import ToastNotifier

toaster = ToastNotifier()
host = 'smtp.email.cn'
user = 'yanruisong@email.cn'
pwd = 'KegAnNBedRWdXtjH'
sender = 'yanruisong@email.cn'
receivers = ['rusonbot@139.com']


def send_mail(title, msg):
    message = MIMEText(msg, 'plain', 'utf-8')
    message['Subject'] = title
    message['From'] = sender
    message['To'] = receivers[0]
    smtpObj = smtplib.SMTP()
    smtpObj.connect(host, 25)
    smtpObj.login(user, pwd)
    smtpObj.sendmail(
        sender, receivers, message.as_string())
    smtpObj.quit()
    print('success')


def send(title, msg):
    toaster.show_toast(title,
                       msg,
                       threaded=True,
                       icon_path=None,
                       duration=5, )


def send_errow(msg):
    send("错误", msg)
    send_mail('错误', msg)
