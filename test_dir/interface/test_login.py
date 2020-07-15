import time

from selenium.webdriver import ActionChains

import page.base_page as base
import pytest
import requests
import page.login_page as login
import os
from sys import path


parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
path.insert(0, parentdir)


def setup_module(module):
    base.cookies = login.login()


def setup_function(function):
    base.driver.switch_to.default_content()
    base.wait_element(base.find_xpath("订单")).click()
    time.sleep(1)
    base.wait_element(base.find_xpath("全部订单")).click()
    time.sleep(1)
    base.driver.switch_to.default_content()
    frame = base.get_location("全部订单框架")
    base.driver.switch_to.frame(base.driver.find_element_by_xpath(base.get_location("全部订单框架")))


def teardown_function(function):
    base.driver.switch_to.default_content()
    ActionChains(base.driver).double_click(base.wait_element("//span[text()='全部订单']")).perform()


def teardown_module(module):
    # base.browser_close()
    print("测试结束")


def test_login_for_module():
    # cookie_str = login.login()
    url = "http://gw.erp12345.com/api/Orders/AllOrder/QueryPage?ModelTypeName=ErpWeb.Domain.ViewModels.Orders" \
        ".AllOrderVmv&page=1&pagesize=20 "
    headers = {
        'Cookie': base.cookies
    }
    response = requests.get(url, headers=headers)
    print()
    print("查询结果1：", end=' ')
    print(response.text.encode('utf8'))
    url = 'http://gw.erp12345.com/api/Orders/AllOrder/QueryPage?OrderStatus=1&ModelTypeName=ErpWeb.Domain.ViewModels' \
          '.Orders.AllOrderVmv&page=1&pagesize=20 '
    response = requests.get(url, headers=headers)
    print()
    print("查询结果2：", end=' ')
    print(response.text)


if __name__ == '__main__':
    pytest.main()
