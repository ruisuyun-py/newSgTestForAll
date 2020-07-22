import datetime
import time

import js2py
import requests
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

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
             "供应商管理框架": "//iframe[contains(@src,'Settings/Supplier/SupplierBrowserView')]"
             }


def get_location(key_name):
    return locations[key_name]


def get_now_string():
    now_string = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    return now_string


def close_page(page_name):
    xpath = "//span[@title='双击关闭窗口 右键固定菜单' and text()='{0}']".format(page_name)
    driver.switch_to.default_content()
    ActionChains(driver).double_click(wait_element(xpath)).perform()


def browser_close():
    driver.quit()


def find_xpath_by_placeholder(keywords):
    xpath = f"//*[@placeholder='{keywords}']"
    return xpath


def find_xpath(keywords1, keywords2=''):
    if keywords2 == '':
        xpath = f"//*[text()='{keywords1}']"
    else:
        xpath = f"//*[contains(text(),'{keywords1}')]/following::*[contains(text(),'{keywords2}')]"
    return xpath


def find_xpath_by_tag_name(keywords1, keywords2):
    xpath = "//*[text()='{0}']/following::{1}".format(keywords1, keywords2)
    return xpath


def find_xpath_with_bland(keywords):
    xpath = f"//*[contains(text(),'{keywords}')]"
    return xpath


def find_xpath_for_right_menu(keywords):
    xpath = f"//span[@ref='eName' and text()='{keywords}']"
    return xpath


def find_frame(frame_name):
    xpath = f"//div[text()='{frame_name}']/../div[2]/iframe"
    return xpath


def switch_to_frame(xpath):
    driver.switch_to.frame(driver.find_element_by_xpath(xpath))


def open_page(menu_name, page_name, frame_name):
    driver.switch_to.default_content
    wait_element(find_xpath(menu_name)).click()
    wait_element(find_xpath(page_name)).click()
    driver.switch_to.default_content
    switch_to_frame(get_location(frame_name))


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


def wait_elements(xpath):
    start = datetime.datetime.now()
    while (datetime.datetime.now() - start).seconds < 30:
        try:
            elements = driver.find_elements_by_xpath(xpath)
            if elements:
                return elements
            else:
                continue
        except Exception:
            continue
    assert 1 == 2, "元素不存在:{}".format(xpath)


def wait_table_refresh(button_xpath, column_name, keywords):
    element = driver.find_element_by_xpath(get_cell_xpath(keywords, column_name))
    wait_element(button_xpath).click()
    start = datetime.datetime.now()
    while (datetime.datetime.now() - start).seconds < 30:
        try:
            element.get_attribute("value")
        except StaleElementReferenceException:
            break


def get_column_field(column_name):
    xpath = "//div[contains(@class,'ag-header-cell') and contains(string(),'{}')]".format(column_name)
    column_field = wait_element(xpath).GetAttribute("col-id")
    return column_field


# 获取主表中指定行号指定列单元格
def get_cell_xpath(row_key, column_name):
    """
    row_id:行号，由于主表的行号是从0计数，这里做了-1处理
    column_name:列名
    return:单元格定位
    """
    if isinstance(row_key, int):
        xpath = f"//div[@row-id='{row_key - 1}']/div[@col-id='{get_column_field(column_name)}']"
    else:
        xpath = f"//div[@role='row' and contains(string(),'{row_key}')]/div[@col-id='{get_column_field(column_name)}']"
    return xpath


# 获取新表格中指定行号，指定列，中指定图标定位
def get_cell_icon_xpath(row_key, column_name, icon_text):
    """
    row_key:行号或者行关键字
    column_name：列名
    icon_text:图标文本
    return：图标定位
    """
    if isinstance(row_key, int):
        xpath = f"//div[@row-id='{row_key - 1}']/div[@col-id='{get_column_field(column_name)}']/span[1]/span[text()='{icon_text}'] "
    else:
        xpath = f"//div[@role='row' and contains(string(),'{row_key}')]/div[@col-id='{get_column_field(column_name)}']/span[1]/span[text()='{icon_text}'] "
    return xpath


# 获取主表中输入框的订单，现在用的很少
def get_input_xpath(column_name):
    """
    column_name:列名
    return:一列输入框的定位
    """
    xpath = f"//div[@role='gridcell' and @col-id='{get_column_field(column_name)}']/span/input"
    return xpath


# 获取主表中一列的文本
def get_column_text(column_name):
    """
    column:列名
    return：文本列表
    """
    xpath = f"//div[@role='gridcell' and @col-id='{get_column_field(column_name)}']"
    elements = wait_elements(xpath)
    text_list = []
    for element in elements:
        text_list.append(element.text)
    return text_list


# 滚动条滚动
def scroll_to(num):
    """
    将滚动条分成10份，选择移动到哪个位置
    """
    context_js_obj = js2py.EvalJs()
    js = f"document.getElementsByClassName('ag-body-horizontal-scroll-viewport')[0].scrollLeft=document" \
         f".getElementsByClassName('ag-body-horizontal-scroll-viewport')[0].scrollWidth/10*{num}; "
    context_js_obj.execute(js)


def scroll_to_view(xpath):
    element = wait_element(xpath)
    context_js_obj = js2py.EvalJs()
    js = "arguments[0].scrollIntoView();"
    context_js_obj.execute(js, element)


def select_all():
    xpath = "//input[@ref='cbSelectAll']"
    wait_element(xpath).click()


def double_click(xpath):
    ActionChains(driver).double_click(wait_element(xpath)).perform()


def right_click(xpath):
    ActionChains(driver).context_click(wait_element(xpath)).perform()


def click_control():
    ActionChains(driver).key_down(Keys.CONTROL).perform()


def click_space():
    ActionChains(driver).key_down(Keys.SPACE).perform()