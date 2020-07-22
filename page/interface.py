import time
import requests
import page.base_page as base


# 新增会员
def new_vip(name):
    """
    name:会员名称，一般用get_now_string()生成
    return:返回【会员ID，会员名称】
    """
    headers = {
        'Cookie': base.cookies
    }
    vip = {
        'Id': 0,
        'VipId': 0,
        'Platform': 0,
        'ShopId': 0,
        'IsPosVip': 'true',
        'VipName': name,
        'VipCode': name,
        'ShipName': '',
        'ShipMobile': '',
        'ReceiverName': '芮苏云',
        'ReceiverMobile': '15221071395',
        'ReceiverPhone': '',
        'ReceiverZip': '',
        'ProvinceName': '上海',
        'CityName': '上海市',
        'DistrictName': '闵行区',
        'ReceiverAddress': '衡东路189',
        'IsIllegal': 'false'
    }
    url_param = ''
    for k, v in vip.items():
        url_param += f"'{k}':'{v}',"
    url = "http://gw.erp12345.com/api/Vips/FullVip/SaveVip?vip={" + url_param + "}"
    response = requests.get(url, headers=headers, )
    result = dict(response.json())
    vip_info = [result["data"]["VipId"], result['data']['VipName']]
    return vip_info


# 获取会员ID
def get_vip_id(name):
    """
    name:会员名称
    return vip_id 直接返回会员id
    """
    user_info = {
        'ModelTypeName': 'ErpWeb.Domain.ViewModels.Vips.FullVipVmv',
        'VipName': name,
        'IsHide': 'false',
    }
    url = "http://gw.erp12345.com/api/Vips/FullVip/QueryPage?"
    for k, v in user_info.items():
        url += f"{k}={v}&"
    headers = {
        'Cookie': base.cookies
    }
    response = requests.get(url, headers=headers)
    vip_id = dict(response.json())['data']['Items'][0]['VipId']
    return vip_id


# 新建商品
def new_product(product_code):
    """
    product_code:商品货号，一般通过get_now_string 获取
    return:返货商品id和商家编码列表
    比如：[
    {'Id': '7495021643807326816', 'Code': '20200722141224-红色 XS'},
    {'Id': '7495021643807326817', 'Code': '20200722141224-红色 S'},
    ]
    """
    url = "http://gw.erp12345.com/api/Products/FullProduct/New"
    url += "?product={"
    product_info = {
        "Name": product_code,
        "Code": product_code,
        "ProductCategoryId": "0",
        "ShortName": '',
        "V": "0",
        "BrandId": "0",
        "Unit": "",
        "PicUrl": "",
        "StandardPrice": '0',
    }
    for k, v in product_info.items():
        url += f"'{k}':'{v}',"
    product_skus = [
        {"Id": "0", "Name": "红色 XS", "Code": "" + product_code + "-红色 XS", "LastPurPrice": 0, "StandardPrice": 0,
         "Weight": 0, "PackageWeight": 0, "BarCode": "null", "ValidityDate": time.strftime('%Y-%m-%d %H:%M:%S'),
         "SkuImg": "null", "IsHide": "false", "V": 0},
        {"Id": "0", "Name": "红色 S", "Code": "" + product_code + "-红色 S", "LastPurPrice": 0, "StandardPrice": 0,
         "Weight": 0, "PackageWeight": 0, "BarCode": "null", "ValidityDate": time.strftime('%Y-%m-%d %H:%M:%S'),
         "SkuImg": "null", "IsHide": "false", "V": 0},
        {"Id": "0", "Name": "红色 M", "Code": "" + product_code + "-红色 M", "LastPurPrice": 0, "StandardPrice": 0,
         "Weight": 0, "PackageWeight": 0, "BarCode": "null", "ValidityDate": time.strftime('%Y-%m-%d %H:%M:%S'),
         "SkuImg": "null", "IsHide": "false", "V": 0},
        {"Id": "0", "Name": "红色 L", "Code": "" + product_code + "-红色 L", "LastPurPrice": 0, "StandardPrice": 0,
         "Weight": 0, "PackageWeight": 0, "BarCode": "null", "ValidityDate": time.strftime('%Y-%m-%d %H:%M:%S'),
         "SkuImg": "null", "IsHide": "false", "V": 0},
        {"Id": "0", "Name": "红色 XL", "Code": "" + product_code + "-红色 XL", "LastPurPrice": 0, "StandardPrice": 0,
         "Weight": 0, "PackageWeight": 0, "BarCode": "null", "ValidityDate": time.strftime('%Y-%m-%d %H:%M:%S'),
         "SkuImg": "null", "IsHide": "false", "V": 0},
        {"Id": "0", "Name": "红色 2XL", "Code": "" + product_code + "-红色 2XL", "LastPurPrice": 0, "StandardPrice": 0,
         "Weight": 0, "PackageWeight": 0, "BarCode": "null", "ValidityDate": time.strftime('%Y-%m-%d %H:%M:%S'),
         "SkuImg": "null", "IsHide": "false", "V": 0},
        {"Id": "0", "Name": "红色 3XL", "Code": "" + product_code + "-红色 3XL", "LastPurPrice": 0, "StandardPrice": 0,
         "Weight": 0, "PackageWeight": 0, "BarCode": "null", "ValidityDate": time.strftime('%Y-%m-%d %H:%M:%S'),
         "SkuImg": "null", "IsHide": "false", "V": 0},
    ]
    url += "'ProductSkus':["
    for sku in product_skus:
        url += "{"
        for k, v in sku.items():
            url += f"'{k}':'{v}',"
        url += "},"
    url += "]}"
    headers = {
        'cookie': base.cookies
    }
    response = requests.post(url, headers=headers)
    sku_list = dict(response.json())['data']['ProductSkus']
    sku_info = []
    for i in sku_list:
        sku = {'Id': i['Id'], 'Code': i['Code']}
        sku_info.append(sku)
    return sku_info


# 获取商家编码id
def get_sku_id(sku_code):
    """
    sku_code:需要查询的商家编码
    return:sku_id
    """
    url_params = {
        'ModelTypeName': 'ErpWeb.Domain.ViewModels.Products.FullProductVmv',
        'SkuCode': sku_code,
        'ishide': 'false',
    }
    url = "http://gw.erp12345.com/api/Products/FullProduct/QueryPage?"
    for k, v in url_params.items():
        url += f"{k}={v}&"
    headers = {
        'cookie': base.cookies
    }
    response = requests.get(url, headers=headers)
    result = dict(response.json())['data']['Items']
    return result[0]['Id']


# 新建订单
def new_order(vip_info, sku_info):
    """
    vip_info:Vip信息，包含，vip_id 和vip_name,一般通过 new_vip 获取
    sku_info:商品信息列表，商品信息字典，如下
    sku_info = [
        {'SkuId': '7494440356323262567', 'Qty': '2'},
    ]
    return:order_info ，订单信息，包含订单id和订单编码
    格式： [order_id,order_code]
    """
    order = {
        "Id": "0",
        "Tid": "",
        "OrderType": 1,
        "DealDate": time.strftime('%Y-%m-%d %H:%M:%S'),
        "ShopId": "7494440439622140309",
        "VipId": vip_info[0],
        "VipName": vip_info[1],
        "ExpressId": "7494440373939341490",
        "PostFee": 0,
        "WarehouseId": "162573418911628622",
        "ProvinceName": "上海",
        "CityName": "上海市",
        "DistrictName": "闵行区",
        "ReceiverName": "芮苏云",
        "ReceiverPhone": "",
        "ReceiverMobile": "15221071395",
        "ReceiverRegionId": "0",
        "ReceiverZip": "",
        "ReceiverAddress": "衡东路189",
        "SellerMemo": "",
        "BuyerMemo": "",
        "Note": "",
        "SettlementMode": 0,
        "SalesManId": "0",
        "SalesManName": "",
        "SellerFlag": 0,
        "InvoiceTitle": "",
        "InvoiceNo": ""
    }
    headers = {
        'Cookie': base.cookies
    }
    url_param = ''
    for k, v in order.items():
        url_param += f"'{k}':'{v}',"
    url = "http://gw.erp12345.com/api/Orders/AllOrder/AddOrder?order={" + url_param + "}"
    response = requests.get(url, headers=headers, )
    result = dict(response.json())
    start = result['data']['OrderCodeTid'].find("T")
    end = len(result['data']['OrderCodeTid'])
    order_info = [result['data']['WaitApproveMaxId'], result['data']['OrderCodeTid'][start: end]]
    # 添加订单主体完成，下面需要添加商品信息
    url_param = ''
    for sku in sku_info:
        url_param += '{'
        for k, v in sku.items():
            url_param += f"'{k}':'{v}',"
        url_param += '},'
    url = "http://gw.erp12345.com/api/Orders/AllOrder/AddOrderLine?orderId=" + order_info[0] + "&skus=[" + url_param + "]"
    requests.get(url, headers=headers, )
    # 添加支付信息
    url = "http://gw.erp12345.com/api/Orders/AllOrder/FastAddOrderPayment?orderId=" + order_info[0] + ""
    requests.get(url, headers=headers)
    return order_info
