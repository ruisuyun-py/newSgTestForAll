import time
import requests
import page.base_page as base
import interface.supplier.supplier_interface as supplier_interface
import interface.product.product_interface as product_interface
import interface.finance.finance_interface as finance_interface


# 获取仓库信息
def get_inventory_info():
    """
    return:
    [
    {'仓库ID': '162573418911628622', '仓库名称': '主仓库'},
    {'仓库ID': '7494446596088660373', '仓库名称': '测试仓'},
    {'仓库ID': '7494805888474021990', '仓库名称': '新仓库'}
    ]

    """
    """
    原始数据：
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


# 获取仓库ID
def get_inventory_id(inventory_name):
    inventory_info_list = get_inventory_info()
    inventory_id = ""
    for i in inventory_info_list:
        if i["仓库名称"] == inventory_name:
            inventory_id = i["仓库ID"]
    return inventory_id


# 新增入库单
def new_stock_in_order(warehouse_name, supplier_name, sku_info_list, memo=''):
    """
            warehouse_name:仓库名称
            supplier_name:供应商名称
            memo:备注
            sku_info_list :
            [
            {"商家编码":"测试商品1-红色 S","数量":"10"},
            {},
            ]
            return:{'ID': '7495081608949531534', 'Code': 'PUO2009010003'}
    """
    """
    sku_info_list : [
    {"SkuId":"7494440356323262567","CostPrice":811.63,"Qty":1},
    {"SkuId":"7494440356323262568","CostPrice":133.99,"Qty":1}
    ]
    返回数据：
    {"data":
        {
            "Id":"7495082491766636848",
            "Code":"SIO2009020002",
            "SourceOrderCode":null,
            "StockInType":0,
            "StockInSearchType":2,
            "StockInSearchTypeName":"无采购入库",
            "StockInTypeName":"手动新增",
            "SupplierId":"7494441869460375525",
            "SupplierName":"供应商1",
            "WarehouseId":"162573418911628622",
            "WarehouseName":"主仓库",
            "Qty":2,
            "Amount":945.62,
            "StockInUserName":null,
            "IsStockIn":false,
            "Memo":"",
            "RecordDate":"2020-09-02 13:39:24",
            "RecordUserName":"测试",
            "StockInDate":null
        },
    "code":1,
    "message":null
    }
    """
    params = {"WarehouseId": get_inventory_id(warehouse_name),
              "SupplierId": supplier_interface.get_supplier_info(supplier_name, ["供应商ID"])["供应商ID"],
              "Memo": memo,
              }
    lines = []
    for i in sku_info_list:
        query_info_list = {"仓库": "主仓库", "商家编码": i["商家编码"]}
        return_info_list = ["成本单价"]
        cost_price = finance_interface.get_warehouse_cost_price_info(query_info_list, return_info_list)[0]["成本单价"]
        line = {"SkuId": product_interface.get_sku_id(i["商家编码"])[0],
                "ActualPrice": cost_price,
                "Qty": i["数量"]
                }
        lines.append(line)
    # print(lines)
    url = "http://gw.erp12345.com/api/Stocks/StockInOrder/AddStockInOrder?stock={"
    for k, v in params.items():
        url += f"'{k}':'{v}',"
    url += "'Lines':["
    for i in lines:
        url += "{"
        for k, v in i.items():
            url += f"'{k}':{v},"
        url += "},"
    url += "]}"
    headers = {
        'Cookie': base.cookies
    }
    response = requests.get(url, headers=headers)
    result = dict(response.json())
    purchase_order_info_list = {
        "ID": result["data"]["Id"],
        "Code": result["data"]["Code"],
    }
    return purchase_order_info_list


# 入库单入库
def stock_in_stock_in_order(stock_in_order_id):
    """
    purchase_order_id:入库单ID
    """
    url = "http://gw.erp12345.com/api/Stocks/StockInOrder/StockIn?"
    params = {
        "stockIds": stock_in_order_id
    }
    for k, v in params.items():
        url += f"{k}={v}"
    headers = {
        'Cookie': base.cookies
    }
    # print(url)
    response = requests.get(url, headers=headers)
    result = dict(response.json())
    return result


# 新建出库单
def new_stock_out_order(warehouse_name, supplier_name, sku_info_list, memo=''):
    """
                warehouse_name:仓库名称
                supplier_name:供应商名称
                memo:备注
                sku_info_list :
                [
                {"商家编码":"测试商品1-红色 S","数量":"10"},
                {},
                ]
                return:{'ID': '7495081608949531534', 'Code': 'PUO2009010003'}
    """
    """
    sku_info_list : [
    {"SkuId":"7494440356323262567","CostPrice":811.63,"Qty":1},
    {"SkuId":"7494440356323262568","CostPrice":133.99,"Qty":1}
    ]
    返回数据：
    {"data":
        {
            "Id":"7495082984681243534",
            "Code":"SOO2009020002",
            "SourceOrderCode":null,
            "StockOutType":1,
            "StockOutTypeName":"采购退货出库",
            "StockOutSort":null,
            "SupplierId":"7494849432077207121",
            "SupplierName":"00000",
            "WarehouseId":"162573418911628622",
            "WarehouseName":"主仓库",
            "Qty":4,
            "Amount":1891.24,
            "StockOutUserName":null,
            "StockOutDate":null,
            "StockOut":false,
            "Memo":"",
            "RecordDate":"2020-09-02 21:49:05",
            "RecordUserName":"测试"
        },
    "code":1,
    "message":null
    }
    """
    params = {"WarehouseId": get_inventory_id(warehouse_name),
              "SupplierId": supplier_interface.get_supplier_info(supplier_name, ["供应商ID"])["供应商ID"],
              "Memo": memo,
              }
    lines = []
    for i in sku_info_list:
        query_info_list = {"仓库": "主仓库", "商家编码": i["商家编码"]}
        return_info_list = ["成本单价"]
        cost_price = finance_interface.get_warehouse_cost_price_info(query_info_list, return_info_list)[0]["成本单价"]
        line = {"SkuId": product_interface.get_sku_id(i["商家编码"])[0],
                "ActualPrice": cost_price,
                "Qty": i["数量"]
                }
        lines.append(line)
    # print(lines)
    url = "http://gw.erp12345.com/api/Stocks/StockOutOrder/AddStockOutOrder?&stock={"
    for k, v in params.items():
        url += f"'{k}':'{v}',"
    url += "'Lines':["
    for i in lines:
        url += "{"
        for k, v in i.items():
            url += f"'{k}':{v},"
        url += "},"
    url += "]}"
    headers = {
        'Cookie': base.cookies
    }
    response = requests.get(url, headers=headers)
    result = dict(response.json())
    purchase_order_info_list = {
        "ID": result["data"]["Id"],
        "Code": result["data"]["Code"],
    }
    return purchase_order_info_list


# 出库出库单
def stock_out_stock_out_order(stock_out_order_id):
    """
        purchase_order_id:入库单ID
        """
    url = "http://gw.erp12345.com/api/Stocks/StockOutOrder/NewStockOut?"
    params = {
        "stockIds": stock_out_order_id
    }
    for k, v in params.items():
        url += f"{k}={v}"
    headers = {
        'Cookie': base.cookies
    }
    # print(url)
    response = requests.get(url, headers=headers)
    result = dict(response.json())
    return result


# 新建退货出库单
def new_refund_out_order(warehouse_name, supplier_name, sku_info_list, memo=''):
    """
                    warehouse_name:仓库名称
                    supplier_name:供应商名称
                    memo:备注
                    sku_info_list :
                    [
                    {"商家编码":"测试商品1-红色 S","数量":"10"},
                    {},
                    ]
                    return:{'ID': '7495081608949531534', 'Code': 'PUO2009010003'}
    """
    """
    sku_info_list : [
    {"SkuId":"7494440356323262567","CostPrice":811.63,"Qty":1},
    {"SkuId":"7494440356323262568","CostPrice":133.99,"Qty":1}
    ]
    返回数据：
    {"data":
        {
            "Id":"7495082984681243534",
            "Code":"SOO2009020002",
            "SourceOrderCode":null,
            "StockOutType":1,
            "StockOutTypeName":"采购退货出库",
            "StockOutSort":null,
            "SupplierId":"7494849432077207121",
            "SupplierName":"00000",
            "WarehouseId":"162573418911628622",
            "WarehouseName":"主仓库",
            "Qty":4,
            "Amount":1891.24,
            "StockOutUserName":null,
            "StockOutDate":null,
            "StockOut":false,
            "Memo":"",
            "RecordDate":"2020-09-02 21:49:05",
            "RecordUserName":"测试"
        },
    "code":1,
    "message":null
    }
    """
    params = {"WarehouseId": get_inventory_id(warehouse_name),
              "SupplierId": supplier_interface.get_supplier_info(supplier_name, ["供应商ID"])["供应商ID"],
              "Memo": memo,
              }
    lines = []
    for i in sku_info_list:
        query_info_list = {"仓库": "主仓库", "商家编码": i["商家编码"]}
        return_info_list = ["成本单价"]
        cost_price = finance_interface.get_warehouse_cost_price_info(query_info_list, return_info_list)[0]["成本单价"]
        line = {"SkuId": product_interface.get_sku_id(i["商家编码"])[0],
                "ActualPrice": cost_price,
                "Qty": i["数量"]
                }
        lines.append(line)
    # print(lines)
    url = "http://gw.erp12345.com/api/Stocks/StockOutOrder/AddStockOutProductOrder?stock={"
    for k, v in params.items():
        url += f"'{k}':'{v}',"
    url += "'Lines':["
    for i in lines:
        url += "{"
        for k, v in i.items():
            url += f"'{k}':{v},"
        url += "},"
    url += "]}"
    headers = {
        'Cookie': base.cookies
    }
    response = requests.get(url, headers=headers)
    result = dict(response.json())
    purchase_order_info_list = {
        "ID": result["data"]["Id"],
        "Code": result["data"]["Code"],
    }
    return purchase_order_info_list
