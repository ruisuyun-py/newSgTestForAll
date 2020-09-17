import os
import sys
import time
from datetime import datetime
import pytest
from os.path import dirname, abspath
from selenium import webdriver
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


def test_new_order():
    base.wait_element_click(base.find_xpath("新增订单"))
    base.wait_element_click(base.find_xpath_with_spaces("手工新增订单"))
    base.change_frame("全部订单框架", "创建新订单")
    base.wait_element_click(base.find_xpath("阿里测试店铺01"))
    base.wait_element_click(base.find_xpath("选择买家", "选择买家"))
    base.change_frame("全部订单框架", "选择买家")
    print(f"该页面单击直接勾选")
    base.wait_element(base.find_xpath("加载", "渲染"))
    base.wait_element_click(base.get_cell_xpath(1, "所属平台"))
    base.change_frame("全部订单框架")
    base.wait_element_click(base.find_xpath("选择买家", "确认选择的买家"))
    base.change_frame("全部订单框架", "创建新订单")
    base.wait_element(base.find_xpath_by_tag_name("买家留言", "input")).send_keys("买家留言")
    base.wait_element(base.find_xpath_by_tag_name("卖家备注", "input")).send_keys("卖家备注")
    base.change_frame("全部订单框架")
    base.wait_element_click(base.find_xpath("确认并创建新的订单"))
    base.wait_element(base.find_xpath("增加新的商品"))
    order_code = base.wait_element(base.get_cell_xpath(1, "订单编码")).text
    base.wait_element_click(base.find_xpath("增加新的商品"))
    base.change_frame("全部订单框架", "选择商品")
    base.chose_product_by_text("测试商品1-红色 XS,测试商品1-红色 S")
    base.change_frame("全部订单框架")
    base.wait_element_click(base.find_xpath("选择商品", "确定"))
    base.wait_element_click(base.get_cell_xpath(1, "订单编码"))
    base.wait_element_click(base.get_cell_xpath(1, "订单编码", "详"))
    base.change_frame("全部订单框架", "订单详情")
    base.wait_element_click(base.find_xpath("快速支付"))
    base.wait_element(base.find_xpath("确认快速添加支付明细吗？"))
    time.sleep(1)
    base.wait_element_click(base.find_xpath("确认快速添加支付明细吗？", "确定"))
    base.wait_element(base.find_xpath("支付账号", "支付日期"))
    base.change_frame("全部订单框架")
    base.wait_element_click(base.find_xpath_by_tag_name("订单详情", "a"))
    order_status = base.wait_element(base.get_cell_xpath(1, "订单状态")).text
    assert order_status == '待审核'






if __name__ == '__main__':
    pytest.main()