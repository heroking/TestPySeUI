#coding=utf-8

import os
from public.common.readconfig import ReadConfig

# 默认浏览器
browser = 'chrome' #or "firefox" or "internet explorer" or "opera"

# 默认邮件服务器地址和端口
email_smtp = 'smtp.qq.com'   # 163:smtp.163.com
email_prot = 25              # 163:25     QQ:需要设置独立密码和开启POP3、SMTP服务
# 默认邮件发送人账号和密码
email_sendaddr_name = '363060259@qq.com'
email_sendaddr_pwd = 'flsevkifcqqbbjfj'        #QQ邮箱密码必须是授权码
# 默认邮件接收人
# email_recvaddress = ['363060259@qq.com','418027013@qq.com','1292689135@qq.com','798210142@qq.com','994053455@qq.com']

email_recvaddress = ['363060259@qq.com']

# 读取config.ini配置文件
config_file_path = os.path.split(os.path.realpath(__file__))[0]
read_config = ReadConfig(os.path.join(config_file_path,'config.ini'))
# 读取config.ini配置文件项目参数地址
prj_path = read_config.getValue('projectConfig','project_path')
# 日志路径
log_path = os.path.join(prj_path, 'report', 'log')
# 截图文件路径
img_path = os.path.join(prj_path, 'report', 'screenshot')
# 测试报告路径
report_path = os.path.join(prj_path, 'report', 'testreport')
# 测试数据路径
data_path = os.path.join(prj_path, 'data', 'testdata')
