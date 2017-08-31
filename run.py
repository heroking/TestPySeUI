#coding=utf-8

import unittest
from public.common import HTMLTestRunner
import time
from config import globalparam
from public.common import sendmail

def run():
    test_dir = './testcase'
    suite = unittest.defaultTestLoader.discover(start_dir=test_dir,pattern='test*.py')

    now = time.strftime('%Y-%m-%d_%H_%M_%S')
    reportname = globalparam.report_path + '\\' + u'百度搜索测试报告' + now + '.html'
    with open(reportname,'wb') as f:
        runner = HTMLTestRunner.HTMLTestRunner(
            stream=f,
            title=u'百度测试报告',
            description=u'主要测试百度首页的搜索功能'
        )
        runner.run(suite)
    time.sleep(3)
    # 发送邮件  sendmail.SendMail("接受者邮箱地址","邮件主题","报告附件名")
    mail = sendmail.SendMail(None,u"百度测试报告",u"百度搜索测试报告.html")
    mail.send()

if __name__=='__main__':
    run()