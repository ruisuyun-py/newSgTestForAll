import time
import page.base_page as base
from selenium.webdriver.common.keys import Keys
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


# 转异常
def turn_to_exception(exception_type, exception_description='', normal_exceptions='常用异常1,常用异常2,常用异常3'):
    """
    exception_type:异常类型 目前仅支持常用异常，黑名单，终结，标记异常
    exception_description：异常描述，当使用常用异常时，用于指定是哪个常用异常
    normal_exceptions：用于直接覆盖常用异常枚举
    """
    base.wait_element_click(base.find_xpath("转异常"))
    base.change_frame("全部订单框架", "请输入标记异常的类型,输入相关说明")
    if exception_type == '常用异常':
        base.wait_element_click(base.find_xpath("维护常用异常"))
        base.change_frame("全部订单框架")
        base.wait_element(base.find_xpath_by_placeholder("请输入常用异常(逗号分隔)")).send_keys(Keys.CONTROL+'a')
        base.wait_element(base.find_xpath_by_placeholder("请输入常用异常(逗号分隔)")).send_keys(normal_exceptions)
        base.wait_element_click(base.find_xpath("维护常用异常", "确认"))
        base.change_frame("全部订单框架", "请输入标记异常的类型,输入相关说明")
        time.sleep(1)
        base.wait_element_click(base.find_xpath("常用异常", exception_description))
    elif exception_type in ["黑名单", "终结", "标记异常"]:
        base.wait_element_click(base.find_xpath(exception_type))
        if exception_description != '':
            base.wait_element(base.find_xpath_by_tag_name("异常描述：", "input")).send_keys(Keys.CONTROL+'a')
            base.wait_element(base.find_xpath_by_tag_name("异常描述：", "input")).send_keys(exception_description)
    else:
        assert 1 == 2, "请核实异常类型是否正确，目前仅支持常用异常，黑名单，终结，标记异常"
    base.change_frame("全部订单框架")
    base.wait_element_click(base.find_xpath("请输入标记异常的类型,输入相关说明", "确认"))
    if exception_type == '终结':
        base.wait_element(base.find_xpath("是否终结", "确定"))
        time.sleep(1)
        base.wait_element_click(base.find_xpath("是否终结", "确定"))


def turn_to_normal(exception_type):
    """
    exception_type:异常类型 目前包括：全部异常，黑名单等
    """
    base.wait_element_click(base.find_xpath("转正常单"))
    base.wait_element(base.find_xpath("选中", exception_type))
    time.sleep(1)
    base.wait_element_click(base.find_xpath("选中", exception_type))
    base.wait_element_click(base.find_xpath("转正常单", "清除选中异常"))


def modify_seller_memo(keyword, modify_info):
    """
    key_word:关键字，比如order_code
    modify_info = {"旗帜": "红旗", "备注": "111", "追加": "true", "常用备注": "常用备注1", }
    """
    flag_mapping = {
        "无旗帜": "i[2]",
        "红旗": "i[3]",
        "黄旗": "i[4]",
        "绿旗": "i[5]",
        "蓝旗": "i[6]",
        "紫旗": "i[7]",
    }
    with base.wait_refresh(base.get_cell_xpath(keyword, "卖家备注")) as e:
        base.wait_element_click(base.find_xpath("修改&标记"))
        base.wait_element_click(base.find_xpath("修改&标记", "修改备注"))
        for k, v in modify_info.items():
            if k == "旗帜":
                base.wait_element(base.find_xpath_by_tag_name("修改备注", flag_mapping[v]))
                time.sleep(1)
                base.wait_element_click(base.find_xpath_by_tag_name("修改备注", flag_mapping[v]))
            elif k == "备注":
                base.wait_element(base.find_xpath_by_tag_name("修改备注", "textarea")).send_keys(Keys.CONTROL+'a')
                base.wait_element(base.find_xpath_by_tag_name("修改备注", "textarea")).send_keys(v)
            elif k == "追加":
                element = base.wait_element(base.find_xpath_by_inner_tag_name("是否追加备注", "input"))
                is_select = element.is_selected()
                if is_select != v:
                    base.wait_element_click(base.find_xpath_by_inner_tag_name("是否追加备注", "input"))
            elif k == "常用备注":
                base.wait_element_click(base.find_xpath("维护常用卖家备注"))
                base.wait_element(base.find_xpath_by_placeholder("请输入常用卖家备注(逗号分隔)")).send_keys(Keys.CONTROL+'a')
                base.wait_element(base.find_xpath_by_placeholder("请输入常用卖家备注(逗号分隔)")).send_keys("常用备注1,常用备注2,常用备注3")
                base.wait_element_click(base.find_xpath("维护常用卖家备注", "确认"))
                base.wait_element(base.find_xpath("常用卖家备注", v))
                time.sleep(1)
                base.wait_element_click(base.find_xpath("常用卖家备注", v))
        base.wait_element_click(base.find_xpath("修改备注", "保存"))


def modify_warehouse_and_express(keyword, modify_info):
    """
    keyword:关键字，比如 order_code
    modify_info: {"仓库": "主仓库", "快递": "EMS",}
    """
    with base.wait_refresh(base.get_cell_xpath(keyword, "仓库")) as e:
        base.wait_element_click(base.find_xpath("修改&标记"))
        base.wait_element_click(base.find_xpath("修改&标记", "修改仓库、快递"))
        base.change_frame("全部订单框架", "修改仓库和快递")
        for k, v in modify_info.items():
            base.wait_element_click(base.find_xpath_by_tag_name(k, "input"))
            base.wait_element_click(base.find_xpath(v))
        base.change_frame("全部订单框架")
        base.wait_element_click(base.find_xpath("修改仓库和快递", "确认"))