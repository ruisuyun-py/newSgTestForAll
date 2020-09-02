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
import interface.purchase.purchase_interface as purchase_interface
import interface.product.product_interface as product_interface
import interface.inventory.inventory_interface as inventory_interface
sys.path.insert(0, dirname(dirname(dirname(abspath(__file__)))))


def setup_module():
    base.driver = webdriver.Chrome()
    base.cookies = login.login()


def setup_function():
    base.open_page("库存", "库存查询", "库存查询框架")


def teardown_function():
    base.close_page("库存查询")


def teardown_module():
    base.browser_close()


# 验证库存查询页面数据准确性
def test_data_correctness():
    product_code = base.get_now_string()
    product_interface.new_product(product_code)
    print(f"先新建一个商品:{product_code}")
    base.wait_element_click(base.find_xpath_by_placeholder("货号")).send_keys(product_code)
    base.wait_table_refresh(base.find_xpath("组合查询"), 1, "货号")
    print(f"校验货号是不是{product_code}")
    result = base.get_column_text("货号")
    for i in result:
        assert i == product_code
    sku_name_list = [
        "红色 XS",
        "红色 S",
        "红色 M",
        "红色 L",
        "红色 XL",
        "红色 2XL",
        "红色 3XL",
    ]
    print(f"通过规格名称数，和规格名称是不是在规格名称列表中验证规格名称")
    result = base.get_column_text("规格名称")
    assert len(result) == len(sku_name_list)
    for i in result:
        assert i in sku_name_list
    sku_code_list = []
    for i in sku_name_list:
        sku_code_list.append(product_code+"-"+i)
    print(f"通过商家编码数量和商家编码是否在商家编码列表中验证商家编码是否正确")
    result = base.get_column_text("商家编码")
    for i in result:
        assert i in sku_code_list
    sku_id_list = product_interface.get_sku_id("", product_code)
    modify_info_dict = {"商品简称": "简称"}
    product_interface.multi_modify_sku_info(sku_id_list, modify_info_dict)
    print(f"修改商品的简称为简称,再刷新一次简称是否能正常显示")
    base.wait_table_refresh(base.find_xpath("组合查询"), 1, "货号")
    result = base.get_column_text("商品简称")
    for i in result:
        assert i == "简称"
    sku_info_list = []
    for i in sku_code_list:
        sku_info_list.append({"商家编码": i, "单价": "20", "数量": "100"})
    purchase_order_id = purchase_interface.new_purchase_order("主仓库", "供应商1", sku_info_list)["ID"]
    purchase_interface.approve_and_stock_in_purchase_order(purchase_order_id)
    base.wait_table_refresh(base.find_xpath("组合查询"), 1, "货号")
    base.scroll_to(3)
    result = base.get_column_text("可销库存数")
    for i in result:
        assert i == '100'
    result = base.get_column_text("库存")
    for i in result:
        assert i == '100'
    result = base.get_column_text("余额")
    for i in result:
        assert i == "2000.00"
    result = base.get_column_text("暂存位库存")
    for i in result:
        assert i == '100'
    result = base.get_column_text("最新进价")
    for i in result:
        assert i == '20.00'
    result = base.get_column_text("成本价")
    for i in result:
        assert i == '20.00'
    print(f"每个规格采购100个，单价20，验证可销库存数是100，库存数是100，余额是2000.00,暂存位库存是100,最新进价是20.00,成本单价是20.00")
    stock_in_order_id = inventory_interface.new_stock_in_order("主仓库", "供应商1", sku_info_list)["ID"]
    inventory_interface.stock_in_stock_in_order(stock_in_order_id)
    base.wait_table_refresh(base.find_xpath("组合查询"), 1, "可销库存数")
    base.scroll_to(3)
    result = base.get_column_text("可销库存数")
    for i in result:
        assert i == '200'
    result = base.get_column_text("库存")
    for i in result:
        assert i == '200'
    result = base.get_column_text("余额")
    for i in result:
        assert i == "4000.00"
    result = base.get_column_text("暂存位库存")
    for i in result:
        assert i == '200'
    result = base.get_column_text("最新进价")
    for i in result:
        assert i == '20.00'
    result = base.get_column_text("成本价")
    for i in result:
        assert i == '20.00'
    print(f"每个规格入库100个，验证可销售库存是200，库存是200，余额是4000， 暂存位库存是200， 最新进价 20， 成本单价是20")
    stock_out_info = []
    for i in sku_code_list:
        stock_out_info.append({"商家编码": i, "单价": "20", "数量": "50"})
    result = inventory_interface.new_stock_out_order("主仓库", "供应商1", stock_out_info)
    stock_out_order_id = result["ID"]
    inventory_interface.stock_out_stock_out_order(stock_out_order_id)
    base.wait_table_refresh(base.find_xpath("组合查询"), 1, "可销库存数")
    result = base.get_column_text("可销库存数")
    for i in result:
        assert i == '150'
    result = base.get_column_text("库存")
    for i in result:
        assert i == '150'
    result = base.get_column_text("余额")
    for i in result:
        assert i == "3000.00"
    result = base.get_column_text("暂存位库存")
    for i in result:
        assert i == '150'
    result = base.get_column_text("最新进价")
    for i in result:
        assert i == '20.00'
    result = base.get_column_text("成本价")
    for i in result:
        assert i == '20.00'
    print(f"每个规格出库50个，验证可销售库存150个，库存150个， 余额3000， 暂存位库存15， ")
    result = inventory_interface.new_refund_out_order("主仓库", "供应商1", stock_out_info)
    refund_out_order_id = result["ID"]
    inventory_interface.stock_out_stock_out_order(refund_out_order_id)
    base.wait_table_refresh(base.find_xpath("组合查询"), 1, "可销库存数")
    result = base.get_column_text("可销库存数")
    for i in result:
        assert i == '100'
    result = base.get_column_text("库存")
    for i in result:
        assert i == '100'
    result = base.get_column_text("余额")
    for i in result:
        assert i == "2000.00"
    result = base.get_column_text("暂存位库存")
    for i in result:
        assert i == '100'
    result = base.get_column_text("最新进价")
    for i in result:
        assert i == '20.00'
    result = base.get_column_text("成本价")
    for i in result:
        assert i == '20.00'
    print(f"每个规格退货出库50个，验证可销售库存100个，库存100个， 余额2000， 暂存位库存100， ")
    purchase_order_id = purchase_interface.new_purchase_order("主仓库", "供应商1", stock_out_info)["ID"]
    purchase_interface.approve_purchase_order(purchase_order_id)
    base.wait_table_refresh(base.find_xpath("组合查询"), 1, "可销库存数")
    result = base.get_column_text("可销库存数")
    for i in result:
        assert i == '100'
    result = base.get_column_text("库存")
    for i in result:
        assert i == '100'
    result = base.get_column_text("余额")
    for i in result:
        assert i == "2000.00"
    result = base.get_column_text("暂存位库存")
    for i in result:
        assert i == '100'
    result = base.get_column_text("最新进价")
    for i in result:
        assert i == '20.00'
    result = base.get_column_text("成本价")
    for i in result:
        assert i == '20.00'
    result = base.get_column_text("采购在途数")
    for i in result:
        assert i == "50"
    print(f"每个规格采购50个，不入库，验证可销售库存100个，库存100个， 余额2000， 暂存位库存100， 采购在途数是50")
    