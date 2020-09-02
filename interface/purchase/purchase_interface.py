import time
import requests
import page.base_page as base
import interface.supplier.supplier_interface as supplier_interface
import interface.inventory.inventory_interface as inventory_interface
import interface.product.product_interface as product_interface


# 新建采购入库单并入库
def new_purchase_order(warehouse_name, supplier_name, sku_info_list, memo="", is_cash_pay="false"):
    """
        warehouse_name:仓库名称
        supplier_name:供应商名称
        memo:备注
        is_cash_pay: 现金支付
        sku_info_list :
        [
        {"商家编码":"测试商品1-红色 S","单价":"20","数量":"10"},
        {},
        ]
        return:{'ID': '7495081608949531534', 'Code': 'PUO2009010003'}
        """
    """
    sku_info_list : [
    {"SkuId":"7495079369275081918","ActualPrice":"20","Qty":"10"},
    {"SkuId":"7495079369275081919","ActualPrice":"21","Qty":"11"},
    {"SkuId":"7495079369275081920","ActualPrice":"22","Qty":"12"},
    {"SkuId":"7495079369275081921","ActualPrice":"23","Qty":"13"},
    {"SkuId":"7495079369275081922","ActualPrice":"24","Qty":"14"},
    {"SkuId":"7495079369275081923","ActualPrice":"25","Qty":"15"},
    {"SkuId":"7495079369275081924","ActualPrice":"26","Qty":"16"}
    ]
    返回数据：
    {"data":
        {
            "Id":"7495081583011954992",
            "Code":"PUO2009010001",
            "OutCode":null,
            "SupplierId":"7494441869460375525",
            "SupplierName":"供应商1",
            "WarehouseId":"162573418911628622",
            "WarehouseName":"主仓库",
            "Qty":91,
            "Amount":2121.0,
            "PayAmount":0.0,
            "IsCashPay":false,
            "Memo":"",
            "Status":"未审核",
            "StatusType":1,
            "IsSettlement":false,
            "SettlementAmount":0.0,
            "UnSettlementAmount":0.0,
            "RecordDate":"2020-09-01 22:36:38",
            "RecordUserName":"测试",
            "PushStatus":"",
            "WmsStatus":"",
            "WmsMessage":null,
            "StockInQty":0,
            "ProcurementType":null
        },
    "code":1,
    "message":null
    }
    """
    params = {"WarehouseId": inventory_interface.get_inventory_id(warehouse_name),
              "SupplierId": supplier_interface.get_supplier_info(supplier_name, ["供应商ID"])["供应商ID"],
              "Memo": memo,
              "IsCashPay": is_cash_pay,
              }
    lines = []
    for i in sku_info_list:
        line = {"SkuId": product_interface.get_sku_id(i["商家编码"])[0],
                "ActualPrice": i["单价"],
                "Qty": i["数量"]
                }
        lines.append(line)
    # print(lines)
    url = "http://gw.erp12345.com/api/Purchase/Purchase/AddPurchase?purchase={"
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


# 采购单审核并入库
def approve_and_stock_in_purchase_order(purchase_order_id):
    """
    purchase_order_id:采购单Id
    """
    url = "http://gw.erp12345.com/api/Purchase/Purchase/ApproveAndStockInOrder?"
    params = {
        "purchaseIds": purchase_order_id
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


# 采购单审核
def approve_purchase_order(purchase_order_id):
    """
        purchase_order_id:采购单Id
        """
    url = "http://gw.erp12345.com/api/Purchase/Purchase/ApprovePurchase?"
    params = {
        "purchaseIds": purchase_order_id
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

