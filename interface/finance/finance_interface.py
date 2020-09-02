import time
import requests
import page.base_page as base
import interface.supplier.supplier_interface as supplier_interface
import interface.inventory.inventory_interface as inventory_interface
import interface.product.product_interface as product_interface


# 获取财务信息
def get_warehouse_cost_price_info(query_params_dict, return_info_list):
    """
        query_params_dict:查询信息字典{"仓库": "主仓库", "商家编码": "测试商品1-红色 XS",}
        return_info_list：需要返回的信息列表,如：["成本单价", "最新进价"]
        return:[{'最新进价': 100.0, '成本单价': 811.631883}]
    """
    """
    return:
    {"data":
        {"Items":
            [
                {
                    "Id":"7495063912123990225","ProductId":"7495063912123990219","SkuId":"7495063912123990225",
                    "WarehouseId":"162573418911628622","SupplierId":"0","PicUrl":"null","ThumbnailUrl":"",
                    "SkuCode":"20200820180212-红色 2XL","BarCode":null,"ProductName":"20200820180212",
                    "ProductCode":"20200820180212","SkuName":"红色 2XL","LastPurPrice":0.0,
                    "CostPrice":0.0,"Qty":0,"Balance":0.0,"HasRecord":false
                }
            ],
        "TotalCount":1
        },
    "code":1,
    "message":null}
    """
    # 信息对照表,方便通过显示名称获取数据库字段名称
    info_map = {
        "仓库": "WarehouseId",
        "供应商": "SupplierId",
        "商家编码": "SkuCode",
        "规格名称": "SkuName",
        "库存": "Qty",
        "商品条码": "BarCode",
        "未设置最新进价": "IsPurPrice",
        "有库存无成本": "IsPrice",
        "商品货号": "ProductCode",
        "最新进价": "LastPurPrice",
        "成本单价": "CostPrice",
    }
    params = {
        'ModelTypeName': 'ErpWeb.Domain.ViewModels.Finances.WarehousePurPriceVmv',
    }
    for k, v in query_params_dict.items():
        if k == "仓库":
            params[info_map[k]] = inventory_interface.get_inventory_id(v)
        elif k == "供应商":
            params[info_map[k]] = supplier_interface.get_supplier_info(v, "供应商ID")["供应商ID"]
        else:
            params[info_map[k]] = v
    url = "http://gw.erp12345.com/api/Finances/WarehousePurPrice/QueryPage?"
    for k, v in params.items():
        url += f"{k}={v}&"
    headers = {
        'Cookie': base.cookies
    }
    response = requests.get(url, headers=headers)
    result = dict(response.json())
    return_info = []
    for i in result["data"]["Items"]:
        info = {}
        for j in return_info_list:
            info[j] = i[info_map[j]]
        return_info.append(info)
    return return_info
