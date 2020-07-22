import sys
import time

import pytest
from os.path import dirname, abspath
from selenium import webdriver
import page.login_page as login
import page.base_page as base
import page.order.all_order_page as order

sys.path.insert(0, dirname(dirname(dirname(abspath(__file__)))))


def setup_module():
    base.driver = webdriver.Chrome()
    base.cookies = login.login()
    print("全部订单测试开始")


def setup_function():
    base.open_page("订单", "全部订单", "全部订单框架")


def teardown_function():
    base.close_page("全部订单")


def teardown_module():
    base.browser_close()
    print("全部订单测试结束")


def test_multi_search():
    time.sleep(1)
    base.wait_element(order.locations["批量搜索下拉按钮"]).click()
    base.wait_element(base.find_xpath("搜索类型", "买家账号")).click()
    base.wait_element(order.locations["批量搜索文本框"]).send_keys("20200722150615")
    base.wait_table_refresh(base.find_xpath("每行一个", "确认"), 1, "会员名")



if __name__ == '__main__':
    pytest.main()
