#coding:utf-8

import os
import smtplib
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from public.common.log import Log
from config import globalparam

# 测试报告的路径
reportPath = globalparam.report_path
logger = Log()
# 配置收件人
recvaddress = globalparam.email_recvaddress
# 发件人账号和密码
sendaddr_name = globalparam.email_sendaddr_name
sendaddr_pswd = globalparam.email_sendaddr_pwd
# 邮件服务器地址和端口
email_smtp = globalparam.email_smtp
email_prot = globalparam.email_prot

class SendMail:
	def __init__(self,recver=None,subject=None,attach=None):
		"""接收邮件的人、邮件主题、附件"""
		if recver is None:
			self.sendTo = recvaddress
		else:
			self.sendTo = recver

		if subject is None:
			self.subjectname = "测试报告主题"
		else:
			self.subjectname = subject
			
		if attach is None:
			self.attachname = "测试报告附件.html".decode('utf-8').encode('gbk')    #解决中文乱码
		else:
			self.attachname = attach.decode('utf-8').encode('gbk')             #解决中文乱码

	def __get_report(self):
		"""获取最新测试报告"""
		dirs = os.listdir(reportPath)
		dirs.sort()
		newreportname = dirs[-1]
		print(u'最新报告名: {0}'.format(newreportname))
		return newreportname

	def __take_messages(self):
		"""生成邮件的内容 和 html报告附件"""
		newreport = self.__get_report()
		self.msg = MIMEMultipart()
		self.msg['Subject'] = self.subjectname
		self.msg['date'] = time.strftime('%a, %d %b %Y %H:%M:%S %z')

		with open(os.path.join(reportPath,newreport), 'rb') as f:
			mailbody = f.read()
		html = MIMEText(mailbody,_subtype='html',_charset='utf-8')
		self.msg.attach(html)
		
		# html附件
		att1 = MIMEText(mailbody, 'base64', 'utf-8')
		att1["Content-Type"] = 'application/octet-stream'
		att1["Content-Disposition"] = 'attachment; filename="'+str(self.attachname)+'"'
		self.msg.attach(att1)

	def send(self):
		"""发送邮件"""
		self.__take_messages()
		self.msg['from'] = sendaddr_name
		try:
			smtp = smtplib.SMTP(email_smtp,email_prot)
			
			# 设置为调试模式，就是在会话过程中会有输出信息
			#smtp.set_debuglevel(1)
			# ehlo命令，docmd方法包括了获取对方服务器返回信息，如果支持安全邮件，返回值里会有starttls提示
			#smtp.docmd("EHLO server")
			smtp.starttls()          # <------ 这行就是新加的支持安全邮件的代码！QQ邮箱必须增加
			# auth login 命令
			#smtp.docmd("AUTH LOGIN")
			
			smtp.login(sendaddr_name,sendaddr_pswd)
			smtp.sendmail(self.msg['from'], self.sendTo,self.msg.as_string())
			smtp.close()
			logger.info(u"发送邮件成功")
		except Exception:
			logger.error(u"发送邮件失败")
			raise

if __name__ == '__main__':
	sendMail = SendMail()
	sendMail.send()

