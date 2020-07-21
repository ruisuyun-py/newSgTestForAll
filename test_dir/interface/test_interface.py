import time
import urllib
from urllib.parse import urlencode

from selenium import webdriver
import page.base_page as base
import pytest
import requests
import page.login_page as login
import os
from sys import path

parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
path.insert(0, parentdir)


def setup_module(module):
    base.driver = webdriver.Chrome()
    base.cookies = login.login()


def setup_function(function):
    pass


def teardown_function(function):
    pass


def teardown_module(module):
    base.browser_close()
    print("测试结束")


def test_001():
    pass


def test_login_for_module():
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


def test_add_vip():
    vip_name = base.get_now_string()
    name = base.new_vip(vip_name)
    print(name)


def test_new_order():
    name = base.get_now_string()
    vip_info = base.new_vip(name)
    sku_info = [{'SkuId': '7494440356323262567', 'Qty': '2'}, ]
    order_info = base.new_order(vip_info, sku_info)
    print(order_info)


if __name__ == '__main__':
    pytest.main()
