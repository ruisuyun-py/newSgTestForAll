import time
import requests
import page.base_page as base


# 新增会员
def new_vip(name):
    """
    name:会员名称，一般用get_now_string()生成
    return:{'data': {'Id': '7495034719080285576', 'VipId': '7495034719080285575',
    'Platform': 0, 'PlatformName': '0', 'ShopId': '0', 'ShopName': '测试门店1', 'VipLevelId': '0', 'VipCode':
    '20200731144129', 'VipName': '20200731144129', 'Email': None, 'IsPosVip': True, 'ShipName': '', 'ShipMobile': '',
    'ReceiverName': '芮苏云', 'ReceiverMobile': '15221071395', 'ReceiverPhone': '', 'ReceiverZip': '',
    'ReceiverAddress': '衡东路189', 'ReceiverRegionId': '0', 'IsIllegal': False, 'Balance': 0.0, 'Point': 0.0,
    'LevelName': None, 'Company': None, 'IsHide': False, 'Amount': 0.0, 'PayTypeName': None}, 'code': 1, 'message':
    None}
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
    return result


# 修改会员信息，目前只有等级
def modify_vip(vip_name, level_name):
    """
    vip_info:[会员id, 会员名称]，一般通过新建会员返回
    return:{'data': {'Id': '7495034716999911296', 'VipId': '7494440359611598114',
    'Platform': 0, 'PlatformName': '0', 'ShopId': '0', 'ShopName': '测试门店1', 'VipLevelId': '0', 'VipCode': '测试会员1',
    'VipName': '测试会员1', 'Email': '', 'IsPosVip': True, 'ShipName': '', 'ShipMobile': '', 'ReceiverName': '芮苏云',
    'ReceiverMobile': '15221071395', 'ReceiverPhone': '', 'ReceiverZip': '', 'ReceiverAddress': '衡东路189',
    'ReceiverRegionId': '0', 'IsIllegal': False, 'Balance': 0.0, 'Point': 0.0, 'LevelName': None, 'Company': None,
    'IsHide': False, 'Amount': 0.0, 'PayTypeName': None}, 'code': 1, 'message': None}
    """
    vip_info = get_vip_info(vip_name)
    vip_level_info = get_vip_level_info(level_name)
    headers = {
        'Cookie': base.cookies
    }
    vip = {
        'Id': 0,
        'VipId': vip_info["data"]["Items"][0]["VipId"],
        'Platform': vip_info["data"]["Items"][0]["Platform"],
        'ShopId': vip_info["data"]["Items"][0]["ShopId"],
        'IsPosVip': vip_info["data"]["Items"][0]["IsPosVip"],
        'VipLevelId': vip_level_info["data"]["Items"][0]["Id"],
        'VipLevelName': vip_level_info["data"]["Items"][0]["VipLevelName"],
        'VipName': vip_info["data"]["Items"][0]["VipName"],
        'VipCode': vip_info["data"]["Items"][0]["VipCode"],
        'ShipName': vip_info["data"]["Items"][0]["ShipName"],
        'ShipMobile': vip_info["data"]["Items"][0]["ShipMobile"],
        'ReceiverName': vip_info["data"]["Items"][0]["ReceiverName"],
        'ReceiverMobile': vip_info["data"]["Items"][0]["ReceiverMobile"],
        'ReceiverPhone': vip_info["data"]["Items"][0]["ReceiverPhone"],
        'ReceiverZip': vip_info["data"]["Items"][0]["ReceiverZip"],
        'ProvinceName': '上海',
        'CityName': '上海市',
        'DistrictName': '闵行区',
        'ReceiverAddress': vip_info["data"]["Items"][0]["ReceiverAddress"],
        'IsIllegal': vip_info["data"]["Items"][0]["IsIllegal"]
    }
    url_param = ''
    for k, v in vip.items():
        url_param += f"'{k}':'{v}',"
    url = "http://gw.erp12345.com/api/Vips/FullVip/SaveVip?vip={" + url_param + "}"
    response = requests.get(url, headers=headers, )
    result = dict(response.json())
    # print(result)
    return result


# 获取会员ID
def get_vip_info(name):
    """
    name:会员名称
    return:{'data': {'Items': [{'Id': '7495034562951513075', 'VipId': '7494440359611598114', 'Platform': 0,
    'PlatformName': '0', 'ShopId': '0', 'ShopName': None, 'VipLevelId': '7494730574376992769', 'VipCode': '测试会员1',
    'VipName': '测试会员1', 'Email': '', 'IsPosVip': True, 'ShipName': '', 'ShipMobile': '', 'ReceiverName': '芮苏云',
    'ReceiverMobile': '15221071395', 'ReceiverPhone': '', 'ReceiverZip': '', 'ReceiverAddress': '衡东路189',
    'ReceiverRegionId': '1234668550602865521', 'IsIllegal': False, 'Balance': 9900.0, 'Point': 0.0, 'LevelName':
    '固定减5-1', 'Company': '', 'IsHide': False, 'Amount': 3075300.0, 'PayTypeName': None}], 'TotalCount': 1},
    'code': 1, 'message': None}
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
    result = dict(response.json())
    # print(result)
    # vip_info = [result["data"]["Items"][0]["VipId"], result['data']["Items"][0]['VipName']]
    return result


# 获取会员等级信息
def get_vip_level_info(level_name):
    """
    level_name:等级名称
    return:{'data': {'Items': [{'Id': '7494745001692234941', 'VipLevelName': '8折', 'PriceType': 0,
    'Discount': 8.0, 'Amount1': 0.0, 'Amount1Discount': 0.0, 'Amount2': 0.0, 'Amount2Discount': 0.0, 'Amount3': 0.0,
    'Amount3Discount': 0.0, 'PriceTypeName': '标准售价'}], 'TotalCount': 1}, 'code': 1, 'message': None}
    """
    user_info = {
        'ModelTypeName': 'ErpWeb.Domain.ViewModels.Vips.VipLevelVmv',
        'VipLevelName': level_name,
    }
    url = "http://gw.erp12345.com/api/Vips/VipLevel/QueryPage?"
    for k, v in user_info.items():
        url += f"{k}={v}&"
    headers = {
        'Cookie': base.cookies
    }
    response = requests.get(url, headers=headers)
    result = dict(response.json())
    return result


# 新建商品
def new_product(product_code):
    """
    product_code:商品货号，一般通过get_now_string 获取
    return:{'data': {'Id': '7495034720204357633', 'Name': '20200731144235',
    'Code': '20200731144235', 'ProductCategoryId': '0', 'ShortName': '', 'BrandId': '0', 'Unit': '', 'PicUrl': '',
    'StandardPrice': 0.0, 'V': 0, 'ProductSkus': [{'Id': '7495034720204357634', 'Name': '红色 XS',
    'Code': '20200731144235-红色 XS', 'LastPurPrice': 0.0, 'StandardPrice': 0.0, 'Weight': 0.0, 'PackageWeight': 0.0,
    'BarCode': 'null', 'ValidityDate': '2020-07-31 14:42:35', 'SkuImg': 'null', 'IsHide': False, 'V': 0},
    {'Id': '7495034720204357635', 'Name': '红色 S', 'Code': '20200731144235-红色 S', 'LastPurPrice': 0.0,
    'StandardPrice': 0.0, 'Weight': 0.0, 'PackageWeight': 0.0, 'BarCode': 'null', 'ValidityDate': '2020-07-31
    14:42:35', 'SkuImg': 'null', 'IsHide': False, 'V': 0}, {'Id': '7495034720204357636', 'Name': '红色 M',
    'Code': '20200731144235-红色 M', 'LastPurPrice': 0.0, 'StandardPrice': 0.0, 'Weight': 0.0, 'PackageWeight': 0.0,
    'BarCode': 'null', 'ValidityDate': '2020-07-31 14:42:35', 'SkuImg': 'null', 'IsHide': False, 'V': 0},
    {'Id': '7495034720204357637', 'Name': '红色 L', 'Code': '20200731144235-红色 L', 'LastPurPrice': 0.0,
    'StandardPrice': 0.0, 'Weight': 0.0, 'PackageWeight': 0.0, 'BarCode': 'null', 'ValidityDate': '2020-07-31
    14:42:35', 'SkuImg': 'null', 'IsHide': False, 'V': 0}, {'Id': '7495034720204357638', 'Name': '红色 XL',
    'Code': '20200731144235-红色 XL', 'LastPurPrice': 0.0, 'StandardPrice': 0.0, 'Weight': 0.0, 'PackageWeight': 0.0,
    'BarCode': 'null', 'ValidityDate': '2020-07-31 14:42:35', 'SkuImg': 'null', 'IsHide': False, 'V': 0},
    {'Id': '7495034720204357639', 'Name': '红色 2XL', 'Code': '20200731144235-红色 2XL', 'LastPurPrice': 0.0,
    'StandardPrice': 0.0, 'Weight': 0.0, 'PackageWeight': 0.0, 'BarCode': 'null', 'ValidityDate': '2020-07-31
    14:42:35', 'SkuImg': 'null', 'IsHide': False, 'V': 0}, {'Id': '7495034720204357640', 'Name': '红色 3XL',
    'Code': '20200731144235-红色 3XL', 'LastPurPrice': 0.0, 'StandardPrice': 0.0, 'Weight': 0.0, 'PackageWeight': 0.0,
    'BarCode': 'null', 'ValidityDate': '2020-07-31 14:42:35', 'SkuImg': 'null', 'IsHide': False, 'V': 0}]},
    'code': 1, 'message': None}
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
    result = dict(response.json())
    return result


# 获取商家编码id
def get_sku_info(sku_code, product_code=''):
    """
    sku_code:需要查询的商家编码或者货号
    return:{'data': {'Items': [{'Id': '7494440356323262567', 'ProductId': '7494440356323262566',
    'PicUrl': '', 'ThumbnailUrl': '', 'SkuCode': '测试商品1-红色 XS', 'ProductCode': '测试商品1', 'ProductName': '测试商品1',
    'ProductShortName': '测试商品1', 'ProductCategoryId': '7494441867648435188', 'ProductCategory': '裤子', 'SupplierId':
    '7494553699939779471', 'SupplierName': '供应商3', 'BrandId': '7494556458986505405', 'BrandName': '阿迪达斯', 'Unit': '',
    'BarCode': '1907150011407', 'SkuName': '红色 XS', 'StandardPrice': 100.0, 'SecPrice': 200.0, 'ThirPrice': 300.0,
    'FourPrice': 400.0, 'Weight': 1.0, 'SalesPoint': 0.0, 'PackageWeight': 0.0, 'BoxSize': 30, 'SkuMemo': None,
    'FirstField': '红色', 'SecField': 'XS', 'ThirField': '106', 'FourField': '121', 'FifthField': '136',
    'FirstWarehouseId': '0', 'FirstWarehouseName': None, 'SyncType': 0, 'VirtualQty': 0, 'RealQty': 310,
    'RecordDate': '2019-06-17 13:55:08', 'RecordUserName': '系统管理员', 'ProductShopMappingQty': 0, 'LocalCode':
    'S-01-001-01-0002,D-01-001-01', 'IsHide': False, 'ValidityDate': None, 'PrintQty': 1, 'SyncTypeName': '不同步库存',
    'LastPurPrice': 10.0}], 'TotalCount': 1}, 'code': 1, 'message': None}
    """
    url_params = {
                'ModelTypeName': 'ErpWeb.Domain.ViewModels.Products.FullProductVmv',
                'SkuCode': sku_code,
                'ProductCode': product_code,
                'ishide': 'false',
            }
    url = "http://gw.erp12345.com/api/Products/FullProduct/QueryPage?"
    for k, v in url_params.items():
        url += f"{k}={v}&"
    headers = {
        'cookie': base.cookies
    }
    response = requests.get(url, headers=headers)
    result = dict(response.json())
    return result


# 修改商品价格方法
def modify_sku_price(sku_code, stand_price, second_price="", third_price="", fourth_price=""):
    """
    sku_code:商家编码
    stand_code:标准售价
    second_price:第二价格
    third_price：第三价格
    fourth_price：第四价格
    return:{'code': 1, 'message': None}
    """
    sku_info = get_sku_info(sku_code)
    url = "http://gw.erp12345.com/api/Products/FullProduct/BatchAllEditField?"
    url_param = {
        "proIds": sku_info["data"]["Items"][0]["ProductId"],
        "skuId": sku_info["data"]["Items"][0]["Id"],
        "selectSkuIds": sku_info["data"]["Items"][0]["Id"],
        "allType": 1,
        "editType": "2",
    }
    vm = {"StandardPrice": stand_price, "SecPrice": second_price, "ThirPrice": third_price, "FourPrice": fourth_price}
    editFields = {"StandardPrice": stand_price, "SecPrice": second_price, "ThirPrice": third_price,
                  "FourPrice": fourth_price}
    if second_price == "":
        vm.pop("SecPrice")
        editFields.pop("SecPrice")
    if third_price == "":
        vm.pop("ThirPrice")
        editFields.pop("ThirPrice")
    if fourth_price == "":
        vm.pop("FourPrice")
        editFields.pop("FourPrice")
    for k, v in url_param.items():
        url += f"{k}={v}&"
    url += "vm={"
    for k, v in vm.items():
        url += f"'{k}':'{v}',"
    url += "}&editFields={"
    for k, v in editFields.items():
        url += f"'{k}':'{v}',"
    url += "}"
    headers = {
        'cookie': base.cookies
    }
    response = requests.post(url, headers=headers)
    result = dict(response.json())
    # print(result)
    return result


# 新建订单
def new_order(vip_name, sku_info):
    """
    vip_name:会员名
    sku_info:商品信息列表，商品信息字典，如下
    sku_info = [
        {'SkuCode': '测试商品1-红色 XS', 'Qty': '2'},
    ]
    return:order_info ，订单信息，包含订单id和订单编码
    格式： [order_id,order_code]
    """
    vip_info = get_vip_info(vip_name)
    order = {
        "Id": "0",
        "Tid": "",
        "OrderType": 1,
        "DealDate": time.strftime('%Y-%m-%d %H:%M:%S'),
        "ShopId": "7494440439622140309",
        "VipId": vip_info["data"]["Items"][0]["VipId"],
        "VipName": vip_info["data"]["Items"][0]["VipName"],
        "ExpressId": "7494440373939341490",
        "PostFee": 0,
        "WarehouseId": "162573418911628622",
        "ProvinceName": "上海",
        "CityName": "上海市",
        "DistrictName": "闵行区",
        "ReceiverName": vip_info["data"]["Items"][0]["ReceiverName"],
        "ReceiverPhone": vip_info["data"]["Items"][0]["ReceiverPhone"],
        "ReceiverMobile": vip_info["data"]["Items"][0]["ReceiverMobile"],
        "ReceiverRegionId": vip_info["data"]["Items"][0]["ReceiverRegionId"],
        "ReceiverZip": vip_info["data"]["Items"][0]["ReceiverZip"],
        "ReceiverAddress": vip_info["data"]["Items"][0]["ReceiverAddress"],
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
        sku["SkuId"] = get_sku_info(sku["SkuCode"])["data"]["Items"][0]["Id"]
        sku.pop("SkuCode")
        url_param += '{'
        for k, v in sku.items():
            url_param += f"'{k}':'{v}',"
        url_param += '},'
    url = "http://gw.erp12345.com/api/Orders/AllOrder/AddOrderLine?orderId=" + order_info[
        0] + "&skus=[" + url_param + "]"
    requests.get(url, headers=headers, )
    # 添加支付信息
    url = "http://gw.erp12345.com/api/Orders/AllOrder/FastAddOrderPayment?orderId=" + order_info[0] + ""
    requests.get(url, headers=headers)
    return order_info


# 获取商品款号会员价格信息
def get_product_info_by_id(vip_name, sku_code):
    """
    vip_name:会员名称
    sku_code:商家编码
    return: {'data': [{'Id': '7494440356323262567', 'ProductId': '7494440356323262566',
    'ProductName': '测试商品1', 'ProductCode': '测试商品1', 'SkuCode': '测试商品1-红色 XS', 'SkuName': '红色 XS', 'Price': 100.0,
    'Weight': 1.0, 'PicUrl': '', 'Discount': 0.0, 'StandardPrice': 100.0, 'Storage': 'S-01-001-01-0002',
    'InvQty': 261, 'CostQty': 0, 'CanInvQty': -15489, 'Qty': 0, 'ThumbnailUrl': '', 'DescField': '测试商品1_红色 44'},
    {'Id': '7494440356323262568', 'ProductId': '7494440356323262566', 'ProductName': '测试商品1', 'ProductCode': '测试商品1',
    'SkuCode': '测试商品1-红色 S', 'SkuName': '红色 S', 'Price': 100.0, 'Weight': 1.0, 'PicUrl': '', 'Discount': 0.0,
    'StandardPrice': 100.0, 'Storage': 'S-01-001-01-0002', 'InvQty': 1967, 'CostQty': 0, 'CanInvQty': 1038, 'Qty': 0,
    'ThumbnailUrl': '', 'DescField': '测试商品1_红色 46'}, {'Id': '7494440356323262569', 'ProductId':
    '7494440356323262566', 'ProductName': '测试商品1', 'ProductCode': '测试商品1', 'SkuCode': '测试商品1-红色 M', 'SkuName': '红色
    M', 'Price': 100.0, 'Weight': 1.0, 'PicUrl': '', 'Discount': 0.0, 'StandardPrice': 100.0, 'Storage':
    'S-01-001-01-0003', 'InvQty': 930, 'CostQty': 0, 'CanInvQty': 329, 'Qty': 0, 'ThumbnailUrl': '', 'DescField':
    '测试商品1_红色 48'}, {'Id': '7494440356323262570', 'ProductId': '7494440356323262566', 'ProductName': '测试商品1',
    'ProductCode': '测试商品1', 'SkuCode': '测试商品1-红色 L', 'SkuName': '红色 L', 'Price': 100.0, 'Weight': 1.0, 'PicUrl': '',
    'Discount': 0.0, 'StandardPrice': 100.0, 'Storage': 'S-01-001-01-0004', 'InvQty': 3279, 'CostQty': 0,
    'CanInvQty': 2621, 'Qty': 0, 'ThumbnailUrl': '', 'DescField': '测试商品1_红色 50'}, {'Id': '7494440356323262571',
    'ProductId': '7494440356323262566', 'ProductName': '测试商品1', 'ProductCode': '测试商品1', 'SkuCode': '测试商品1-红色 XL',
    'SkuName': '红色 XL', 'Price': 100.0, 'Weight': 1.0, 'PicUrl': '', 'Discount': 0.0, 'StandardPrice': 100.0,
    'Storage': 'S-01-001-01-0005', 'InvQty': 6188, 'CostQty': 0, 'CanInvQty': 4411, 'Qty': 0, 'ThumbnailUrl': '',
    'DescField': '测试商品1_红色 52'}, {'Id': '7494440356323262572', 'ProductId': '7494440356323262566', 'ProductName':
    '测试商品1', 'ProductCode': '测试商品1', 'SkuCode': '测试商品1-红色 XXL', 'SkuName': '红色 XXL', 'Price': 100.0, 'Weight': 1.0,
    'PicUrl': '', 'Discount': 0.0, 'StandardPrice': 100.0, 'Storage': 'S-01-001-01-0005', 'InvQty': -181, 'CostQty':
    0, 'CanInvQty': -187, 'Qty': 0, 'ThumbnailUrl': '', 'DescField': '测试商品1_红色 55'}, {'Id': '7494440356323262573',
    'ProductId': '7494440356323262566', 'ProductName': '测试商品1', 'ProductCode': '测试商品1', 'SkuCode': '测试商品1-红色 XXXL',
    'SkuName': '红色 XXXL', 'Price': 100.0, 'Weight': 1.0, 'PicUrl': '', 'Discount': 0.0, 'StandardPrice': 100.0,
    'Storage': 'A-01-002-03', 'InvQty': -181, 'CostQty': 0, 'CanInvQty': -187, 'Qty': 0, 'ThumbnailUrl': '',
    'DescField': '测试商品1_红色 57'}, {'Id': '7494440356323262574', 'ProductId': '7494440356323262566', 'ProductName':
    '测试商品1', 'ProductCode': '测试商品1', 'SkuCode': '测试商品1-红色 XXXXL', 'SkuName': '红色 XXXXL', 'Price': 100.0,
    'Weight': 1.0, 'PicUrl': '', 'Discount': 0.0, 'StandardPrice': 100.0, 'Storage': 'A-01-002-03', 'InvQty': -181,
    'CostQty': 0, 'CanInvQty': -192, 'Qty': 0, 'ThumbnailUrl': '', 'DescField': '测试商品1_红色 59'},
    {'Id': '7494440356323262575', 'ProductId': '7494440356323262566', 'ProductName': '测试商品1', 'ProductCode': '测试商品1',
    'SkuCode': '测试商品1-红色 XXXXXL', 'SkuName': '红色 XXXXXL', 'Price': 100.0, 'Weight': 1.0, 'PicUrl': '', 'Discount':
    0.0, 'StandardPrice': 100.0, 'Storage': 'A-01-002-02', 'InvQty': -176, 'CostQty': 0, 'CanInvQty': -1170,
    'Qty': 0, 'ThumbnailUrl': '', 'DescField': '测试商品1_红色 61'}, {'Id': '7494440356323262576', 'ProductId':
    '7494440356323262566', 'ProductName': '测试商品1', 'ProductCode': '测试商品1', 'SkuCode': '测试商品1-红色 XXXXXXL', 'SkuName':
    '红色 XXXXXXL', 'Price': 100.0, 'Weight': 1.0, 'PicUrl': '', 'Discount': 0.0, 'StandardPrice': 100.0, 'Storage':
    'A-01-002-01', 'InvQty': -181, 'CostQty': 0, 'CanInvQty': -384, 'Qty': 0, 'ThumbnailUrl': '', 'DescField':
    '测试商品1_红色 63'}, {'Id': '7494440356323262577', 'ProductId': '7494440356323262566', 'ProductName': '测试商品1',
    'ProductCode': '测试商品1', 'SkuCode': '测试商品1-红色 2XL', 'SkuName': '红色 2XL', 'Price': 100.0, 'Weight': 1.0,
    'PicUrl': '', 'Discount': 0.0, 'StandardPrice': 100.0, 'Storage': 'S-01-001-01-0005', 'InvQty': 1019, 'CostQty':
    0, 'CanInvQty': 1013, 'Qty': 0, 'ThumbnailUrl': '', 'DescField': '测试商品1_红色 54'}, {'Id': '7494440356323262578',
    'ProductId': '7494440356323262566', 'ProductName': '测试商品1', 'ProductCode': '测试商品1', 'SkuCode': '测试商品1-红色 3XL',
    'SkuName': '红色 3XL', 'Price': 100.0, 'Weight': 1.0, 'PicUrl': '', 'Discount': 0.0, 'StandardPrice': 100.0,
    'Storage': 'A-01-002-02', 'InvQty': 1140, 'CostQty': 0, 'CanInvQty': 1134, 'Qty': 0, 'ThumbnailUrl': '',
    'DescField': '测试商品1_红色 56'}, {'Id': '7494440356323262579', 'ProductId': '7494440356323262566', 'ProductName':
    '测试商品1', 'ProductCode': '测试商品1', 'SkuCode': '测试商品1-红色 4XL', 'SkuName': '红色 4XL', 'Price': 100.0, 'Weight': 1.0,
    'PicUrl': '', 'Discount': 0.0, 'StandardPrice': 100.0, 'Storage': 'A-01-002-03', 'InvQty': -181, 'CostQty': 0,
    'CanInvQty': -187, 'Qty': 0, 'ThumbnailUrl': '', 'DescField': '测试商品1_红色 58'}, {'Id': '7494440356323262580',
    'ProductId': '7494440356323262566', 'ProductName': '测试商品1', 'ProductCode': '测试商品1', 'SkuCode': '测试商品1-红色 5XL',
    'SkuName': '红色 5XL', 'Price': 100.0, 'Weight': 1.0, 'PicUrl': '', 'Discount': 0.0, 'StandardPrice': 100.0,
    'Storage': 'A-01-002-02', 'InvQty': -82, 'CostQty': 0, 'CanInvQty': -104, 'Qty': 0, 'ThumbnailUrl': '',
    'DescField': '测试商品1_红色 60'}, {'Id': '7494440356323262581', 'ProductId': '7494440356323262566', 'ProductName':
    '测试商品1', 'ProductCode': '测试商品1', 'SkuCode': '测试商品1-红色 6XL', 'SkuName': '红色 6XL', 'Price': 100.0, 'Weight': 1.0,
    'PicUrl': '', 'Discount': 0.0, 'StandardPrice': 100.0, 'Storage': 'A-01-002-03', 'InvQty': 18417, 'CostQty': 0,
    'CanInvQty': 15619, 'Qty': 0, 'ThumbnailUrl': '', 'DescField': '测试商品1_红色 62'}], 'code': 1, 'message': None}

    """
    url = "http://gw.erp12345.com/api/Pos/Pos/GetProductInfoById?"
    sku_info = get_sku_info(sku_code)
    product_id = sku_info["data"]["Items"][0]["ProductId"]
    vip_info = get_vip_info(vip_name)
    vip_id = vip_info["data"]["Items"][0]["VipId"]
    url_params = {
        "productId": product_id,
        "isCombo": "false",
        "vipId": vip_id,
    }
    for k, v in url_params.items():
        url += f"{k}={v}&"
    headers = {
        'cookie': base.cookies
    }
    response = requests.post(url, headers=headers)
    result = dict(response.json())
    return result


# 在get_product_info_by_id基础上进一步优化，直接给出sku的会员价格
def get_sku_price_by_vip_id(vip_name, sku_code):
    """
    vip_name:会员名称
    sku_code:商家编码
    return：商品对饮的会员价格
    """
    vip_price = ''
    result = get_product_info_by_id(vip_name, sku_code)
    for sku_info in result["data"]:
        if sku_info["SkuCode"] == sku_code:
            vip_price = sku_info["Price"]
    return vip_price


# 门店开单
def new_pos_oder(vip_name, sku_info):
    """
    由于需要打开页面才能读取到NewId,所以必须使用try catch 包裹
    vip_name ：会员名称
    sku_info:商品信息列表，商品信息字典，如下
sku_info = [
        {'SkuCode': '测试商品1-红色 XS', 'Qty': '2', 'Price': "100"},
        {'SkuCode': '测试商品1-红色 S', 'Qty': '2', 'Price': "100"},
        {'SkuCode': '测试商品1-红色 M', 'Qty': '2', 'Price': "100"},
    ]
    """
    with base.operate_page("订单", "门店收银", "门店收银框架") as e:
        # 有BUG必须等5秒
        time.sleep(5)

        vip_info = get_vip_info(vip_name)
        js = " return model.NewId;"
        new_id = base.driver.execute_script(js)
        url = "http://gw.erp12345.com/api/Pos/Pos/SingleSettle?dto={"
        dto = {
            "VipId": vip_info["data"]["Items"][0]["VipId"],
            "ShopId": "7494440358269421036",
            "WarehouseId": "162573418911628622",
            "SalesManId": "7494505976142234005",
            "SalesManName": "测试",
            "ReceiverPhone": vip_info["data"]["Items"][0]["VipId"],
            "ReceiverMobile": vip_info["data"]["Items"][0]["VipId"],
            "ReceiverZip": vip_info["data"]["Items"][0]["VipId"],
            "ReceiverRegionId": vip_info["data"]["Items"][0]["VipId"],
            "ReceiverName": vip_info["data"]["Items"][0]["VipId"],
            "ReceiverAddress": vip_info["data"]["Items"][0]["VipId"],
            "SumQty": 2,
            "SumRefundQty": 0,
            "SumAmount": 200,
            "Memo": "",
            "PayType": "2341617839082309572",
            "PaidAmount": 200,
            "DiscountAmount": 0,
            "PlatformPayCode": "",
            "PayAccount": "",
            "OrderCode": "",
            "NewId": f"{new_id}"
        }
        for k, v in dto.items():
            url += f'"{k}":"{v}",'
        # 用于存储商品信息
        lines = []
        line = {}
        for sku in sku_info:
            sku_id = get_sku_info(sku["SkuCode"])["data"]["Items"][0]["Id"]
            line["Id"] = sku_id
            line["Qty"] = sku["Qty"]
            line["Price"] = sku["Price"]
            line["VipPrice"] = get_sku_price_by_vip_id(vip_name, sku["SkuCode"])
            actual_amount = int(line["Price"])*int(line["Qty"])
            line["ActualAmount"] = actual_amount
            discount = int(line["Price"])/int(line["VipPrice"])
            line["Discount"] = discount
            lines.append(line)
        url += "Lines:["
        for s in lines:
            url += "{"
            for k, v in s.items():
                url += f"'{k}':'{v}',"
            url += "},"
        url += "]}"
        headers = {
            'cookie': base.cookies
        }
        response = requests.post(url, headers=headers)
        result = dict(response.json())
        return result


# 保存订单设置
def save_order_setting(setting_info):
    """
    setting_inf0:需要修改的设置信息字典，
    格式：
    setting_info = {
        "只有手工修改售价才会记录预设价格": "false",
    }
    """
    setting = {
        "IsCheckInventory": "false",
        "InvLockType": 1,
        "IsScanWeight": "false",
        "IsScanDelivery": "false",
        "IsWeightDelivery": "false",
        "IsWeightTrans": "false",
        "IsDeliveryPackage": "false",
        "IsInterceptOrder": "false",
        "IsScanCheckOrder": "false",
        "IsTransCheckOrder": "false",
        "IsPickCheckOrder": "false",
        "IsAfterWeightDelivery": "true",
        "IsDeliveryTrans": "true",
        "IsScanAutoSubmit": "true",
        "IsScanAutoPrint": "false",
        "IsScanAutoDelivery": "true",
        "IsScanAutoPrintAndDelivery": "true",
        "PrintBeforPush": "true",
        "IsOrderTmc": "false",
        "SplitToDelivery": "true",
        "UploadExpressNoIntoMemo": "true",
        "BuyerMemoSplitSend": "true",
        "ComboProductBuyerMemoSplitSend": "true",
        "IsRecordVipSkuPrice": "true",
        "IsRecordVipProductPrice": "false",
        "DeliverySort": 0,
        "DeliveryPrintSort": 0,
        "SigleProductFirst": "true",
        "ProductSortType": 0,
        "MergeDupplicatSalesOrderLine": "true",
        "EnablePromotions": "true",
        "EnableGiftRules": "true",
        "IsNegativeCostAudit": "false",
        "PreventContinuousScan": "true",
        "NeedScanPackageBarCode": "false",
        "ModifyNotSyncToBill": "false",
        "IsServiceAutomaticAddGift": "false",
        "NotShowAssignTimeSalesOrder": 0,
        "IsMarkDeliveryModifyMemo": "false",
        "IsPdaWaveInkpadPrintSend": "true",
        "IsOnlyManuallyChangingRecordPriceService": "true"
    }
    for k, v in setting_info.items():
        if k == "记录会员上次交易价：手工单或者门店单保存时，记录会员的商品交易价格":
            setting["IsRecordVipSkuPrice"] = v
        elif k == "记录会员上次交易价 同款同价：手工单或者门店单保存时，记录会员的商品交易价格 同款同价":
            setting["IsRecordVipProductPrice"] = v
        elif k == "只有手工修改售价才会记录预设价格":
            setting["IsOnlyManuallyChangingRecordPriceService"] = v
    headers = {
        'Cookie': base.cookies
    }
    url_param = ''
    for k, v in setting.items():
        url_param += f"'{k}':'{v}',"
    url = "http://gw.erp12345.com/api/Settings/OrderSetting/SaveSetting?setting={" + url_param + "}"
    response = requests.get(url, headers=headers)
    print(response.status_code)
