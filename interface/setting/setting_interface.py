import time
import random
import requests
import page.base_page as base
import interface.inventory.inventory_interface as inventory_interface


# 保存基础业务
def save_base_setting(setting_info):
    """
    setting_info:{"允许负库存": "false",}
    """
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
        elif k == '允许负库存':
            setting["EnableLackOfInventery"] = v
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


def save_auto_merge_setting(setting_info):
    """
    setting_info:{"店铺相同": "false",}
    """
    setting = {
        "Enable": "false",
        "SameShop": "false",
        "SameVip": "false",
        "SameReceiver": "true",
        "SameExpress": "false",
        "SameWarehouse": "false",
        "NotMergeRefundOrder": "false",
        "NotMergeDispatchedOrder": "false",
        "MergeMemoWithoutTid": "false",
    }
    for k, v in setting_info.items():
        if k == "开启":
            setting["Enable"] = v
        elif k == '店铺相同':
            setting["SameShop"] = v
        elif k == '会员相同':
            setting["SameVip"] = v
        elif k == '相同收货人、手机、地址':
            setting["SameReceiver"] = v
        elif k == '仓库相同':
            setting["SameWarehouse"] = v
        elif k == '快递相同':
            setting["SameExpress"] = v
        elif k == '不合并有退款订单':
            setting["NotMergeRefundOrder"] = v
        elif k == '不合并已配货订单':
            setting["NotMergeDispatchedOrder"] = v
        elif k == '合并买家/卖家备注不加平台单号':
            setting["MergeMemoWithoutTid"] = v
    headers = {
        'Cookie': base.cookies
    }
    url = "http://gw.erp12345.com/api/Settings/TradeMergeSetting/savesetting?setting={"
    for k, v in setting.items():
        url += f"'{k}':'{v}',"
    url += "}"
    response = requests.get(url, headers=headers)


# 获取快递ID
def get_express_info(warehouse_name, express_name):
    """
    warehouse_name:仓库名称
    express_name:快递名称
    return:express_id
    """
    """
    {"data":[
        {"Code":"POSTB","TmsExpressId":"3413544150343193823","Name":"邮政小包电子面单（拼多多）","IsDisable":false,"PrintTempletId":"7494440374308438523","WayBillConfigId":"7494440377512888705","CodType":1,"IsWayBill":true,"Id":"7494446596608753867","HasSetting":true},
        {"Code":"POSTB","TmsExpressId":"3413544150343193823","Name":"邮政小包电子面单","IsDisable":false,"PrintTempletId":"0","WayBillConfigId":"7494805874565711749","CodType":1,"IsWayBill":true,"Id":"7494440373939341490","HasSetting":true},
        {"Code":"SF","TmsExpressId":"1385921083136794008","Name":"顺丰速运电子面单","IsDisable":false,"PrintTempletId":"7494440374308438523","WayBillConfigId":"7494805874565711749","CodType":1,"IsWayBill":true,"Id":"7494806984277886040","HasSetting":true},
        {"Code":"HTKY","TmsExpressId":"1220813892426788076","Name":"不设置运费计算规则","IsDisable":false,"PrintTempletId":"7494440374308438523","WayBillConfigId":"7494805874565711749","CodType":1,"IsWayBill":true,"Id":"7494805888910230111","HasSetting":false},
        {"Code":"HTKY","TmsExpressId":"1220813892426788076","Name":"百世汇通电子面单","IsDisable":false,"PrintTempletId":"7494440374308438523","WayBillConfigId":"7494440377512888697","CodType":1,"IsWayBill":true,"Id":"7494505992315469926","HasSetting":false},
        {"Code":"EMS","TmsExpressId":"2186415495986999893","Name":"EMS","IsDisable":false,"PrintTempletId":"7494440374308438523","WayBillConfigId":"7494886860653593385","CodType":1,"IsWayBill":true,"Id":"7494505997868728927","HasSetting":false},
        {"Code":"OFFLINE","TmsExpressId":"1983430599389482375","Name":"买家自提","IsDisable":false,"PrintTempletId":"7494440374308438523","WayBillConfigId":null,"CodType":1,"IsWayBill":false,"Id":"7494515725952877959","HasSetting":false}
        ],
    "code":1,
    "message":null
    }
    """
    url = "http://gw.erp12345.com/api/Basics/WarehouseExpress/GetExpressList?"
    headers = {
        'cookie': base.cookies
    }
    url_params = {
        'isDisable': 'false',
        'warehouseId': inventory_interface.get_inventory_id(warehouse_name)
    }
    for k, v in url_params.items():
        url += f"'{k}'='{v}',"
    response = requests.get(url, headers=headers)
    result = dict(response.json())
    express_info_list = []
    for i in result["data"]:
        express_info = {}
        for k, v in i.items():
            if k == "Id":
                express_info["快递ID"] = v
            elif k == "Name":
                express_info["快递名称"] = v
        express_info_list.append(express_info)
    # print(f"快递信息列表：{express_info_list}")
    return express_info_list


# 获取快递ID
def get_express_id(warehouse_name, express_name):
    express_info = get_express_info(warehouse_name, express_name)
    express_id = ""
    for i in express_info:
        if i["快递名称"] == express_name:
            express_id = i["快递ID"]
            break
    # print(f"快递ID：{express_id}")
    return express_id


# 获取库位信息
def get_bin_info(warehouse_name):
    """
      warehouse_name:仓库名
      """
    url = "http://gw.erp12345.com/api/Basics/WarehouseStorage/QueryPage?"
    params = {
        "WarehouseId": inventory_interface.get_inventory_id(warehouse_name),
        "BinType": 11,
        "ModelTypeName": "ErpWeb.Domain.ViewModels.Basics.WarehouseStorageVmv",
        "page": 1,
        "pagesize": 2000,
    }
    for k, v in params.items():
        url += f"{k}={v}&"
    headers = {
        'Cookie': base.cookies
    }
    # print(url)
    response = requests.get(url, headers=headers)
    result = dict(response.json())
    return result


# 获取随机库位
def get_random_bin(warehouse_name):
    """
    warehouse_name: 仓库名称
    return :{'ID': '7494878028288230927', '库位': 'P-1-975-1', '绑定商品': None}

    """
    """
    原始结果：{'WarehouseStorageProSku': None, 'Name': 'R-1-1-1-49', 'WarehouseStorage': None, 'WarehouseId': '162573418911628622', 'Id': '7494878028338561085'}

    """
    result = get_bin_info(warehouse_name)
    random_num = random.randint(1, 2000)
    random_bin = result["data"]["Items"][random_num]
    random_bin_info = {"ID": random_bin["Id"], "库位": random_bin["Name"], "绑定商品": random_bin["WarehouseStorageProSku"]}
    return random_bin_info


# 获取店铺信息
def get_shop_info(shop_name):
    """
    shop_name:店铺名
    """
    """原始数据： {"data":{"Items":[{"Id":"7494677199308457149","IsDisable":false,"Name":"巨淘气","PlatformType":1,
    "PlatformName":"淘宝集市","ShipName":"芮苏云","ShipPhone":"15221071395","ShipAddress":"恒西路189号","Memo":"",
    "AuthorizeBeginDate":"2020-07-03 12:38:05","AuthorizeEndDate":"2020-12-27 05:59:59","Nick":"章kun666666",
    "ShipRegionName":"上海 > 上海市 > 闵行区"}],"TotalCount":1},"code":1,"message":null} """
    url = "http://gw.erp12345.com/api/Basics/Shop/QueryPage?"
    params = {
        "ModelTypeName": "ErpWeb.Domain.ViewModels.ShopVm",
        "Name": shop_name,
    }
    for k, v in params.items():
        url += f"{k}={v}&"
    headers = {
        'Cookie': base.cookies
    }
    # print(url)
    response = requests.get(url, headers=headers)
    result = dict(response.json())
    return result


# 获取店铺id
def get_shop_id(shop_name):
    """
    shop_name:店铺名
    """
    result = get_shop_info(shop_name)
    shop_id = result["data"]["Items"][0]["Id"]
    return shop_id
