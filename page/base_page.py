import datetime
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver import ActionChains

driver = webdriver.Chrome()
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


def find_xpath_by_placeholder(keywords):
    xpath = "//*[@placeholder='{}']".format(keywords)
    return xpath


def find_xpath(keywords):
    xpath = "//*[text()='{}']".format(keywords)
    return xpath

"""
def find_xpath(keywords1, keywords2):
    xpath = "//*[contains(text(),'{}')]/following::*[contains(text(),'{}')]".format(keywords1, keywords2)
    return xpath
"""

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
