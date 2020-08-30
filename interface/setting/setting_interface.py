import time
import requests
import page.base_page as base


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
