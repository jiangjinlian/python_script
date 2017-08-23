#!/bin/usr/env python
# -*- coding:utf-8 -*-
# Created by jiangjinlian on 2017/8/22

import sys
sys.path.append('/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages')
import unittest
from selenium import webdriver
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class Test_mail_126_login(unittest.TestCase):
    
    def setUp(self):
        self.driver = webdriver.Chrome()
    
    def test_mail_126_login(self):
        self.driver.get("https://cas.shmtu.edu.cn/cas/login?service=http%3A%2F%2Fportal.shmtu.edu.cn%2Fdcp%2Findex.jsp")
        self.driver.find_element_by_id("username").send_keys('201630310002')
        self.driver.find_element_by_id('password').send_keys('260788')
        self.driver.find_element_by_class_name('btn-submit').click()
        time.sleep(3)
        self.driver.find_element_by_link_text('here').click()
        self.assertIn('一卡通信息',self.driver.page_source)
    
    
    
    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
