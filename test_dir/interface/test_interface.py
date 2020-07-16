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
    vip_name = base.get_now_string()
    vip_info = base.new_vip(vip_name)
    url = "http://gw.erp12345.com/api/Orders/AllOrder/AddOrder?order={\"Id\":\"0\",\"Tid\":\"\",\"OrderType\":1,\"DealDate\":\"2020-07-16 17:08:59\",\"ShopId\":\"7494440439622140309\",\"VipId\":\"" + vip_info[1] + "\",\"VipName\":\"" + vip_info[0] + "\",\"ExpressId\":\"7494440373939341490\",\"PostFee\":0,\"WarehouseId\":\"162573418911628622\",\"ProvinceName\":\"上海\",\"CityName\":\"上海市\",\"DistrictName\":\"闵行区\",\"ReceiverName\":\"芮苏云\",\"ReceiverPhone\":\"\",\"ReceiverMobile\":\"15221071395\",\"ReceiverRegionId\":\"0\",\"ReceiverZip\":\"\",\"ReceiverAddress\":\"衡东路189\",\"SellerMemo\":\"2\",\"BuyerMemo\":\"1\",\"Note\":\"\",\"SettlementMode\":0,\"SalesManId\":\"0\",\"SalesManName\":\"\",\"SellerFlag\":0,\"InvoiceTitle\":\"\",\"InvoiceNo\":\"\"}"
    payload = {}
    headers = {
        'Cookie': base.cookies
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    print(response.text.encode('utf8'))
    result = dict(response.json())
    url = "http://gw.erp12345.com/api/Orders/AllOrder/AddOrderLine?orderId=7495013147674151390&skus=[{\"SkuId\":\"7495003057839669935\",\"Qty\":1}]"
    response = requests.get(url, headers=headers)
    print(response.url)
    print(response.json())
    result = dict(response.json())
    url = "http://gw.erp12345.com/api/Orders/AllOrder/FastAddOrderPayment?orderId=7495013156901620392"
    response = requests.get(url, headers=headers)
    print(response.url)
    print(response.json())
    result = dict(response.json())


if __name__ == '__main__':
    pytest.main()
