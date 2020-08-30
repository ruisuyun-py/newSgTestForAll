import time
import requests
import page.base_page as base
import interface.product.product_interface as product_interface


# 新增会员
def new_vip(name):
    """
    name:会员名称，一般用get_now_string()生成
    return:
    {'data':
        {
            'Id': '7495034719080285576', 'VipId': '7495034719080285575',
            'Platform': 0, 'PlatformName': '0', 'ShopId': '0', 'ShopName': '测试门店1', 'VipLevelId': '0', 'VipCode':
            '20200731144129', 'VipName': '20200731144129', 'Email': None, 'IsPosVip': True, 'ShipName': '',
            'ShipMobile': '','ReceiverName': '芮苏云', 'ReceiverMobile': '15221071395', 'ReceiverPhone': '',
            'ReceiverZip': '',
            'ReceiverAddress': '衡东路189', 'ReceiverRegionId': '0', 'IsIllegal': False, 'Balance': 0.0, 'Point': 0.0,
            'LevelName': None, 'Company': None, 'IsHide': False, 'Amount': 0.0, 'PayTypeName': None
        },
    'code': 1,
    'message':
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
    return:
    {'data':
        {
            'Id': '7495034716999911296', 'VipId': '7494440359611598114',
            'Platform': 0, 'PlatformName': '0', 'ShopId': '0', 'ShopName': '测试门店1', 'VipLevelId': '0', 'VipCode': '测试会员1',
            'VipName': '测试会员1', 'Email': '', 'IsPosVip': True, 'ShipName': '', 'ShipMobile': '', 'ReceiverName': '芮苏云',
            'ReceiverMobile': '15221071395', 'ReceiverPhone': '', 'ReceiverZip': '', 'ReceiverAddress': '衡东路189',
            'ReceiverRegionId': '0', 'IsIllegal': False, 'Balance': 0.0, 'Point': 0.0, 'LevelName': None, 'Company': None,
            'IsHide': False, 'Amount': 0.0, 'PayTypeName': None
        },
    'code': 1,
    'message': None}
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
    return result


# 修改会员等级
def modify_vip_level(vip_name, level_name):
    result = modify_vip(vip_name, level_name)
    return result


# 获取会员ID
def get_vip_info(name):
    """
    name:会员名称
    return:
    {'data':
    {'Items':
        [
            {'Id': '7495034562951513075', 'VipId': '7494440359611598114', 'Platform': 0,
            'PlatformName': '0', 'ShopId': '0', 'ShopName': None, 'VipLevelId': '7494730574376992769', 'VipCode': '测试会员1',
            'VipName': '测试会员1', 'Email': '', 'IsPosVip': True, 'ShipName': '', 'ShipMobile': '', 'ReceiverName': '芮苏云',
            'ReceiverMobile': '15221071395', 'ReceiverPhone': '', 'ReceiverZip': '', 'ReceiverAddress': '衡东路189',
            'ReceiverRegionId': '1234668550602865521', 'IsIllegal': False, 'Balance': 9900.0, 'Point': 0.0, 'LevelName':
            '固定减5-1', 'Company': '', 'IsHide': False, 'Amount': 3075300.0, 'PayTypeName': None}
        ],
    'TotalCount': 1},
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
    return result


# 获取vip_id
def get_vip_id(name):
    result = get_vip_info(name)
    vip_id = result["data"]["Items"][0]["VipId"]
    return vip_id


# 获取会员等级信息
def get_vip_level_info(level_name):
    """
    level_name:等级名称
    return:
    {'data':
        {'Items':
            [
                {'Id': '7494745001692234941', 'VipLevelName': '8折', 'PriceType': 0,
                'Discount': 8.0, 'Amount1': 0.0, 'Amount1Discount': 0.0, 'Amount2': 0.0, 'Amount2Discount': 0.0, 'Amount3': 0.0,
                'Amount3Discount': 0.0, 'PriceTypeName': '标准售价'}
            ],
         'TotalCount': 1},
     'code': 1,
     'message': None}
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


# 修改预设会员价
def modify_preset_price(vip_name, product_code, old_price, price):
    """
    vipname:会员名称
    product_code:款号
    old_price:老价格，也就是原价
    price:需要修改成的价格
    return {"code":1,"message":null}
    """
    url = "http://gw.erp12345.com/api/Vips/VipPresupposePrice/NewModifyProductPrice?"
    vip_id = get_vip_id(vip_name)
    product_id = product_interface.get_product_id(product_code)
    url_params = {
        "vipId": vip_id,
        "productId": product_id,
        "price": price,
        "oldPrice": old_price,
    }
    for k, v in url_params.items():
        url += f"{k}={v}&"
    headers = {
        'cookie': base.cookies
    }
    response = requests.get(url, headers=headers)
    result = dict(response.json())
    return result


# 获取商品款号会员价格信息
def get_product_info_by_vip_id(vip_name, sku_code):
    """
    vip_name:会员名称
    sku_code:商家编码
    return:
    {
    'data':
        [
            {'Id': '7494440356323262581', 'ProductId': '7494440356323262566', 'ProductName':
            '测试商品1', 'ProductCode': '测试商品1', 'SkuCode': '测试商品1-红色 6XL', 'SkuName': '红色 6XL', 'Price': 100.0,
            'Weight': 1.0,
            'PicUrl': '', 'Discount': 0.0, 'StandardPrice': 100.0, 'Storage': 'A-01-002-03', 'InvQty': 18417, 'CostQty': 0,
            'CanInvQty': 15619, 'Qty': 0, 'ThumbnailUrl': '', 'DescField': '测试商品1_红色 62'}
        ],
    'code': 1,
    'message': None
    }
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
    return：商品的会员价格
    """
    vip_price = ''
    result = get_product_info_by_vip_id(vip_name, sku_code)
    for sku_info in result["data"]:
        if sku_info["SkuCode"] == sku_code:
            vip_price = sku_info["Price"]
    return vip_price