import os
import requests
import page.base_page as base
import interface.supplier.supplier_interface as supplier_interface
import interface.product.product_interface as product_interface
import interface.finance.finance_interface as finance_interface

cookies = []


def get_cookie():
    # 获取当前文件的目录
    cur_path = os.path.abspath(os.path.dirname(__file__))
    # 获取根目录
    root_path = cur_path[:cur_path.find("newSgTestForAll\\") + len("newSgTestForAll\\")]
    with open(root_path + "/page/pda_cookie.txt", "r") as file:
        cookie = file.readline()
    return cookie


def login():
    """
    purchase_order_id:采购单Id
    """
    url = "http://gw.erp12345.com/api/PdaUser/Login?"
    params = {
        "companyName": "测试专用",
        "userName": "测试",
        "password": "8888",
        "deviceId": "10446013",
    }
    for k, v in params.items():
        url += f"{k}={v}&"
    response = requests.get(url)
    result = dict(response.json())
    print(f"登录返回数据：{result}")
    cookie_str = f"LoginToken={result['data']['LoginToken']}"
    # 获取当前文件的目录
    cur_path = os.path.abspath(os.path.dirname(__file__))
    # 获取根目录
    root_path = cur_path[:cur_path.find("newSgTestForAll\\") + len("newSgTestForAll\\")]
    with open(root_path + "/page/pda_cookie.txt", "w") as file:
        file.truncate()
        file.write(cookie_str)
    return cookie_str
