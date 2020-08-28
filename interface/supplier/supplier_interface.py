import os
import time
import requests
import page.base_page as base


def get_supplier_info(supplier_name, require_info_name_list):
    """
    supplier_name:供应商名称
    require_info_name_list:比如：["供应商ID","市场","联系人",]
        "供应商ID": "Id",
        "市场": "BazaarName",
        "联系人": "ContactName",
        "手机": "ContactMobile",
        "地址": "ContactAddress",
        "备注": "Memo",
        "隐藏": "IsHide",
    return:{"供应商ID":"111111","市场":"2222","联系人":"33333",}
    原始数据：
    {"data":
        {"Items":
            [
                {"Id":"7494441869460375525","SupplierName":"供应商1","SupplierCode":null,"BazaarName":"市场",
                "SupplierType":null,"SupplierTypeId":"0","ContactName":"联系人","ContactMobile":"联系人手机",
                "ContactAddress":"联系人地址","Memo":"备注","IsHide":false}
            ],
        "TotalCount":1
        },
    "code":1,
    "message":null
    }
    """
    supplier_info_mapping = {
        "供应商ID": "Id",
        "市场": "BazaarName",
        "联系人": "ContactName",
        "手机": "ContactMobile",
        "地址": "ContactAddress",
        "备注": "Memo",
        "隐藏": "IsHide",
    }
    user_info = {
        'ModelTypeName': 'ErpWeb.Domain.ViewModels.Settings.SupplierVmv',
        'SupplierName': supplier_name,
        'IsHide': 'false',
    }
    url = "http://gw.erp12345.com/api/Settings/Supplier/QueryPage?"
    for k, v in user_info.items():
        url += f"{k}={v}&"
    headers = {
        'Cookie': base.cookies
    }
    response = requests.get(url, headers=headers)
    result = dict(response.json())
    supplier_info_list = {}
    for i in require_info_name_list:
        supplier_info_list[i] = result["data"]["Items"][0][supplier_info_mapping[i]]
    return supplier_info_list
