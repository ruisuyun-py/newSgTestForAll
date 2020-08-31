import time
import requests
import page.base_page as base
import interface.supplier.supplier_interface as supplier_interface


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


# 批量修改
def multi_modify_sku_info(sku_id_list, modify_info_dict):
    """
    sku_code_lsit:["测试商品1-红色 XS", "测试商品1-红色 XS", "测试商品1-红色 S", "测试商品1-红色 M", "测试商品1-红色 L", ]
    modify_info_dict:{"商品简称":"奖惩", "商品分类":"上衣", "供应商":"供应商1", "品牌":"阿迪达斯", "标准售价":"1", }
    """
    sku_ids = ""
    for i in sku_id_list:
        sku_ids += str(i)
        sku_ids += ","
    print(f"sku_ids={sku_ids}")
    modify_info_mapping = {
        "商品简称": "ProductShortName",
        "商品分类ID": "ProductCategoryId",
        # TODO:(RUI) 获取商品分类ID方法
        "品牌ID": "BrandId",
        # TODO:(RUI) 获取品牌ID 方法
        "单位": "Unit",
        "标准售价": "StandardPrice",
        "最新进价": "LastPurPrice",
        "重量": "Weight",
        "箱规": "BoxSize",
        "库存同步类型": "SyncType",
        "虚拟库存数": "VirtualQty",
        "包装重量": "PackageWeight",
        "优先出库仓": "FirstWarehouseId",
        "供应商ID": "SupplierId",
        "积分": "SalesPoint",
        "库存预警值": "WarningQty",
        "扩展字段1": "FirstField",
        "扩展字段2": "SecField",
        "扩展字段3": "ThirField",
        "扩展字段4": "FourField",
        "扩展字段5": "FifthField",
        "长": "SkuLength",
        "宽": "SkuWidth",
        "高": "SkuHeight",
        "周长": "PackingPerimeter",
        "规格便签": "SkuMemo",
    }
    url = "http://gw.erp12345.com/api/Products/FullProduct/BatchUpdateProduct?model={"
    params = {}
    for k, v in modify_info_dict.items():
        if k == "供应商ID":
            supplier_id = supplier_interface.get_supplier_info(v, ["供应商ID"])["供应商ID"]
            params[modify_info_mapping[k]] = supplier_id
        elif k in ["商品分类ID", "品牌ID"]:
            assert 1 == 2, "商品分类和品牌获取ID方法需要完善"
        else:
            params[modify_info_mapping[k]] = v
    print(f"params={params}")
    for k, v in params.items():
        url += f"'{k}':'{v}',"
    url += "}&ids="
    url += sku_ids
    headers = {
        'cookie': base.cookies
    }
    response = requests.get(url, headers=headers)
    print(response.json())
