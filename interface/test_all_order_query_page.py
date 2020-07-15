import pytest
import requests
import os
from sys import path

parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
path.insert(0, parentdir)


def test_login():
    base_url = ""
    pass


class TestQuery:
    """ 获得发布会列表 """

    def test_query(self):
        self.base_url = "http://s40.erp12345.com/api/Orders/AllOrder/" \
                        "QueryPage?ModelTypeName=ErpWeb.Domain.ViewModels.Orders.AllOrderVmv&page=1&pagesize=20"
        self.payload = {}
        self.files = {}
        self.headers = {
            'Cookie': 'LoginType=0; _ati=8376370957708; rememberUserName=true; '
                      '3AB9D23F7A4B3C9B'
                      '=H6W4GFSKI5K42JJNF4QE4PWC7WKRBIBLHA3HN6FV5KVOLCJ7PE3IW4M4B3KT4FSYKIRRLLLMNAD3V4DW42LJFDJOVM; '
                      'username=%E6%B5%8B%E8%AF%95; companyName=%E6%B5%8B%E8%AF%95%E4%B8%93%E7%94%A8; '
                      'TENANTID=7494308563943163372; '
                      'TOKEN'
                      '=AzTaukJqI4IJocwpZP0rRrUUIy3mooZVhRJgoKvTxvEJL_2njdyTyLF5TJql6X3l1rJ_2I94WwVQ_03ywPZuctVXhXeuhTUcAIkEoKNDUyLJFpkAe7GFsdZCCAHzGHDsz_0UPn4Ggy9xGjRgQnANjWovcniGWMfSr_0bm_0zcRR6Jv0Fo_1 '

        }
        response = requests.request("GET", self.base_url, headers=self.headers, data=self.payload, files=self.files)
        print(response.text.encode('utf8'))


if __name__ == '__main__':
    pytest.main(["-v", "-s", "test_all_order_query_page.py"])
