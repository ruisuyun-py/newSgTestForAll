import sys
import time
from os.path import dirname, abspath
from selenium import webdriver
import page.base_page as base
import page.interface as interface
import pytest
import requests
import page.login_page as login

sys.path.insert(0, dirname(dirname(dirname(abspath(__file__)))))


def setup_module():
    base.cookies = interface.get_cookie()


def setup_function():
    pass


def teardown_function():
    pass


def teardown_module():
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
    vip_id = interface.get_vip_info("测试会员1")
    print(vip_id)


def test_get_vip_level_info():
    vip_level_info = interface.get_vip_level_info("8折")
    print(vip_level_info)


def test_modify_vip():
    interface.modify_vip("测试会员1", "8折")
    interface.modify_vip("测试会员1", "固定减5-1")


def test_new_order():
    name = base.get_now_string()
    print(name)
    interface.new_vip(name)
    sku_info = [{'SkuCode': '测试商品1-红色 XS', 'Qty': '2'}, ]
    order_info = interface.new_order(name, sku_info)
    print(order_info)


def test_get_product_info_by_id():
    result = interface.get_sku_price_by_vip_id("20200803195546", "20200803195549-红色 3XL")
    print(result)


def test_new_pos_order():
    sku_info = [
        {'SkuCode': '测试商品1-红色 XS', 'Qty': 2, 'Price': "80"},
        {'SkuCode': '测试商品1-红色 S', 'Qty': 2, 'Price': "90"},
        {'SkuCode': '测试商品1-红色 M', 'Qty': 2, 'Price': "100"},
    ]
    result = interface.new_pos_oder("芮苏云", sku_info)
    print(result)


def test_new_product():
    product_code = base.get_now_string()
    result = interface.new_product(product_code)
    print(result)


def test_get_sku_info():
    sku_code = "测试商品1-红色 XS"
    sku_id = interface.get_sku_info(sku_code)
    print(sku_id)
    product_info = interface.get_sku_info('', "测试商品1")
    print(product_info)


def test_modify_sku_price():
    result = interface.modify_sku_price("07080932-黑 XS XS", "7", )


def test_001():
    product_code = base.get_now_string()
    interface.new_product(product_code)
    print(f"新建商品,款号：{product_code}")
    sku_id_list = interface.get_sku_id('', product_code)
    print("sku_id列表：")
    print(sku_id_list)
    for i in sku_id_list:
        print(i)
    interface.new_create_sku_bar_code(sku_id_list)
    barcode_list = interface.get_sku_bar_code('', product_code)
    print("barcode_list列表：")
    for i in barcode_list:
        print(i)


def test_get_sku_unique_bar_code():
    result = interface.get_sku_unique_bar_code("测试商品1-红色 XL", 2)
    for i in result:
        print(i)


if __name__ == '__main__':
    pytest.main()
