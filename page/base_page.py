import datetime
import time

import requests
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver import ActionChains

global driver
cookies = []
locations = {"全部订单框架": "//iframe[contains(@src,'orders/allOrder/orderbrowserview')]",
             "自由打印框架": "//iframe[contains(@src,'Products/FreePrint/FreePrintBrowserView')]",
             "平台编码上传框架": "//iframe[contains(@src,"
                         "'Products/PlatformProductTool/PlatformProductToolBrowserView')]",
             "店铺商品匹配框架": "//iframe[contains(@src,'Products/ShopProductMatch/ShopProductMatchBrowserView')]",
             "套餐商品框架": "//iframe[contains(@src,'Products/comboProduct/ComboProductBrowserView')]",
             "门店收银框架": "//iframe[contains(@src,'Pos/Pos/PosBrowserView')]",
             "采购建议框架": "//iframe[contains(@src,'Purchase/PurchaseAdvise/PurchaseAdviseBrowserView')]",
             "采购单框架": "//iframe[contains(@src,'Purchase/Purchase/PurchaseOrderBrowserView')]",
             "全部订单框架": "//iframe[contains(@src,'orders/allOrder/orderbrowserview')]",
             "打印发货框架": "//iframe[contains(@src,'Deliverys/Delivery/DeliveryBrowserView')]",
             "打包登记框架": "//iframe[contains(@src,'Orders/PackageRegister/PackageRegisterBrowserView')]",
             "会员管理框架": "//iframe[contains(@src,'Vips/FullVip/FullVipBrowserView')]",
             "库存查询框架": "//iframe[contains(@src,'Inventorys/Inventory/InventoryBrowserView')]",
             "入库单框架": "//iframe[contains(@src,'Stocks/StockInOrder/StockInOrderBrowserView')]",
             "盘点单框架": "//iframe[contains(@src,'Inventorys/InventoryVer/InventoryVerBrowserView')]",
             "售后单框架": "//iframe[contains(@src,'AfterServices/ServiceOrder/ServiceOrderBrowserView')]",
             "供应商往来账框架": "//iframe[contains(@src,'Finances/SupplierBillOrder/SupplierBillOrderBrowserView')]",
             "供应商结算单框架": "//iframe[contains(@src,'Finances/SupplierSettleOrder/SupplierSettleOrderBrowserView')]",
             "基础业务框架": "//iframe[contains(@src,'Settings/BillSetting/BillSettingBrowserView')]",
             "订单设置框架": "//iframe[contains(@src,'Settings/OrderSetting/OrderSettingBrowserView')]",
             "外观设置框架": "//iframe[contains(@src,'Settings/AppearanceSetting/AppearanceSettingBrowserView')]",
             "供应商管理框架": "//iframe[contains(@src,'Settings/Supplier/SupplierBrowserView')]"}


def get_location(key_name):
    return locations[key_name]


def get_now_string():
    now_string = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    return now_string


def find_xpath_by_placeholder(keywords):
    xpath = f"//*[@placeholder='{keywords}']"
    return xpath


"""
def find_xpath(keywords):
    xpath = f"//*[text()='{keywords}']"
    return xpath



def find_xpath(keywords1, keywords2):
    xpath = "//*[contains(text(),'{}')]/following::*[contains(text(),'{}')]".format(keywords1, keywords2)
    return xpath
"""


def find_xpath(keywords1, keywords2=''):
    if keywords2 == '':
        xpath = f"//*[text()='{keywords1}']"
    else:
        xpath = f"//*[contains(text(),'{keywords1}')]/following::*[contains(text(),'{keywords2}')]"
    return xpath


def find_xpath_by_tag_name(keywords1, keywords2):
    xpath = "//*[text()='{0}']/following::{1}".format(keywords1, keywords2)
    return xpath


def wait_element(xpath):
    start = datetime.datetime.now()
    while (datetime.datetime.now() - start).seconds < 30:
        try:
            element = driver.find_element_by_xpath(xpath)
            if element:
                return element
            else:
                continue
        except Exception:
            continue
    assert 1 == 2, "元素不存在:{}".format(xpath)


def wait_table_refresh(button_xpath, keywords, column_name):
    element = driver.find_element_by_xpath(get_cell_xpath(keywords, column_name))
    wait_element(button_xpath).click()
    start = datetime.datetime.now()
    while (datetime.datetime.now() - start).seconds < 30:
        try:
            element.get_attribute("value")
        except StaleElementReferenceException:
            break


def get_cell_xpath():
    pass


def get_column_field(column_name):
    xpath = "//div[contains(@class,'ag-header-cell') and contains(string(),'{}')]".format(column_name)
    column_field = wait_element(xpath).GetAttribute("col-id")
    return column_field


def close_page(page_name):
    xpath = "//span[@title='双击关闭窗口 右键固定菜单' and text()='{0}']".format(page_name)
    driver.switch_to.default_content()
    ActionChains(driver).double_click(wait_element(xpath)).perform()


def browser_close():
    driver.quit()


# 新增会员
def new_vip(name):
    """
    name:会员名称，一般用get_now_string()生成
    return:返回【会员ID，会员名称】
    """
    headers = {
        'Cookie': cookies
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


def get_vip_id(name):
    user_info = {
        'ModelTypeName': 'ErpWeb.Domain.ViewModels.Vips.FullVipVmv',
        'VipName': name,
        'IsHide': 'false',
    }
    url = "http://gw.erp12345.com/api/Vips/FullVip/QueryPage?"
    for k, v in user_info.items():
        url += f"{k}={v}&"
    headers = {
        'Cookie': cookies
    }
    response = requests.get(url, headers=headers)
    vip_id = dict(response.json())['data']['Items'][0]['VipId']
    return vip_id

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
        'Cookie': cookies
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
