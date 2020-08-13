import sys
import time
import pytest
from os.path import dirname, abspath
from selenium import webdriver
import page.login_page as login
import page.base_page as base
import page.order.all_order_page as order

sys.path.insert(0, dirname(dirname(dirname(abspath(__file__)))))


def setup_module():
    base.driver = webdriver.Chrome()
    base.cookies = login.login()
    print("全部订单测试开始")


def setup_function():
    base.open_page("订单", "全部订单", "全部订单框架")


def teardown_function():
    base.close_page("全部订单")


def teardown_module():
    base.browser_close()
    print("全部订单测试结束")


# 测试批量搜索功能
def test_multi_search():
    # 测试批量搜索会员名称
    """
    目前支持的类型共有4种：会员名称，平台单号，物流单号，地址（未发货）
    1.先进行会员名称批量搜索
        先打开文件，读取数据，然后使用批量搜索并对比结果
        会员名称可以搜索所有订单的会员，包括 未审核，已审核，已出库等
    2.再进行物流单号批量搜索
        物流单号可搜索所哟状态，包括已出库，未出库
    3.之后是平台单号
        只要是系统中的平台单号都能搜索，platform_order_code.txt 中包含未审核，发货中，已出库的平台单号
    4.最后是地址
            地址比较特殊，只搜索未审核的订单地址，包含未审核，和部分审核，文件中给了3种
            address_list.txt 中是未审核，部分审核的
            not_found_address_list.txt 包含已审核，已出库的地址和找不到的地址
    全部通过数据文件使用固定数据进行测试
    批量搜索提示不要超过200，其实超过了没事，只不过可能查询时间会比较长
    """
    # ————————————————————————————
    # 111111111111111111111111111111
    # 先进行会员名称测试
    # 111111111111111111111111111111
    # ————————————————————————————
    with open('file_for_multi_search/vip_list.txt', 'r', encoding='UTF-8') as f:
        vip_list = f.readlines()
    f.close()
    with open('file_for_multi_search/not_found_vip_list.txt', 'r', encoding='UTF-8') as f:
        not_found_vip_list = f.readlines()
    f.close()
    base.wait_element(order.locations["批量搜索下拉按钮"]).click()
    base.wait_element(base.find_xpath("搜索类型", "买家账号")).click()
    for v in vip_list:
        base.wait_element(order.locations["批量搜索文本框"]).send_keys(v)
    for v in not_found_vip_list:
        base.wait_element(order.locations["批量搜索文本框"]).send_keys(v)
    base.wait_table_refresh(base.find_xpath("每行一个", "确认"), 1, "会员名")
    base.driver.switch_to.default_content()
    not_found_vip_result = base.wait_element(base.find_xpath("信息", "以下买家账号没有搜索到")).text.split("\n")
    print(not_found_vip_result)
    not_found_vip_result.pop(0)
    print(not_found_vip_result)
    for v in not_found_vip_result:
        assert v+'\n' in not_found_vip_list
    base.wait_element(base.find_xpath("信息", "确定")).click()
    base.driver.switch_to.default_content()
    base.switch_to_frame(base.locations["全部订单框架"])
    vip_result = base.get_column_text("会员名")
    for v in vip_result:
        assert v+'\n' in vip_list
    # ————————————————————————————
    # 22222222222222222222222222222222
    # 再进行物流单号测试
    # 22222222222222222222222222222222
    # ————————————————————————————
    time.sleep(1)
    base.wait_table_refresh(base.find_xpath('清空'), 1, '会员名')
    # 测试批量搜索物流单号
    with open('file_for_multi_search/express_code.txt', 'r', encoding='UTF-8') as f:
        express_code_list = f.readlines()
    f.close()
    with open('file_for_multi_search/not_found_express_code_list.txt', 'r', encoding='UTF-8') as f:
        not_found_express_code_list = f.readlines()
    f.close()
    base.wait_element(order.locations["批量搜索下拉按钮"]).click()
    base.wait_element(base.find_xpath("搜索类型", "物流单号")).click()
    for v in express_code_list:
        base.wait_element(order.locations["批量搜索文本框"]).send_keys(v)
    for v in not_found_express_code_list:
        base.wait_element(order.locations["批量搜索文本框"]).send_keys(v)
    base.wait_table_refresh(base.find_xpath("每行一个", "确认"), 1, "会员名")
    base.driver.switch_to.default_content()
    not_found_express_code_result = base.wait_element(base.find_xpath("信息", "以下物流单号没有搜索到")).text.split("\n")
    print(not_found_express_code_result)
    not_found_express_code_result.pop(0)
    print(not_found_express_code_result)
    for v in not_found_express_code_result:
        assert v+'\n' in not_found_express_code_list
    base.wait_element(base.find_xpath("信息", "确定")).click()
    base.driver.switch_to.default_content()
    base.switch_to_frame(base.locations["全部订单框架"])
    vip_result = base.get_column_text("会员名")
    # 全部订单页面没有物流单号字段只能使用会员名称替代下
    with open('file_for_multi_search/express_code_vip_name_result.txt', 'r', encoding='UTF-8') as f:
        vip_name_result = f.readlines()
    f.close()
    for v in vip_result:
        assert v+'\n' in vip_name_result
    # ————————————————————————————
    # 33333333333333333333333333333333
    # 之后是平台单号测试
    # 33333333333333333333333333333333
    # ————————————————————————————
    time.sleep(1)
    base.wait_table_refresh(base.find_xpath('清空'), 1, '会员名')
    # 开始平台单号批量搜索测试
    with open('file_for_multi_search/platform_order_code.txt', 'r', encoding='UTF-8') as f:
        platform_order_code_list = f.readlines()
    f.close()
    with open('file_for_multi_search/not_found_platform_order_code.txt', 'r', encoding='UTF-8') as f:
        not_found_platform_order_code_list = f.readlines()
    f.close()
    base.wait_element(order.locations["批量搜索下拉按钮"]).click()
    base.wait_element(base.find_xpath("搜索类型", "平台单号")).click()
    for v in platform_order_code_list:
        base.wait_element(order.locations["批量搜索文本框"]).send_keys(v)
    for v in not_found_platform_order_code_list:
        base.wait_element(order.locations["批量搜索文本框"]).send_keys(v)
    base.wait_table_refresh(base.find_xpath("每行一个", "确认"), 1, "会员名")
    base.driver.switch_to.default_content()
    not_found_platform_order_code_result = base.wait_element(base.find_xpath("信息", "以下")).text.split("\n")
    print(not_found_platform_order_code_result)
    not_found_platform_order_code_result.pop(0)
    print(not_found_platform_order_code_result)
    for v in not_found_platform_order_code_result:
        assert v+'\n' in not_found_platform_order_code_list
    base.wait_element(base.find_xpath("信息", "确定")).click()
    base.driver.switch_to.default_content()
    base.switch_to_frame(base.locations["全部订单框架"])
    platform_order_code_result = base.get_column_text("平台单号")
    for v in platform_order_code_result:
        assert v+'\n' in platform_order_code_list
    # ————————————————————————————
    # 4444444444444444444444444444444444
    # 最后是地址
    # 4444444444444444444444444444444444
    # ————————————————————————————
    time.sleep(1)
    base.wait_table_refresh(base.find_xpath('清空'), 1, '会员名')
    # 最后开始地址（未发货）批量搜索测试
    with open('file_for_multi_search/address_list.txt', 'r', encoding='UTF-8') as f:
        address_list = f.readlines()
    f.close()
    print(address_list)
    with open('file_for_multi_search/not_found_address_list.txt', 'r', encoding='UTF-8') as f:
        not_found_address_list = f.readlines()
    f.close()
    print(not_found_address_list)
    base.wait_element(order.locations["批量搜索下拉按钮"]).click()
    base.wait_element(base.find_xpath("搜索类型", "地址")).click()
    for v in address_list:
        base.wait_element(order.locations["批量搜索文本框"]).send_keys(v)
    for v in not_found_address_list:
        base.wait_element(order.locations["批量搜索文本框"]).send_keys(v)
    base.wait_table_refresh(base.find_xpath("每行一个", "确认"), 1, "会员名")
    base.driver.switch_to.default_content()
    not_found_address_result = base.wait_element(base.find_xpath("信息", "以下")).text.split("\n")
    print(not_found_address_result)
    not_found_address_result.pop(0)
    print(not_found_address_result)
    for v in not_found_address_result:
        assert v + '\n' in not_found_address_list
    base.wait_element(base.find_xpath("信息", "确定")).click()
    base.driver.switch_to.default_content()
    base.switch_to_frame(base.locations["全部订单框架"])
    base.scroll_to(5)
    address_result = base.get_column_text("收货地址")
    for v in address_result:
        assert v.replace('\n改', '') + '\n' in address_list


# 测试模糊搜索功能
def test_fuzzy_search():
    """
    订单编码，平台单号，买家帐号，收货人姓名，收货人手机，收货人电话，物流单号
    """


if __name__ == '__main__':
    pytest.main()
