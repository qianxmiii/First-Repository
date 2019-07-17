#*-coding:utf-8-*-
import smtplib
import requests
import re
import time
from email.mime.text import MIMEText
from email.header import Header
from email.utils import parseaddr, formataddr

# 格式化邮件地址，包含中文，需要通过Header对象进行编码
def _format_addr(s):
    name,addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(),addr.encode('utf-8') if isinstance(addr, unicode) else addr))


def sendemail():
    # 邮件服务器
    smtp_server = 'smtp.163.com'
    # 发件人邮箱及密码（163邮箱需授权码）
    from_addr = 'xxx@163.com'
    password = 'xxx'
    # 收件人邮箱
    to_addr = 'xxx@163.com'

    # 邮件对象
    msg = MIMEText('hello, send by Python...', 'plain', 'utf-8')
    msg['From'] = _format_addr(u'草莓味奶昔 <%s>' % from_addr)
    msg['To'] = _format_addr(u'苦哈哈的租房党 <%s>' % to_addr)
    msg['Subject'] = Header(u'房子在等你，快预订！', 'utf-8').encode()

    server = smtplib.SMTP(smtp_server, 25)
    # 打印详细连接信息
    server.set_debuglevel(1)
    server.login(from_addr, password)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()

print ("开始找房子啦")
session = requests.session()

while (1):
    try:
        # 待释放
        room_url = "http://www.ziroom.com/x/738198018.html"
        response_ziroom = session.get(room_url,headers ={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:48.0) Gecko/20100101 Firefox/48.0'})
        webpage_result = re.compile(r'class="status iconicon_release"') # 待释放
        analyze_result = re.search(webpage_result, response_ziroom._content)
        if analyze_result:
            print "还没释放呢，耐心等待!"
            print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            time.sleep(30)
        else:
            sendemail(5)
            print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            print "房子释放了，快抢！"
            break
    except:
        print "连接失败啦！嘤嘤嘤"