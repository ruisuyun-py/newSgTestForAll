import os
import time
import requests
import page.base_page as base


def get_cookie():
    # 获取当前文件的目录
    cur_path = os.path.abspath(os.path.dirname(__file__))
    # 获取根目录
    root_path = cur_path[:cur_path.find("newSgTestForAll\\") + len("newSgTestForAll\\")]
    with open(root_path + "/page/cookie.txt", "r") as file:
        cookie = file.readline()
    return cookie


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


# 新建商品
def new_product(product_code):
    """
    product_code:商品货号，一般通过get_now_string 获取
    return:
    {'data':
        {
            'Id': '7495034720204357633', 'Name': '20200731144235',
            'Code': '20200731144235', 'ProductCategoryId': '0', 'ShortName': '', 'BrandId': '0', 'Unit': '', 'PicUrl': '',
            'StandardPrice': 0.0, 'V': 0,

            'ProductSkus':
                [
                    {'Id': '7495034720204357634', 'Name': '红色 XS',
                    'Code': '20200731144235-红色 XS', 'LastPurPrice': 0.0, 'StandardPrice': 0.0, 'Weight': 0.0, 'PackageWeight': 0.0,
                    'BarCode': 'null', 'ValidityDate': '2020-07-31 14:42:35', 'SkuImg': 'null', 'IsHide': False, 'V': 0},
                    {'Id': '7495034720204357635', 'Name': '红色 S', 'Code': '20200731144235-红色 S', 'LastPurPrice': 0.0,
                    'StandardPrice': 0.0, 'Weight': 0.0, 'PackageWeight': 0.0, 'BarCode': 'null', 'ValidityDate': '2020-07-31
                    14:42:35', 'SkuImg': 'null', 'IsHide': False, 'V': 0},
                ]
        },
    'code': 1,
    'message': None}
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
         "Weight": 0, "PackageWeight": 0, "BarCode": "", "ValidityDate": time.strftime('%Y-%m-%d %H:%M:%S'),
         "SkuImg": "null", "IsHide": "false", "V": 0},
        {"Id": "0", "Name": "红色 S", "Code": "" + product_code + "-红色 S", "LastPurPrice": 0, "StandardPrice": 0,
         "Weight": 0, "PackageWeight": 0, "BarCode": "", "ValidityDate": time.strftime('%Y-%m-%d %H:%M:%S'),
         "SkuImg": "null", "IsHide": "false", "V": 0},
        {"Id": "0", "Name": "红色 M", "Code": "" + product_code + "-红色 M", "LastPurPrice": 0, "StandardPrice": 0,
         "Weight": 0, "PackageWeight": 0, "BarCode": "", "ValidityDate": time.strftime('%Y-%m-%d %H:%M:%S'),
         "SkuImg": "null", "IsHide": "false", "V": 0},
        {"Id": "0", "Name": "红色 L", "Code": "" + product_code + "-红色 L", "LastPurPrice": 0, "StandardPrice": 0,
         "Weight": 0, "PackageWeight": 0, "BarCode": "", "ValidityDate": time.strftime('%Y-%m-%d %H:%M:%S'),
         "SkuImg": "null", "IsHide": "false", "V": 0},
        {"Id": "0", "Name": "红色 XL", "Code": "" + product_code + "-红色 XL", "LastPurPrice": 0, "StandardPrice": 0,
         "Weight": 0, "PackageWeight": 0, "BarCode": "", "ValidityDate": time.strftime('%Y-%m-%d %H:%M:%S'),
         "SkuImg": "null", "IsHide": "false", "V": 0},
        {"Id": "0", "Name": "红色 2XL", "Code": "" + product_code + "-红色 2XL", "LastPurPrice": 0, "StandardPrice": 0,
         "Weight": 0, "PackageWeight": 0, "BarCode": "", "ValidityDate": time.strftime('%Y-%m-%d %H:%M:%S'),
         "SkuImg": "null", "IsHide": "false", "V": 0},
        {"Id": "0", "Name": "红色 3XL", "Code": "" + product_code + "-红色 3XL", "LastPurPrice": 0, "StandardPrice": 0,
         "Weight": 0, "PackageWeight": 0, "BarCode": "", "ValidityDate": time.strftime('%Y-%m-%d %H:%M:%S'),
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
    sku_code:需要查询的商家编码
    product_code:货号
    return:{
    'data':
        {'Items':
            [
                {'Id': '7494440356323262567', 'ProductId': '7494440356323262566',
                'PicUrl': '', 'ThumbnailUrl': '', 'SkuCode': '测试商品1-红色 XS', 'ProductCode': '测试商品1', 'ProductName': '测试商品1',
                'ProductShortName': '测试商品1', 'ProductCategoryId': '7494441867648435188', 'ProductCategory': '裤子', 'SupplierId':
                '7494553699939779471', 'SupplierName': '供应商3', 'BrandId': '7494556458986505405', 'BrandName': '阿迪达斯', 'Unit': '',
                'BarCode': '1907150011407', 'SkuName': '红色 XS', 'StandardPrice': 100.0, 'SecPrice': 200.0, 'ThirPrice': 300.0,
                'FourPrice': 400.0, 'Weight': 1.0, 'SalesPoint': 0.0, 'PackageWeight': 0.0, 'BoxSize': 30, 'SkuMemo': None,
                'FirstField': '红色', 'SecField': 'XS', 'ThirField': '106', 'FourField': '121', 'FifthField': '136',
                'FirstWarehouseId': '0', 'FirstWarehouseName': None, 'SyncType': 0, 'VirtualQty': 0, 'RealQty': 310,
                'RecordDate': '2019-06-17 13:55:08', 'RecordUserName': '系统管理员', 'ProductShopMappingQty': 0, 'LocalCode':
                'S-01-001-01-0002,D-01-001-01', 'IsHide': False, 'ValidityDate': None, 'PrintQty': 1, 'SyncTypeName': '不同步库存',
                'LastPurPrice': 10.0}
            ],
            'TotalCount': 1},
     'code': 1,
     'message': None}
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


# 获取product_id
def get_product_id(product_code=''):
    """
    product_code:货号
    return: product_id
    """
    result = get_sku_info("", product_code)
    product_id = result["data"]["Items"][0]["ProductId"]
    return product_id


# 通过product_code或者sku_code获取sku_id
def get_sku_id(sku_code, product_code=''):
    """
    sku_code:需要查询的商家编码
    product_code:货号
    return:['sku_id','sku_id','sku_id','sku_id','sku_id','sku_id','sku_id','sku_id','sku_id',]
    """
    result = get_sku_info(sku_code, product_code)
    sku_id_list = []
    for info in result["data"]["Items"]:
        sku_id_list.append(int(info["Id"]))
    return sku_id_list


# 通过product_code或者sku_code获取bar_code
def get_sku_bar_code(sku_code, product_code=''):
    """
    sku_code:需要查询的商家编码
    product_code:货号
    return:['sku_barcode','sku_barcode','sku_barcode','sku_barcode',]
    """
    result = get_sku_info(sku_code, product_code)
    sku_barcode_list = []
    for info in result["data"]["Items"]:
        sku_barcode_list.append(info["BarCode"])
    return sku_barcode_list


# 通过product_code获取该款所有sku_code
def get_sku_code(product_code):
    """
    product_code:货号
    return:['sku_code','sku_code','sku_code','sku_code',]

    """
    result = get_sku_info("", product_code)
    sku_code_list = []
    for info in result["data"]["Items"]:
        sku_code_list.append(info["SkuCode"])
    return sku_code_list


# 生成商家编码
def new_create_sku_bar_code(sku_id_list):
    """
    主要功能是生成商品条码，返回值目前没什么用
    sku_id_list:['sku_id','sku_id',]
    return:
    {"data":[
                {"Id":"7495000258460516455","BarCode":"2008030040407","BarCode2":null,"BarCode3":null},
                {"Id":"7495000258460516457","BarCode":"2008160043477","BarCode2":null,"BarCode3":null}
            ],
    "code":1,
    "message":null}
    """
    url = "http://gw.erp12345.com/api/Products/FullProduct/NewCreateSkuBarCode?skuIds="
    for i in sku_id_list:
        url += f"{i},"
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
    return result


def get_bar_code_print_data(sku_code, qty):
    """
    sku_code:商家编码
    qty:数量
    return：
    {
    "data":
        {
        "id":"7494441895767049203","tenantId":"7494308563943163372","name":"唯一码15位",
            "data":
                [
                    { "Id":"7495000258460516455","ProductCode":"200707200742","AnalFullProductCode":null,
                    "ProductImage_ImageUrl":null,"ProductName":"200707200742-红色-L","ProductShortName":null,
                    "SkuCode":"200707200742-红色-L","SkuName":"红色-L","LocalCode":null,"LocalName":"","Qty":0,
                    "BarCode":"20080300404077","BarCode2BarCode":null,"BarCode3BarCode":null,"StandardPrice":100.0,"SecPrice":200.0,
                    "ThirPrice":300.0,"FourPrice":400.0,"LastPurPrice":0.0,"FirstField":null,"SecField":null,"ThirField":null,
                    "FourField":null,"FifthField":null,"SupplierName":null,"CategoryName":null,"BrandName":null,"SkuMemo":null,
                    "Unit":null,"CustomText":null,"PrintDate":"2020-08-20 22:29:54","SkuQty":0
                    }
                    { "Id":"7495000258460516455","ProductCode":"200707200742","AnalFullProductCode":null,
                    "ProductImage_ImageUrl":null,"ProductName":"200707200742-红色-L","ProductShortName":null,
                    "SkuCode":"200707200742-红色-L","SkuName":"红色-L","LocalCode":null,"LocalName":"","Qty":0,
                    "BarCode":"20080300404077","BarCode2BarCode":null,"BarCode3BarCode":null,"StandardPrice":100.0,"SecPrice":200.0,
                    "ThirPrice":300.0,"FourPrice":400.0,"LastPurPrice":0.0,"FirstField":null,"SecField":null,"ThirField":null,
                    "FourField":null,"FifthField":null,"SupplierName":null,"CategoryName":null,"BrandName":null,"SkuMemo":null,
                    "Unit":null,"CustomText":null,"PrintDate":"2020-08-20 22:29:54","SkuQty":0
                    }
                 ]
        },
    "code":1,
    "message":null
    }
    """
    sku_id = get_sku_id(sku_code)[0]
    url = "http://gw.erp12345.com/api/Products/FullProduct/GetBarCodePrintData?print={'PrintItems':[{"
    headers = {
        'cookie': base.cookies
    }
    url_params = {
        'SkuId': sku_id,
        'Qty': qty
    }
    for k, v in url_params.items():
        url += f"'{k}':'{v}',"
    url += "}],'TemplateId':'7494441895767049203','PrintName':'Microsoft XPS Document Writer'}"
    response = requests.get(url, headers=headers)
    result = dict(response.json())
    return result


def get_sku_unique_bar_code(sku_code, qty):
    result = get_bar_code_print_data(sku_code, qty)
    unique_bar_code_list = []
    for i in result["data"]["data"]:
        unique_bar_code_list.append(i["BarCode"])
    return unique_bar_code_list


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


# 获取订单信息
def get_order_info_by_fuzzy(fuzzy_keywords, required_information_list):
    """
    fuzzy_keywords:模糊搜索的关键字
    required_information_list：需要的信息名称,比如：[info_name1, info_name2, info_name3]
    return:[{"info_name1": "value", "info_name2": "value", "info_name3": "value",}]
    原始信息：
    {data: {Items: [{WaitApproveMaxId: "7495029146578322338",…}], TotalCount: 1}, code: 1, message: null}
    code: 1
        data: {Items: [{WaitApproveMaxId: "7495029146578322338",…}], TotalCount: 1}
            Items: [{WaitApproveMaxId: "7495029146578322338",…}]
                0: {WaitApproveMaxId: "7495029146578322338",…}
                    Approved: false
                    BuyerMemo: ""
                    Code: "TD200727007"
                    DeliveryCompleted: false
                    DispatchCompleted: false
                    EncriptReceiverMobile: "$176$CkuuVaTZ5CdQYgSEVM/phA==$1$"
                    EncriptReceiverName: "~xNPw4a7Nc5bLCphunyYZjQ==~1~"
                    EncriptReceiverPhone: null
                    ExceptionMessage: "其他ERP已发货"
                    ExceptionType: 1048576
                    ExpressId: "7494440373939341490"
                    ExpressName: "邮政小包电子面单"
                    ExpressNo: null
                    Id: "7495029146578322338"
                    ImBackGroundImgUrl: "https://amos.alicdn.com/online.aw?v=2&uid=t_1479214728795_0&site=cntaobao&s=2&charset=utf-8"
                    ImUrl: "https://amos.alicdn.com/getcid.aw?v=3&site=cntaobao&groupid=0&s=1&fromid=&uid=t_1479214728795_0&status=1&charset=utf-8"
                    InvoiceNo: null
                    InvoiceTitle: null
                    IsCod: false
                    IsEnd: false
                    LackType: 4
                    Note: "{来源:WAP,WAP}"
                    OrderCodeTid: "1146084768821949721<br/>[全缺]TD200727007"
                    OrderCount: 4
                    OrderStatus: "其他ERP已发货"
                    OrderTypeName: "销售订单"
                    PayDate: "2020-07-27 18:24:55"
                    PayDays: 29
                    Platform: 1
                    PostFee: 0
                    ProHtml: "<span class="good-box"><span class="label">1</span><img src="https://img.alicdn.com/bao/uploaded/i2/2462224143/O1CN01Bpi9Ny1gTXTt4cGoS_!!2462224143.jpg_30x30.jpg" title="07080932-黑 43-46 43-46" /></span><span class="good-box"><span class="label">1</span><img src="https://img.alicdn.com/bao/uploaded/i2/2462224143/O1CN01Bpi9Ny1gTXTt4cGoS_!!2462224143.jpg_30x30.jpg" title="07080932-蓝 35-38 35-38" /></span><span class="good-box"><span class="label">1</span><img src="https://img.alicdn.com/bao/uploaded/i2/2462224143/O1CN01Bpi9Ny1gTXTt4cGoS_!!2462224143.jpg_30x30.jpg" title="07080932-红 31-34 31-34" /></span>"
                    ProList: [{Id: "7495029146578322338",…}, {Id: "7495029146578322338",…}, {Id: "7495029146578322338",…}]
                    ReceiverAddress: "上海 上海市 闵行区 浦江镇永杰路439弄永康城浦晨雅苑1号楼401"
                    ReceiverMobile: "17673647529"
                    ReceiverName: "郭习浪"
                    ReceiverPhone: null
                    ReceiverRegionId: "1234668550602865521"
                    RecordDate: "2020-07-27 18:25:48"
                    SellerFlag: 1
                    SellerMemo: "天下无敌  建单人：售后专用 - 建单时间：07/28 - 物流单号：568888544 -天下无敌共退1件;(货品信息:【07080932-蓝 35-蓝色 35—38*1】)|2020-07-28 17:12:48退货退款-ERP对接入仓自动退（淘宝）.195307080932-蓝 35-381.00  建单人：售后专用 - 建单时间：07/28 - 物流单号：568888544 -天下无敌共退1件;(货品信息:【07080932-蓝 35-蓝色 35—38*1】);共换1件(货品信息:【07080932-蓝 X-蓝色 XL*1】) （收）07080932-蓝 35-蓝色 3538*1（换）07080932-蓝 X-蓝色 XL*1"
                    ShopId: "7494677199308457149"
                    ShopName: "巨淘气"
                    SortKey: "1_[07080932-黑 43-46 43-46][07080932-红 31-34 31-34][07080932-蓝 35-38 35-38]"
                    SourceType: 1
                    StatusType: 4
                    SumAmount: 3
                    SumDeliveriedQty: 0
                    SumDiscountAmount: 0
                    SumDispatchedQty: 0
                    SumQty: 3
                    Tid: "1146084768821949721"
                    TradeOnlineUrl: "https://trade.taobao.com/trade/detail/trade_item_detail.htm?bizOrderId=1146084768821949721"
                    TradeStatus: 8
                    Type: 1
                    UnPaidAmount: 0
                    VipName: "t_1479214728795_0"
                    WaitApproveMaxId: "7495029146578322338"
                    WarehouseId: "162573418911628622"
                    WarehouseName: "主仓库"
                    Weight: 0
        TotalCount: 1
    message: null
    """
    url_params = {
        "Fuzzy": fuzzy_keywords,
        'ModelTypeName': 'ErpWeb.Domain.ViewModels.Orders.AllOrderVmv',
    }
    url = "http://gw.erp12345.com/api/Orders/AllOrder/QueryPage?"
    for k, v in url_params.items():
        url += f"{k}={v}&"
    headers = {
        'Cookie': base.cookies
    }
    response = requests.get(url, headers=headers)
    result = dict(response.json())
    information_mapping = {
        "是否审核": "Approved",
        "买家备注": "BuyerMemo",
        "订单编码": "Code",
        "是否发货": "DeliveryCompleted",
        "是否配货完成": "DispatchCompleted",
        "加密收货人电话": "EncriptReceiverMobile",
        "加密收货人姓名": "EncriptReceiverName",
        "加密收货人手机": "EncriptReceiverPhone",
        "异常消息": "ExceptionMessage",
        "快递": "ExpressName",
        "快递单号": "ExpressNo",
        "ID": "Id",
        "发票编号": "InvoiceNo",
        "发票抬头": "InvoiceTitle",
        "是否锁定": "IsCod",
        "是否终结": "IsEnd",
        "便签": "Note",
        "订单数": "OrderCount",
        "订单状态": "OrderStatus",
        "订单类型": "OrderTypeName",
        "付款时间": "PayDate",
        "付款天数": "PayDays",
        "运费": "PostFee",
        "商品信息": "ProList",
        "收货地址": "ReceiverAddress",
        "电话": "ReceiverMobile",
        "收货人": "ReceiverName",
        "手机": "ReceiverPhone",
        "创建时间": "RecordDate",
        "旗帜": "SellerFlag",
        "卖家备注": "SellerMemo",
        "店铺": "ShopName",
        "总金额": "SumAmount",
        "总发货数": "SumDeliveriedQty",
        "总优惠金额": "SumDiscountAmount",
        "总未配货数": "SumDispatchedQty",
        "商品数量": "SumQty",
        "平台单号": "Tid",
        "未付金额": "UnPaidAmount",
        "会员名": "VipName",
        "仓库": "WarehouseName",
        "重量": "Weight",
    }
    information_list = []
    for k in result["data"]["Items"]:
        info_dict = {}
        for i in required_information_list:
            info_code = information_mapping[i]
            info_dict[i] = k[info_code]
        information_list.append(info_dict)
    return information_list


# 获取订单的商品明细详情
def get_order_product_detail(order_id, required_information_list):
    """
    order_id:该订单的id
    required_information_list:比如：["商家编码", "商品名称", "规格名称", "平台商家编码", "平台规格名称", "平台商品ID", ]
    return:[{"商家编码":"value", "": "", "": "", "": "", "": "", "": "", "": "",},.....]
    原始数据
    {data: {SumQty: 3, ProductAmount: 3, ExceptionItems: [],…}, code: 1, message: null}
    code: 1
        data: {SumQty: 3, ProductAmount: 3, ExceptionItems: [], Lines: [],…}
            ExceptionItems: []
                Lines: [{Id: "7495029146578322340", ProductId: "7495033536907314668", SkuId: "7495003057839669914",…},…]
                    0: {Id: "7495029146578322340", ProductId: "7495033536907314668", SkuId: "7495003057839669914",…}
                    1: {Id: "7495029146578322341", ProductId: "7495033536907314668", SkuId: "7495003057822892485",…}
                    2: {Id: "7495029146578322342", ProductId: "7495033536907314668", SkuId: "7495003057806115286",…}
                        Amount: 1
                        CanDispatchQty: -6
                        ComboQty: 0
                        DeliveriedQty: 0
                        DeliveryCompleted: false
                        DispatchedQty: 0
                        ExceptionTypeMessage: null
                        HeaderId: "0"
                        Id: "7495029146578322342"
                        IsCombo: false
                        IsGift: false
                        Oid: "1146084768824949721"
                        OnlineStatus: "交易完成"
                        OnlineUrl: "https://item.taobao.com/item.htm?id=610510713972"
                        OriginPrice: 1
                        PicUrl: "https://img.alicdn.com/bao/uploaded/i2/2462224143/O1CN01Bpi9Ny1gTXTt4cGoS_!!2462224143.jpg"
                        PlatProductCode: "200615192123"
                        PlatProductId: "610510713972"
                        PlatProductName: "测试专用 勿拍，不发货"
                        PlatSkuCode: "07080932-红 31-34"
                        PlatSkuId: "4555424594867"
                        PlatSkuName: "红色 31-34"
                        ProductCategoryId: "0"
                        ProductCode: "07080932"
                        ProductId: "7495033536907314668"
                        ProductName: "07080932"
                        Qty: 1
                        SkuCode: "07080932-红 31-34 31-34"
                        SkuId: "7495003057806115286"
                        SkuName: "红色 31-34"
                        SkuWeight: 0
                        SupplierId: "0"
                        ThumbnailUrl: "https://img.alicdn.com/bao/uploaded/i2/2462224143/O1CN01Bpi9Ny1gTXTt4cGoS_!!2462224143.jpg_30x30.jpg"
                        Tid: null
            ProductAmount: 3
            SumQty: 3
    message: null
    """
    url_params = {
        "orderId": order_id,
    }
    url = "http://gw.erp12345.com/api/Orders/AllOrder/GetOrderLines?"
    for k, v in url_params.items():
        url += f"{k}={v}&"
    headers = {
        'Cookie': base.cookies
    }
    response = requests.get(url, headers=headers)
    result = dict(response.json())
    information_mapping = {
        "总金额": "Amount",
        "可配货库存": "CanDispatchQty",
        "配货数量": "DispatchedQty",
        "是否套餐": "IsCombo",
        "是否赠品": "IsGift",
        "平台单号": "Oid",
        "线上状态": "OnlineStatus",
        "原始单价": "OriginPrice",
        "平台货号": "PlatProductCode",
        "平台商品ID": "PlatProductId",
        "平台商品名称": "PlatProductName",
        "平台商家编码": "PlatSkuCode",
        "平台规格ID": "PlatSkuId",
        "平台规格名称": "PlatSkuName",
        "货号": "ProductCode",
        "商品名称": "ProductName",
        "数量": "Qty",
        "商家编码": "SkuCode",
        "商品ID": "SkuId",
        "规格名称": "SkuName",
        "商品重量": "SkuWeight",
        "供应商ID": "SupplierId",
    }
    information_list = []
    for k in result["data"]["Lines"]:
        info_dict = {}
        for i in required_information_list:
            info_code = information_mapping[i]
            info_dict[i] = k[info_code]
        information_list.append(info_dict)
    return information_list


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
    product_id = get_product_id(product_code)
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
            actual_amount = int(line["Price"]) * int(line["Qty"])
            line["ActualAmount"] = actual_amount
            discount = int(line["Price"]) / int(line["VipPrice"])
            line["Discount"] = discount
            lines.append(dict(line))
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


# 保存基础业务
def save_base_setting(setting_info):
    setting = {
        "LockToOperate": "false",
        "RecordOrderChangeDetail": "false",
        "EnableLackOfInventery": "true",
        "UseWarehousePurPrice": "true",
        "FlagMemoSyncPlatform": "true",
        "IsDeliveryReduceVirtualQty": "true",
        "EnableSubScribeBill": "false",
        "IsModifyProductInfUpdateHistoryData": "true",
        "SerivceOrderMismatchPromotion": "false",
        "ReDownloadProWhenMatchFaild": "false",
        "CommodityManagementShopPermissions": "false",
        "IntensityFinanceModel": "false",
        "CreateComboIfProductNotExistCreateProduct": "true",
        "AnalyticalPackageAutomaticAdditionSize": "true",
        "CreateProCodeByAnalProCode": "true",
        "FilterPrice": "false", "LockNewPurPrice": "false",
        "PrintUniqueBarCode": "true",
        "PrintBoxBarCode": "false",
        "FastQuerySkuType": 1,
        "BarCodeCreateRule": 3,
        "SkuInterval": 0,
        "MatchProductByBarCode": "true",
        "ProductMappingType": 3,
        "ProductMappingKeyWords": "",
        "NextProductMappingType": 0,
        "IsModifyProductNoCreateCode": "true",
        "PlatformSkuCodeFilterFlag": "/.",
        "IsOpenFineInventory": "false",
        "OpenBackgroundSendService": "false",
        "OpenBatchDeliverySend": "false",
        "IsDetectionSingleTallying": "false",
        "IsModifySkuBreakMapping": "false",
        "IsCustomerBillOrderShop": "false"
    }
    for k, v in setting_info.items():
        if k == "启用条码唯一码":
            setting["PrintUniqueBarCode"] = v
    headers = {
        'Cookie': base.cookies
    }
    url_param = ''
    for k, v in setting.items():
        url_param += f"'{k}':'{v}',"
    url = "http://gw.erp12345.com/api/Settings/BillSetting/savesetting?setting={" + url_param + "}"
    response = requests.get(url, headers=headers)


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


def get_delivery_order_info():
    """
    return:
    {"data":
        { "Items":
            [
                {"Id":"7495067250655756700","OrderType":8,"OrderTypeName":"[门店]",
                "WarehouseName":"主仓库","ExpressName":"买家自提","Code":"DO200823007","ExpressNo":"DO200823007","PlatCode":null,
                "ProductQuantity":2,"PickCount":0,"PayDate":"2020-08-23 01:18:43","ExpressPrintDate":"2020-08-23 01:18:44",
                "DeliverySendDate":"2020-08-23 01:18:44","TranStatusModifyDate":null,"ScanDate":null,"IsPlatDelivery":false,
                "IsPrintExpress":true,"IsWeight":false,"IsScan":false,"IsTrans":false,"IsSplit":false,"ShopName":"测试门店1",
                "VipName":"20200823011805","Note":null,"ConsigneeName":"7495067250018222081","Weight":0.0,"WeightQty":0.0,
                "SumAmount":200.0,"ConsigneeAdress":"7495067250018222081","DeliverySendUser":"测试","ScanUser":null,
                "WeightUser":null,"PackageUser":null,"PlatDeliveryDate":null,"TranStatusName":"未知状态","ExpressCost":0.0,
                "BatchCode":null,"PackageMemo":null,"Platform":0,"EncriptReceiverMobile":null,"EncriptReceiverPhone":null,
                "EncriptReceiverName":null},
            ]
        ,"TotalCount":2393
        },
    "code":1,
    "message":null
    }
    """
    user_info = {
        'ModelTypeName': 'ErpWeb.Domain.ViewModels.Deliverys.DeliveryOrderQueryVmv',
    }
    url = "http://gw.erp12345.com/api/Deliverys/DeliveryOrderQuery/QueryPage?"
    for k, v in user_info.items():
        url += f"{k}={v}&"
    headers = {
        'Cookie': base.cookies
    }
    response = requests.get(url, headers=headers)
    result = dict(response.json())
    return result


# 获取发货单特定列的值对照表
def get_delivery_order_column_value(key_column, value_column):
    name_code_map = {
        "物流单号": "ExpressNo",
        "会员名称": "VipName",
    }
    result = get_delivery_order_info()
    column_info = {}
    for i in result["data"]["Items"]:
        key = i[name_code_map[key_column]]
        value = i[name_code_map[value_column]]
        column_info[key] = value
    return column_info


