import datetime
import random
import time
from contextlib import contextmanager
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

global driver
cookies = []
locations = {
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
    "预设会员价明细框架": "//iframe[contains(@src,'Vips/VipPresupposePriceDetail/VipPresupposePriceBrowserView')]",
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


def find_xpath_by_inner_tag_name(keywords1, keywords2):
    xpath = "//*[text()='{0}']/descendant::{1}".format(keywords1, keywords2)
    return xpath


def find_xpath_by_preceding_tag_name(keywords1, keywords2):
    xpath = f"//*[text()='{keywords1}']/preceding-sibling::{keywords2}"
    return xpath


def find_xpath_with_spaces(keywords):
    xpath = f"//*[contains(text(),'{keywords}')]"
    return xpath


def find_xpath_for_right_menu(keywords):
    xpath = f"//span[@ref='eName' and text()='{keywords}']"
    return xpath


def find_frame(frame_name):
    xpath = f"//div[text()='{frame_name}']/../div[2]/iframe"
    return xpath


def switch_to_frame(xpath):
    frame = wait_element(xpath)
    driver.switch_to.frame(frame)


def open_page(menu_name, page_name, frame_name):
    driver.switch_to.default_content()
    wait_element(find_xpath(menu_name)).click()
    wait_element(find_xpath(page_name)).click()
    driver.switch_to.default_content()
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


# 等待元素并点击
def wait_element_click(xpath):
    start = datetime.datetime.now()
    while (datetime.datetime.now() - start).seconds < 30:
        try:
            element = driver.find_element_by_xpath(xpath)
            if element:
                element.click()
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


# 等待主表刷新
def wait_table_refresh(button_xpath, keywords, column_name):
    """
    button_xpath:按钮定位
    keywords:可以是行号，也可以是关键字
    column_name:列名
    没有返回值
    """
    element = driver.find_element_by_xpath(get_cell_xpath(keywords, column_name))
    wait_element(button_xpath).click()
    start = datetime.datetime.now()
    while (datetime.datetime.now() - start).seconds < 30:
        try:
            element.get_attribute("value")
        except StaleElementReferenceException:
            break


# 等待元素刷新
def wait_element_refresh(element, old_text):
    """
    通过元素的文本和StaleElementReferenceException 异常来判定，元素已经被刷新
    """
    start = datetime.datetime.now()
    text = ''
    while (datetime.datetime.now() - start).seconds < 30:
        try:
            text = element.text
            if text != old_text:
                print(f"刷新前的文本：{old_text}")
                print(f"刷新后的文本：{text}")
                return text
        except StaleElementReferenceException:
            print("元素过期")
            return text
    assert 1 == 0, "元素刷新失败"


# 等待元素获取焦点
def wait_element_focus(xpath):
    """
    通过判断当前获取焦点的元素是不是目标元素来判断当前元素是否获取焦点
    """
    element = wait_element(xpath)
    start = datetime.datetime.now()
    while (datetime.datetime.now() - start).seconds < 30:
        try:
            focus_element = driver.switch_to.active_element
            if element == focus_element:
                return element
        except Exception:
            continue
    assert 1 == 0, "元素未获取焦点"


# 获取新表格组件的列域值
def get_column_field(column_name, column_name2=""):
    if column_name2 == "":
        xpath = "//div[contains(@class,'ag-header-cell') and contains(string(),'{}')]".format(column_name)
    else:
        xpath = f"//div[contains(@class,'ag-header-cell') and contains(string(),'{column_name}')]/following::div[contains(@class,'ag-header-cell') and contains(string(),'{column_name2}')]"
    column_field = wait_element(xpath).get_attribute("col-id")
    return column_field


# 获取老表格组件的列域值
def get_old_column_field(column_name):
    """
    column_name:列名
    """
    xpath = f"//span[text()='{column_name}']/ancestor::td"
    column_field = wait_element(xpath).get_attribute("field")
    return column_field


# 获取主表中指定行号指定列单元格
def get_cell_xpath(row_key, column_name, icon_text=''):
    """
    row_id:行号，由于主表的行号是从0计数，这里做了-1处理
    column_name:列名
    return:单元格定位
    """
    if isinstance(row_key, int):
        if icon_text == '':
            xpath = f"//div[@row-id='{row_key - 1}']/div[@col-id='{get_column_field(column_name)}']"
        else:
            xpath = f"//div[@row-id='{row_key - 1}']/div[@col-id='{get_column_field(column_name)}']/span[1]/" \
                    f"span[text()='{icon_text}'] "
    else:
        if icon_text == '':
            xpath = f"//div[@role='row' and contains(string(),'{row_key}')]/div[@col-id='{get_column_field(column_name)}']"
        else:
            xpath = f"//div[@role='row' and contains(string(),'{row_key}')]/div[@col-id=" \
                    f"'{get_column_field(column_name)}']/span[1]/span[text()='{icon_text}'] "
    return xpath


def get_old_cell_xpath(row_key, column_name):
    """
    row_key:做了减1
    """
    if isinstance(row_key, int):
        xpath = f"//tr[@datagrid-row-index='{row_key - 1}']/td[@field='{get_old_column_field(column_name)}']"
    else:
        xpath = f"//tr[contains(string(),'{row_key}')]/td[@field='{get_old_column_field(column_name)}']"
    return xpath


def get_old_cell_input_xpath(row_key, column_name):
    if isinstance(row_key, int):
        xpath = f"//tr[@datagrid-row-index='{row_key - 1}']/td[@field='{get_old_column_field(column_name)}']/div/input"
    else:
        xpath = f"//tr[contains(string(),'{row_key}')]/td[@field='{get_old_column_field(column_name)}']/div/input"
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
        xpath = f"//div[@row-id='{row_key - 1}']/div[@col-id='{get_column_field(column_name)}']/span[1]/" \
                f"span[text()='{icon_text}'] "
    else:
        xpath = f"//div[@role='row' and contains(string(),'{row_key}')]/div[@col-id=" \
                f"'{get_column_field(column_name)}']/span[1]/span[text()='{icon_text}'] "
    return xpath


# 获取主表中输入框的订单，现在用的很少
def get_input_xpath(column_name):
    """
    column_name:列名
    return:一列输入框的定位
    """
    xpath = f"//div[@role='gridcell' and @col-id='{get_column_field(column_name)}']/span/input"
    return xpath


# 获取一列定位
def get_column_xpath(column_name, column_name2=''):
    xpath = f"//div[@role='gridcell' and @col-id='{get_column_field(column_name, column_name2)}']"
    return xpath


# 获取主表中一列的文本
def get_column_text(column_name, column_name2=''):
    """
    column:列名
    return：文本列表
    """
    xpath = get_column_xpath(column_name, column_name2)
    elements = wait_elements(xpath)
    text_list = []
    for element in elements:
        text_list.append(element.text)
    return text_list


# 获取主表中一列的文本,并去掉重复值
def get_unique_column_text(column_name):
    """
    column:列名
    return：文本列表
    """
    xpath = get_column_xpath(column_name)
    elements = wait_elements(xpath)
    text_list = []
    for element in elements:
        text_list.append(element.text)
    return text_list


# 获取老表格组件中的一列文本
def get_old_column_text(column_name):
    xpath = f"//table[@class='datagrid-btable']/descendant::td[@field='{get_old_column_field(column_name)}']"
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
    wait_element_click(find_xpath("已选择", "本页共"))
    js = f"document.getElementsByClassName('ag-body-horizontal-scroll-viewport')[0].scrollLeft=document" \
         f".getElementsByClassName('ag-body-horizontal-scroll-viewport')[0].scrollWidth/10*{num}; "
    driver.execute_script(js)


def scroll_to_view(xpath):
    element = wait_element(xpath)
    js = "arguments[0].scrollIntoView();"
    driver.execute_script(js, element)


def select_all():
    xpath = "//div[@class='ag-header-select-all ag-labeled ag-label-align-right ag-checkbox ag-input-field' and " \
            "@ref='cbSelectAll'] "
    wait_element(xpath).click()


def double_click(xpath):
    ActionChains(driver).double_click(wait_element(xpath)).perform()


def right_click(xpath):
    ActionChains(driver).context_click(wait_element(xpath)).perform()


def click_control():
    ActionChains(driver).key_down(Keys.CONTROL).perform()


def click_space():
    ActionChains(driver).key_down(Keys.SPACE).perform()


def chose_vip(vip_name):
    element = wait_element(get_cell_xpath(1, "会员名称"))
    text = element.text
    wait_element(find_xpath_by_placeholder("会员名称")).send_keys(vip_name)
    wait_element(find_xpath_by_placeholder("会员名称")).send_keys(Keys.ENTER)
    wait_element_refresh(element, text)
    time.sleep(1)
    double_click(get_cell_xpath(vip_name, "会员名称"))


# 选择供应商
def chose_supplier_by_text(supplier_name_list):
    supplier_name_text = ""
    if isinstance(supplier_name_list, list):
        for i in supplier_name_list:
            supplier_name_text += i + ","
    else:
        supplier_name_text = supplier_name_list
    supplier_name_text = supplier_name_text.strip(",")
    supplier_input = wait_element_click(find_xpath_by_placeholder("请输入完整的供应商名称，多个供应商以逗号（，）分隔"))
    supplier_input.send_keys(Keys.CONTROL+'a')
    supplier_input.send_keys(supplier_name_text)
    supplier_input.send_keys(Keys.ENTER)
    time.sleep(1)
    print(f"输入的供应商文本{supplier_name_text}")
    print(f"输入之后选择的供应商{supplier_input.get_attribute('value')}")
    assert supplier_input.get_attribute("value") == supplier_name_text, "输入了不存在的供应商"


# 简化切换框架方法
def change_frame(frame_name='', frame_name2=''):
    """
    frame_name:一级框架/二级框架，比如全部订单框架
    frame_name2：二级框架，比如选择会员
    如果不填任何参数则直接返回底层框架
    """
    if frame_name == '':
        driver.switch_to.default_content()
    else:
        if frame_name2 == '':
            if "框架" in frame_name:
                driver.switch_to.default_content()
                switch_to_frame(locations[frame_name])
            else:
                driver.switch_to.default_content()
                switch_to_frame(find_frame(frame_name))
        else:
            driver.switch_to.default_content()
            switch_to_frame(locations[frame_name])
            switch_to_frame(find_frame(frame_name2))


@contextmanager
def operate_page(menu_name, page_name, frame_name):
    try:
        open_page(menu_name, page_name, frame_name)
        yield 1
    finally:
        close_page(page_name)
        

def fuzzy_search(column_name, keywords):
    """
    column_name:一般是需要搜索的列明或者随便什么主表存在的列名都行
    key_words:需要搜搜的关键字
    """
    wait_element(find_xpath_by_placeholder("模糊搜索")).send_keys(Keys.CONTROL + 'a')
    wait_element(find_xpath_by_placeholder("模糊搜索")).send_keys(keywords)
    wait_table_refresh(find_xpath("组合查询"), 1, column_name)


# 为方便模糊搜索测试，随机获取子字符串
def get_random_substring(source_string):
    key_char = random.choice(source_string)
    result = source_string[0:source_string.index(key_char)+1]
    return result

