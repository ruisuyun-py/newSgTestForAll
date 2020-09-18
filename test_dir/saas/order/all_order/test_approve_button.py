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
    vip_name = "会员" + base.get_now_string()
    vip_interface.new_vip(vip_name)
    print(f"{vip_name}")
    sku_info = [{'商家编码': '测试商品1-红色 XS', '数量': '2'}, ]
    order_code = order_interface.new_order(vip_name, sku_info)["Code"]
    base.fuzzy_search("订单编码", order_code)
    base.select_all()
    print(f"先测试 黑名单，终结， 标记异常审核时系统能否正常报错")
    # TODO:(rui)全部订单页面审核时不拦截黑名单异常
    # order.turn_to_exception("黑名单")
    # base.wait_text_locate(base.get_cell_xpath(order_code, "订单状态"), "黑名单")
    # base.wait_element_click(base.find_xpath("审核"))
    # order.turn_to_normal("黑名单")
    # base.wait_text_locate(base.get_cell_xpath(order_code, "订单状态"), "待审核")
    # TODO:(RUI)全部订单页面审核已终结的订单报错：当前数据可能被其他人操作了，请刷新后重试！，需要优化下报错，比如 订单:/TD200918013有异常：标记异常 常用异常2
    # order.turn_to_exception("终结")
    # base.wait_text_locate(base.get_cell_xpath(order_code, "订单状态"), "已终结")
    # order.turn_to_normal("已终结")
    # base.wait_text_locate(base.get_cell_xpath(order_code, "订单状态"), "待审核")
    order.turn_to_exception("标记异常", "手工标记异常测试")
    base.wait_text_locate(base.get_cell_xpath(order_code, "订单状态"), "手工标记异常测试")
    base.wait_element_click(base.find_xpath("审核"))
    try:
        base.wait_element(base.find_xpath("信息", f"订单:/{order_code}有异常：标记异常 手工标记异常测试"))
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
    

if __name__ == '__main__':
    pytest.main()