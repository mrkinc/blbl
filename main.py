import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def start():
    msg_from = '790801144@qq.com'  # 发送方邮箱
    passwd = "arvxmcmyhujqbfjj"  # 就是上面的授权码

    to = ['790801144@qq.com']  # 接受方邮箱

    # 设置邮件内容
    # MIMEMultipart类可以放任何内容
    msg = MIMEMultipart()
    content = "这个是字符串"
    # 把内容加进去
    msg.attach(MIMEText(content, 'plain', 'utf-8'))

    # 设置邮件主题
    msg['Subject'] = "ToEdit"

    # 发送方信息
    msg['From'] = msg_from

    # 通过SSL方式发送，服务器地址和端口
    s = smtplib.SMTP_SSL("smtp.qq.com", 465)
    # 登录邮箱
    s.login(msg_from, passwd)
    # 开始发送
    s.sendmail(msg_from, to, msg.as_string())
    print("邮件发送成功")


if __name__ == '__main__':
    start()


