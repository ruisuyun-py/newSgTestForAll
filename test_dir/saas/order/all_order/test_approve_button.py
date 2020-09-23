import os
import sys
import time
import datetime
import pytest
from os.path import dirname, abspath
from selenium import webdriver
import selenium.common.exceptions as exceptions
from selenium.webdriver.common.keys import Keys
import test_dir.test_base as test
import page.login_page as login
import page.base_page as base
import page.order.all_order_page as order
import interface.interface as interface
import interface.order.delivery_order_interface as delivery_interface
import interface.supplier.supplier_interface as supplier_interface
import interface.order.order_interface as order_interface
import interface.product.product_interface as product_interface
import interface.vip.vip_interface as vip_interface
import interface.setting.setting_interface as setting_interface
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


def test_approve_button():
    print(f"把异常全部点击一遍，有异常的审核，看能否正常报错")
    exception_list = {
        "黑名单": "黑名单",
        "线上改商品": "线上改商品",
        "标记异常": "标记异常",
        "线上修改地址": "线上修改地址",
        "未设置仓库": "未设置仓库",
        "未设置快递": "未设置快递",
        "收货信息不完整": "收货信息不完整",
        "手工终止发货": "手工终止发货",
        "商品未匹配": "商品未匹配",
        "付款异常": "付款异常",
        "全部退款": "全部退款",
        "部分退款": "部分退款",
        "无商品信息": "无商品信息",
        "其他ERP已发货": "其他ERP已发货",
        "线上锁定": "线上锁定",
    }
    base.wait_element(base.find_xpath("异常", "未审核有异常"))
    time.sleep(1)
    base.wait_element_click(base.find_xpath("异常", "未审核有异常"))
    for k, v in exception_list.items():
        base.wait_element_click(base.find_xpath("未审核有异常", k))
        element = base.wait_element(base.find_xpath("本页共", "加载"))
        text = element.text
        base.wait_element_click(base.find_xpath("组合查询"))
        base.wait_element_refresh(element, text)
        num_text = base.wait_element(base.find_xpath("已选择", "本页共")).text
        print(num_text)
        if num_text == "本页共0条数据":
            print(f"黑名单异常没有数据，不用查看")
            base.wait_element_click(base.find_xpath("未审核有异常", k))
            continue
        else:
            base.wait_element_click(base.get_cell_xpath(1, "订单编码"))
            base.click_space()
            base.wait_element_click(base.find_xpath("审核"))
            try:
                base.wait_element(base.find_xpath("信息", v))
            except AssertionError as ae:
                print(ae)
                assert 1 == 2, f"全部订单页面审核有{k}异常的订单不能正常弹窗报错"
            base.wait_element(base.find_xpath("信息", "确定"))
            time.sleep(1)
            base.wait_element_click(base.find_xpath("信息", "确定"))
            base.wait_element_click(base.find_xpath("未审核有异常", k))
    print(f"新建会员，转异常，验证是否能正常报错")
    base.wait_element_click(base.find_xpath("清空"))
    vip_name = "会员" + base.get_now_string()
    vip_interface.new_vip(vip_name)
    print(f"{vip_name}")
    product_code = base.get_now_string()
    product_interface.new_product(product_code)
    sku_code = product_interface.get_sku_code(product_code)[0]
    product_interface.modify_sku_price(sku_code, "100")
    sku_info = [{'商家编码': sku_code, '数量': '2'}, ]
    order_code = order_interface.new_order(vip_name, sku_info)["Code"]
    merge_order_code = order_interface.new_order(vip_name, sku_info)["Code"]
    print(order_code)
    base.fuzzy_search("订单编码", vip_name)
    base.wait_element_click(base.get_cell_xpath(order_code, "订单编码"))
    base.click_space()
    print(f"先测试 黑名单，终结， 标记异常审核时系统能否正常报错")
    order.turn_to_exception("黑名单")
    base.wait_text_locate(base.get_cell_xpath(order_code, "订单状态"), "黑名单")
    base.wait_element_click(base.find_xpath("审核"))
    try:
        base.wait_element(base.find_xpath("信息", f"订单:/{order_code}有异常：黑名单"))
    except AssertionError as e:
        print(e)
        assert 1 == 2, f"全部订单页面审核标记异常订单不能正常弹窗报错"
    time.sleep(1)
    base.wait_element_click(base.find_xpath("信息", "确定"))
    print(f"审核待合并订单，则需要报错待合并订单异常")
    base.fuzzy_search("订单编码", merge_order_code)
    base.select_all()
    base.wait_element_click(base.find_xpath("审核"))
    try:
        base.wait_element(base.find_xpath("信息", f"待合并订单:/{order_code}有异常：黑名单"))
    except AssertionError as e:
        print(e)
        assert 1 == 2, f"全部订单页面审核标记异常订单不能正常弹窗报错"
    time.sleep(1)
    base.wait_element_click(base.find_xpath("信息", "确定"))
    order.turn_to_normal("黑名单")
    base.wait_text_locate(base.get_cell_xpath(order_code, "订单状态"), "待审核")
    # TODO:(RUI)全部订单页面审核已终结的订单报错：当前数据可能被其他人操作了，请刷新后重试！，需要优化下报错，比如 订单:/TD200918013有异常：标记异常 常用异常2
    # order.turn_to_exception("终结")
    # base.wait_text_locate(base.get_cell_xpath(order_code, "订单状态"), "已终结")
    # order.turn_to_normal("已终结")
    # base.wait_text_locate(base.get_cell_xpath(order_code, "订单状态"), "待审核")
    order.turn_to_exception("标记异常", "异常测试")
    base.wait_text_locate(base.get_cell_xpath(order_code, "订单状态"), "异常测试")
    base.wait_element_click(base.find_xpath("审核"))
    try:
        base.wait_element(base.find_xpath("信息", f"订单:/{order_code}有异常：标记异常 异常测试"))
    except AssertionError as e:
        print(e)
        assert 1 == 2, f"全部订单页面审核标记异常订单不能正常弹窗报错"
    time.sleep(1)
    base.wait_element_click(base.find_xpath("信息", "确定"))
    order.turn_to_normal("标记异常")
    base.wait_text_locate(base.get_cell_xpath(order_code, "订单状态"), "待审核")
    order.turn_to_exception("常用异常", "常用异常2")
    base.wait_text_locate(base.get_cell_xpath(order_code, "订单状态"), "常用异常2")
    base.wait_element_click(base.find_xpath("审核"))
    try:
        base.wait_element(base.find_xpath("信息", f"订单:/{order_code}有异常：标记异常 常用异常2"))
    except AssertionError as e:
        print(e)
        assert 1 == 2, f"全部订单页面审核标记异常订单不能正常弹窗报错"
    time.sleep(1)
    base.wait_element_click(base.find_xpath("信息", "确定"))
    order.turn_to_normal("标记异常")
    base.wait_text_locate(base.get_cell_xpath(order_code, "订单状态"), "待审核")
    print(f"先设置不允许负库存，然后审核报错，再设置允许负库存，审核订单")
    setting_info = {"允许负库存": "false"}
    setting_interface.save_base_setting(setting_info)
    time.sleep(5)
    print(f"设置不允许负库存之后，等待5秒设置生效")
    base.wait_element_click(base.find_xpath("审核"))
    base.wait_element(base.find_xpath("信息", "库存不足，不允许审核"))
    time.sleep(1)
    base.wait_element_click(base.find_xpath("信息", "确定"))
    setting_info = {"允许负库存": "true"}
    setting_interface.save_base_setting(setting_info)
    time.sleep(5)
    print(f"设置不允许负库存之后，等待5秒设置生效")
    element = base.wait_element(base.get_cell_xpath(order_code, "订单状态"))
    text = element.text
    base.wait_element_click(base.find_xpath("审核"))
    base.wait_element_refresh(element, text)
    order_status = base.wait_element(base.get_cell_xpath(order_code, "订单状态")).text
    assert order_status == '发货中'



if __name__ == '__main__':
    pytest.main()