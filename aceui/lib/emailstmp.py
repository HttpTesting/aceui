"""
__doc__:
email 此模块用来，发送报告及邮件，格式为定制
如果要用在其它地方，需要修改
create:2018/10/23
by:yhleng
"""
import os
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.header import Header
from email import encoders
from aceui.lib import (gl, scripts)


class EmailClass(object):
    """发送电子邮件"""
    def __init__(self):
        self.cur_date_time = str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())) #当前日期时间
        self.config = scripts.get_yaml_field(gl.configFile) #配置文件路径
        self.sender = self.config['EMAIL']['Smtp_Sender'] # 从配置文件获取，发件人
        self.receivers = self.config['EMAIL']['Receivers']  # 从配置文件获取，接收人
        self.msg_title = self.config['EMAIL']['Msg_Title'] #从配置文件获取，邮件标题
        self.sender_server = self.config['EMAIL']['Smtp_Server'] #从配置文件获取，发送服务器
        self.From = self.config['EMAIL']['From']
        self.To = self.config['EMAIL']['To']


    @property
    def setMailContent(self):
        """配置邮件内容"""
        print(self.receivers)
        msg = MIMEMultipart()
        msg['From'] = Header(self.From, 'utf-8')
        msg['To'] = self.To
        msg['Subject'] = Header('%s%s'%(self.msg_title, self.cur_date_time), 'utf-8')

        #附件路径
        dirpath = gl.reportPath
        zipfile = os.path.join(os.path.dirname(dirpath), 'report.zip')
        reportfile = os.path.join(gl.reportPath, 'Report.html')
        scripts.zip_dir(dirpath, zipfile) #压缩报告
        #增加邮件内容为html
        fp = open(reportfile, 'rb')
        reportHtmlText = fp.read()
        msg.attach(MIMEText(reportHtmlText, 'html', 'utf-8'))
        fp.close()

        #增加附件
        html = self.addAttach(zipfile, filename='Report%s.zip'%self.cur_date_time) #自动化测试报告附件
        msg.attach(html)

        return msg



    def addAttach(self,apath, filename='Report.html'):
        """增加邮件"""
        with open(apath, 'rb') as fp:
            attach = MIMEBase('application', 'octet-stream')
            attach.set_payload(fp.read())
            attach.add_header('Content-Disposition', 'attachment', filename=filename)
            encoders.encode_base64(attach)
            return attach



    def sendEmail(self, message):
        """封装发送email方法"""
        try:

            smtpObj = smtplib.SMTP_SSL(self.sender_server, 465)
            smtpObj.connect(self.sender_server)

            smtpObj.login(self.sender, self.config['EMAIL']['Password'])
            smtpObj.sendmail(self.sender, self.receivers, message.as_string())
            smtpObj.quit()
            print("邮件发送成功")
        except smtplib.SMTPException as ex:
            print("Error: 无法发送邮件.%s"%ex)

    #发送调用
    def send(self):
        """发送email调用入口"""
        self.sendEmail(self.setMailContent)

if __name__ == "__main__":
    email = EmailClass()
    email.send()