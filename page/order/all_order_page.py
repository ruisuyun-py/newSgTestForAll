import time

import page.base_page as base

locations = {
    "批量搜索下拉按钮": "//*[@id='ordermenu']/div[2]/form/div[1]/div/div[2]/i",
    "批量搜索文本框": "//*[@id='ordermenu']/div[2]/form/div[1]/div/div[5]/div[2]/textarea",
    "店铺下拉按钮": "//*[@id='ordermenu']/div[2]/form/div[11]/label[1]/i",
    "快递下拉按钮": "//*[@id='ordermenu']/div[2]/form/div[12]/label[1]/i",
    "仓库下拉按钮": "//*[@id='ordermenu']/div[2]/form/div[13]/label[1]/i",
    "省份下拉按钮": "//*[@id='ordermenu']/div[2]/form/div[16]/label[1]/i",
}


# 获取悬浮商品信息，目前只支持包含关键字的行的信息，后期有必要再加所有行
def get_floating_sku_info_xpath(row_keywords, sku_info_name):
    """
    sku_info_name:图片,平台商品ID,平台规格ID,平台规格ID,平台货号,平台商家编码,平台规格名称,子单号,平台商品名称,商家编码,
                    货号,其他信息,单价,单价输入框,数量输入框,数量,总价,商品名称,规格名称,库存信息,删除,,,,
    sku_keywords：行关键字，如果为空，返回的是所有行的信息定位，有关键字则是包含关键字的行的信息定位
    return：定位
    """
    floating_xpath = {
        # 商品信息悬浮窗口
        # 以下是行中某个信息的定位必须要通过拼接行定位来定位
        "图片": "/div[@class='cell itemimg']/span[1]",
        "平台信息按钮": "/div[@class='cell itemid']/div[@class='sku_id']/i",
        "平台商品ID": "/div[@class='cell itemid']/div[@class='sku_id']/div/span[1]",
        "平台规格ID": "/div[@class='cell itemid']/div[@class='sku_id']/div/span[2]",
        "平台货号": "/div[@class='cell itemid']/div[@class='sku_id']/div/span[3]",
        "平台商家编码": "/div[@class='cell itemid']/div[@class='sku_id']/div/span[4]",
        "平台规格名称": "/div[@class='cell itemid']/div[@class='sku_id']/div/span[5]",
        "子单号": "/div[@class='cell itemid']/div[@class='sku_id']/div/span[6]",
        "平台商品名称": "/div[@class='cell itemid']/div[@class='sku_id']/div",
        "商家编码": "/div[@class='cell itemid']/div[@class='i_id']",
        "货号": "/div[@class='cell itemid']/div[@class='sku_id']",
        # 商品信息包括 线下，待发货，已审xx等，不是固定占位，无法直接定位,只能定位一批
        "其他信息": "/div[@class='cell itemid']/div[@class='sku_id']/span",
        "单价": "/div[@class='cell itemprice']/div[@class='price t']",
        "单价输入框": "/div[@class='cell itemprice']/input",
        "数量输入框": "/div[@class='cell itemqty']/input",
        "数量": "/div[@class='cell itemqty']/div",
        "总价": "/div[5]/div",
        "商品名称": "/div[@class='cell itemname']/div[1]",
        "规格名称": "/div[@class='cell itemname']/div[2]",
        "库存信息": "/div[@class='cell itemname']/div[2]/span",
        "删除": "//span[@title='删除商品']",
    }
    # "包含指定关键字行": "//div[@class='table full_item_table']/div[contains(string(),'{0}')]",
    # "所有行": "//div[@class='table full_item_table']/div",
    if isinstance(row_keywords, int):
        xpath = f"//div[@class='table full_item_table']/div[{row_keywords}]"+floating_xpath[sku_info_name]
    else:
        xpath = f"//div[@class='table full_item_table']/div[contains(string(),'{row_keywords}')]"+floating_xpath[sku_info_name]
    return xpath


# 获取商品信息文本
def get_float_sku_info_text(row_keywords, sku_info_name):
    """
        sku_info_name:图片,平台商品ID,平台规格ID,平台规格ID,平台货号,平台商家编码,平台规格名称,子单号,平台商品名称,商家编码,
                        货号,其他信息,单价,单价输入框,数量输入框,数量,总价,商品名称,规格名称,库存信息,删除,,,,
        sku_keywords：行关键字，如果为空，返回的是所有行的信息定位，有关键字则是包含关键字的行的信息定位
        return：信息字符串
        """
    result = ""
    if sku_info_name == "其他信息":
        elements = base.wait_elements(get_floating_sku_info_xpath(row_keywords, sku_info_name))
        for i in elements:
            result += i.text
    elif "平台" in sku_info_name:
        base.wait_element_click(get_floating_sku_info_xpath(row_keywords, "平台信息按钮"))
        element = base.wait_element(get_floating_sku_info_xpath(row_keywords, sku_info_name))
        result = element.text
        base.wait_element_click(get_floating_sku_info_xpath(row_keywords, "其他信息"))
    else:
        element = base.wait_element(get_floating_sku_info_xpath(row_keywords, sku_info_name))
        result = element.text
    return result


# 获取所有行商品信息文本
def get_all_float_sku_info(sku_info_name):
    all_row_xpath = "//div[@class='table full_item_table']/div"
    all_rows = base.wait_elements(all_row_xpath)
    all_rows_num = len(all_rows)
    result = []
    for i in range(1, all_rows_num+1):
        info = get_float_sku_info_text(i, sku_info_name)
        result.append(info)
    return result


def get_normal_exception():
    """
    获取全部订单页面的所有常用异常，必须打开未审核有异常列表之后才能使用
    return:[normal_exception, normal_exception, normal_exception]
    """
    xpath = "//input[@placeholder='搜索异常']/../div/span"
    elements = base.wait_elements(xpath)
    result = []
    for i in elements:
        result.append(i.text)
    return result


# 获取旗帜列表
def get_flag_list():
    """
    获取全部旗帜类型
    return:["红旗","绿旗","黄旗"]
    """
    xpath = "//span[text()='选择旗帜']/../span"
    elements = base.wait_elements(xpath)
    elements.pop(0)
    flag_list = []
    for i in elements:
        flag_list.append(i.text)
    return flag_list


# 获取省份
def get_province_list():
    xpath = "//label[text()='省份']/../ul/li/label"
    province_elements = base.wait_elements(xpath)
    province_list = []
    for i in province_elements:
        province_list.append(i.text)
    return province_list
