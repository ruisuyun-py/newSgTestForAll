import http
import urllib
import page.base_page as base
import pytest
import requests

from page.base_page import driver
import page.login_page as lo

class TestLogin:
    def test_query(self):
        self.base_url = "http://erp12345.com/api/users/login/CheckLogin"
        login = {
            "companyName": "%E6%B5%8B%E8%AF%95%E4%B8%93%E7%94%A8",
            "username": "%E6%B5%8B%E8%AF%95",
            "password": "8888",
        }
        se = requests.session()
        response = se.get(self.base_url, data=login)
        # coo =
        # coo = requests.utils.dict_from_cookiejar(response.cookies)
        lo.login()
        coo = base.driver.get_cookies()

        # print(coo)
        co = requests.cookies.RequestsCookieJar()
        for c in coo:
            if c["name"] == "TOKEN":
                co.set('TOKEN', c["value"])

        self.base_url = "http://s40.erp12345.com/api/Orders/AllOrder/" \
                        "QueryPage?ModelTypeName=ErpWeb.Domain.ViewModels.Orders.AllOrderVmv&page=1&pagesize=20"
        se.cookies.update(co)
        print("查询之后的cookie内容：")
        print(se.cookies)

        response = se.get(self.base_url)
        print("查询结果：")
        print(response.text.encode('utf8'))
        base.driver.quit()


if __name__ == '__main__':
    pytest.main(["-v", "-s", "test_all_order_query_page.py"])
