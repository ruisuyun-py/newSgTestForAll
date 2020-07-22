import sys
from os.path import dirname, abspath
from selenium import webdriver
import page.base_page as base
import page.interface as interface
import pytest
import requests
import page.login_page as login

sys.path.insert(0, dirname(dirname(dirname(abspath(__file__)))))


def setup_module():
    base.driver = webdriver.Chrome()
    base.cookies = login.login()


def setup_function():
    pass


def teardown_function():
    pass


def teardown_module():
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
    name = interface.new_vip(vip_name)
    print(name)


def test_get_vip_id():
    vip_id = interface.get_vip_id("测试会员1")
    print(vip_id)


def test_new_order():
    name = base.get_now_string()
    vip_info = interface.new_vip(name)
    sku_info = [{'SkuId': '7494440356323262567', 'Qty': '2'}, ]
    order_info = interface.new_order(vip_info, sku_info)
    print(order_info)


def test_new_product():
    product_code = base.get_now_string()
    result = interface.new_product(product_code)
    print(result)


def test_get_sku_id():
    sku_code = "测试商品1-红色 XS"
    sku_id = interface.get_sku_id(sku_code)
    print(sku_id)


if __name__ == '__main__':
    pytest.main()
