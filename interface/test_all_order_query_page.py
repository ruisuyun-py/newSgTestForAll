import pytest
import requests
import os
from sys import path

parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
path.insert(0, parentdir)
from db_fixture import test_data


class TestQuery:
    ''' 获得发布会列表 '''

    def test_query(self):
        self.base_url = "http://s40.erp12345.com/api/Orders/AllOrder/" \
                        "QueryPage?ModelTypeName=ErpWeb.Domain.ViewModels.Orders.AllOrderVmv&page=1&pagesize=20"
        self.payload = {}
        self.files = {}
        self.headers = {
            'Cookie': 'TOKEN=AzTaukJqI4IJocwpZP0rRrUUIy3mooZVhRJgoKvTxvEJL_2njdyTyLF5TJql6X3l1rJ_2I94WwVQ_'
                      '03ywPZuctVXhXeuhTUcAIkEoKNDUyLJFpkAe7GFsdZCCAHzGHDsz_'
                      '0UBDTDZCdIucefx55F4_2pOXO7UsS2_0fuDoD_0J_0wrrwaQ8_1;'
                      ' TENANTID=7494308563943163372'
        }
        response = requests.request("GET", self.base_url, headers=self.headers, data=self.payload, files=self.files)
        print(response.text.encode('utf8'))


if __name__ == '__main__':
    pytest.main(["-v", "-s", "test_all_order_query_page.py"])
