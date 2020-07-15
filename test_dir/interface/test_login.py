import page.base_page as base
import pytest
import requests
import page.login_page as login
import os
from sys import path


parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
path.insert(0, parentdir)


def test_login():
    login.login()
    coo = base.driver.get_cookies()
    cookie_str = 'TOKEN='
    for c in coo:
        if c['name'] == 'TOKEN':
            cookie_str += c['value']
            cookie_str += ';'
        elif c['name'] == 'TENANTID':
            cookie_str += 'TENANTID='
            cookie_str += c['value']
    url = "http://gw.erp12345.com/api/Orders/AllOrder/QueryPage?ModelTypeName=ErpWeb.Domain.ViewModels.Orders" \
        ".AllOrderVmv&page=1&pagesize=20 "
    headers = {
        'Cookie': cookie_str
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
    # base.driver.quit()


if __name__ == '__main__':
    pytest.main(["-v", "-s", "test_all_order_query_page.py"])
