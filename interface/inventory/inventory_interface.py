import time
import requests
import page.base_page as base
import interface.supplier.supplier_interface as supplier_interface


# 获取仓库信息
def get_inventory_info():
    """
    return = {'data':
    [
    {'Id': '162573418911628622', 'Code': '001', 'Name': '主仓库', 'OuterWarehouseId': '0', 'Type': 0, 'EnablePurchaseBin':
    False, 'EnableReturnBin': False, 'PurchaseBinPickSort': 0, 'ReturnBinPickSort': 0, 'IsDisable': False, 'HasSetting': False},
    {'Id': '7494446596088660373', 'Code': '测试仓', 'Name': '测试仓', 'OuterWarehouseId': '0', 'Type': 0, 'EnablePurchaseBin':
     False, 'EnableReturnBin': False, 'PurchaseBinPickSort': 0, 'ReturnBinPickSort': 0, 'IsDisable': False, 'HasSetting': False},
    {'Id': '7494805888474021990', 'Code': '新仓库', 'Name': '新仓库', 'OuterWarehouseId': '0', 'Type': 4, 'EnablePurchaseBin':
    False, 'EnableReturnBin': False, 'PurchaseBinPickSort': 0, 'ReturnBinPickSort': 0, 'IsDisable': False, 'HasSetting': False}
    ],
    'code': 1,
    'message': None}


    """
    url = "http://gw.erp12345.com/api/Basics/WarehouseExpress/GetWarehouseList?"
    headers = {
        'cookie': base.cookies
    }
    url_params = {
        'isDisable': 'false',
    }
    for k, v in url_params.items():
        url += f"'{k}'='{v}',"
    response = requests.get(url, headers=headers)
    result = dict(response.json())
    inventory_info_list = []
    for i in result["data"]:
        inventory_info = {}
        for k, v in i.items():
            if k == "Id":
                inventory_info["仓库ID"] = v
            elif k == "Name":
                inventory_info["仓库名称"] = v
        inventory_info_list.append(inventory_info)
    return inventory_info_list
