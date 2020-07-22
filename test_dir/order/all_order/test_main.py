import sys
import time
import pytest
from os.path import dirname, abspath
from selenium import webdriver
from selenium.webdriver import ActionChains
import page.login_page as login
import page.base_page as base

sys.path.insert(0, dirname(dirname(dirname(abspath(__file__)))))


def setup_module(module):
    base.driver = webdriver.Chrome()
    base.cookies = login.login()
    print("全部订单测试开始")


def setup_function(function):
    base.open_page("订单","全部订单", "全部订单框架")


def teardown_function(function):
    base.close_page("全部订单")


def teardown_module(module):
    base.browser_close()
    print("全部订单测试结束")


def test_multi_search():
    time.sleep(2)


if __name__ == '__main__':
    pytest.main()
