#coding=utf-8

import unittest
from time import sleep
from public.common import excel
from public.common import pyseui
from config import globalparam
from public.common.log import Log

class TestBaiduIndex(unittest.TestCase):

    """百度搜索测试"""
    def setUp(self):
        self.logger = Log()
        self.logger.info('############################### START ###############################')
        self.dr = pyseui.PySeUI(globalparam.browser)
        self.dr.max_window()
        self.dr.open('http://www.baidu.com')

    def tearDown(self):
        self.dr.quit()
        self.logger.info('###############################  End  ###############################')

    def _search(self,searchKey):
        """封装百度搜索的函数"""
        self.dr.clear_type('id->kw',searchKey)
        self.dr.click('id->su')
        sleep(2)
        self.assertIn(searchKey, self.dr.get_title())

    def test_search(self):
        """直接搜索"""
        self.dr.clear_type('id->kw',u'小石头tester')
        self.dr.click('id->su')
        sleep(2)
        self.assertIn(u'小石头', self.dr.get_title())


    def test_search_excel(self):
        """使用数据驱动,进行测试"""
        datas = excel.get_xls_to_list('searKey.xlsx','Sheet1')
        for data in datas:
            self._search(data)

