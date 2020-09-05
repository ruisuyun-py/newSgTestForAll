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
import interface.order.order_interface as order_interface
import interface.vip.vip_interface as vip_interface
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
    product_interface.modify_sku_price(sku_code_list[0], "100", "200", "300", "400")
    print(f"修改标准售价为100,第二价格为200，第三价格为300，第四价格为400")
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
    marketability_inventory = 0
    print(f"可销售库存是{marketability_inventory}")
    inventory = 0
    print(f"库存是{inventory}")
    balance = 0
    print(f"余额是{balance}")
    temporary_inventory = 0
    print(f"暂存位库存是{temporary_inventory}")
    purchase_price = 0
    print(f"最新进价是{purchase_price}")
    cost_price = 0
    print(f"成本单价是{cost_price}")
    marketability_inventory += 100
    print(f"可销售库存是{marketability_inventory}")
    inventory += 100
    print(f"库存是{inventory}")
    balance += 2000
    print(f"余额是{balance}")
    temporary_inventory += 100
    print(f"暂存位库存是{temporary_inventory}")
    purchase_price = 20
    print(f"最新进价是{purchase_price}")
    cost_price = 20
    print(f"成本单价是{cost_price}")
    result = base.get_column_text("可销库存数")
    for i in result:
        assert i == str(marketability_inventory)
    result = base.get_column_text("库存预警值", "库存数")
    for i in result:
        assert i == str(inventory)
    result = base.get_column_text("余额")
    for i in result:
        assert i == format(balance, '.2f')
    result = base.get_column_text("暂存位库存")
    for i in result:
        assert i == str(temporary_inventory)
    result = base.get_column_text("最新进价")
    for i in result:
        assert i == format(purchase_price, '.2f')
    result = base.get_column_text("成本价")
    for i in result:
        assert i == format(cost_price, '.2f')
    print(f"每个规格采购100个，单价20，验证可销库存数是100，库存数是100，余额是2000.00,暂存位库存是100,最新进价是20.00,成本单价是20.00")
    stock_in_order_id = inventory_interface.new_stock_in_order("主仓库", "供应商1", sku_info_list)["ID"]
    inventory_interface.stock_in_stock_in_order(stock_in_order_id)
    base.wait_table_refresh(base.find_xpath("组合查询"), 1, "可销库存数")
    base.scroll_to(3)
    marketability_inventory += 100
    print(f"可销售库存是{marketability_inventory}")
    inventory += 100
    print(f"库存是{inventory}")
    balance += 2000
    print(f"余额是{balance}")
    temporary_inventory += 100
    print(f"暂存位库存是{temporary_inventory}")
    purchase_price = 20
    print(f"最新进价是{purchase_price}")
    cost_price = 20
    print(f"成本单价是{cost_price}")
    result = base.get_column_text("可销库存数")
    for i in result:
        assert i == str(marketability_inventory)
    result = base.get_column_text("库存预警值", "库存数")
    for i in result:
        assert i == str(inventory)
    result = base.get_column_text("余额")
    for i in result:
        assert i == format(balance, '.2f')
    result = base.get_column_text("暂存位库存")
    for i in result:
        assert i == str(temporary_inventory)
    result = base.get_column_text("最新进价")
    for i in result:
        assert i == format(purchase_price, '.2f')
    result = base.get_column_text("成本价")
    for i in result:
        assert i == format(cost_price, '.2f')
    print(f"每个规格入库100个，验证可销售库存是200，库存是200，余额是4000， 暂存位库存是200， 最新进价 20， 成本单价是20")
    stock_out_info = []
    for i in sku_code_list:
        stock_out_info.append({"商家编码": i, "单价": "20", "数量": "50"})
    result = inventory_interface.new_stock_out_order("主仓库", "供应商1", stock_out_info)
    stock_out_order_id = result["ID"]
    inventory_interface.stock_out_stock_out_order(stock_out_order_id)
    base.wait_table_refresh(base.find_xpath("组合查询"), 1, "可销库存数")
    marketability_inventory -= 50
    print(f"可销售库存是{marketability_inventory}")
    inventory -= 50
    print(f"库存是{inventory}")
    balance -= 1000
    print(f"余额是{balance}")
    temporary_inventory -= 50
    print(f"暂存位库存是{temporary_inventory}")
    purchase_price = 20
    print(f"最新进价是{purchase_price}")
    cost_price = 20
    print(f"成本单价是{cost_price}")
    result = base.get_column_text("可销库存数")
    for i in result:
        assert i == str(marketability_inventory)
    result = base.get_column_text("库存预警值", "库存数")
    for i in result:
        assert i == str(inventory)
    result = base.get_column_text("余额")
    for i in result:
        assert i == format(balance, '.2f')
    result = base.get_column_text("暂存位库存")
    for i in result:
        assert i == str(temporary_inventory)
    result = base.get_column_text("最新进价")
    for i in result:
        assert i == format(purchase_price, '.2f')
    result = base.get_column_text("成本价")
    for i in result:
        assert i == format(cost_price, '.2f')
    print(f"每个规格出库50个，验证可销售库存150个，库存150个， 余额3000， 暂存位库存15， ")
    result = inventory_interface.new_refund_out_order("主仓库", "供应商1", stock_out_info)
    refund_out_order_id = result["ID"]
    inventory_interface.stock_out_stock_out_order(refund_out_order_id)
    base.wait_table_refresh(base.find_xpath("组合查询"), 1, "可销库存数")
    marketability_inventory -= 50
    print(f"可销售库存是{marketability_inventory}")
    inventory -= 50
    print(f"库存是{inventory}")
    balance -= 1000
    print(f"余额是{balance}")
    temporary_inventory -= 50
    print(f"暂存位库存是{temporary_inventory}")
    purchase_price = 20
    print(f"最新进价是{purchase_price}")
    cost_price = 20
    print(f"成本单价是{cost_price}")
    result = base.get_column_text("可销库存数")
    for i in result:
        assert i == str(marketability_inventory)
    result = base.get_column_text("库存预警值", "库存数")
    for i in result:
        assert i == str(inventory)
    result = base.get_column_text("余额")
    for i in result:
        assert i == format(balance, '.2f')
    result = base.get_column_text("暂存位库存")
    for i in result:
        assert i == str(temporary_inventory)
    result = base.get_column_text("最新进价")
    for i in result:
        assert i == format(purchase_price, '.2f')
    result = base.get_column_text("成本价")
    for i in result:
        assert i == format(cost_price, '.2f')
    print(f"每个规格退货出库50个，验证可销售库存100个，库存100个， 余额2000， 暂存位库存100， ")
    purchase_order_id = purchase_interface.new_purchase_order("主仓库", "供应商1", stock_out_info)["ID"]
    purchase_interface.approve_purchase_order(purchase_order_id)
    base.wait_table_refresh(base.find_xpath("组合查询"), 1, "可销库存数")
    purchase_num = 0
    purchase_num += 50
    result = base.get_column_text("可销库存数")
    for i in result:
        assert i == str(marketability_inventory)
    result = base.get_column_text("库存预警值", "库存数")
    for i in result:
        assert i == str(inventory)
    result = base.get_column_text("余额")
    for i in result:
        assert i == format(balance, '.2f')
    result = base.get_column_text("暂存位库存")
    for i in result:
        assert i == str(temporary_inventory)
    result = base.get_column_text("最新进价")
    for i in result:
        assert i == format(purchase_price, '.2f')
    result = base.get_column_text("成本价")
    for i in result:
        assert i == format(cost_price, '.2f')
    result = base.get_column_text("采购在途数")
    for i in result:
        assert i == str(purchase_num)
    print(f"每个规格采购50个，不入库，验证可销售库存100个，库存100个， 余额2000， 暂存位库存100， 采购在途数是50")
    vip_name = base.get_now_string()
    vip_interface.new_vip(vip_name)
    sku_info = []
    # 还是通过sku_inf_list生成需要的商品信息列表
    for i in sku_code_list:
        sku_info.append({"商家编码": i, "数量": "10"})
    print(f"商品信息是{sku_info}")
    order_info = order_interface.new_order(vip_name, sku_info)
    order_id = order_info["ID"]
    order_code = order_info["Code"]
    print(f"创建订单单号:{order_code}")
    result = order_interface.approve_order(order_id)
    print(f"审核订单的信息是：{result}")
    delivery_order_id = delivery_interface.get_delivery_order_info({"模糊搜索": order_code}, ["ID"])[0]["ID"]
    print(f"发货单ID是{delivery_order_id}")
    delivery_interface.send_delivery(delivery_order_id)
    print(f"订单发货出库")
    sales_num = 10
    base.wait_table_refresh(base.find_xpath("组合查询"), 1, "可销库存数")
    marketability_inventory -= 10
    print(f"可销售库存是{marketability_inventory}")
    inventory -= 10
    print(f"库存是{inventory}")
    balance -= 200
    print(f"余额是{balance}")
    temporary_inventory -= 10
    print(f"暂存位库存是{temporary_inventory}")
    purchase_price = 20
    print(f"最新进价是{purchase_price}")
    cost_price = 20
    print(f"成本单价是{cost_price}")
    result = base.get_column_text("可销库存数")
    for i in result:
        assert i == str(marketability_inventory)
    result = base.get_column_text("库存预警值", "库存数")
    for i in result:
        assert i == str(inventory)
    result = base.get_column_text("余额")
    for i in result:
        assert i == format(balance, '.2f')
    result = base.get_column_text("暂存位库存")
    for i in result:
        assert i == str(temporary_inventory)
    result = base.get_column_text("最新进价")
    for i in result:
        assert i == format(purchase_price, '.2f')
    result = base.get_column_text("成本价")
    for i in result:
        assert i == format(cost_price, '.2f')
    result = base.get_column_text("采购在途数")
    for i in result:
        assert i == str(purchase_num)
    base.wait_element_click(base.find_xpath("刷新报表"))
    base.wait_element(base.find_xpath("刷新报表缓存", "确定"))
    time.sleep(1)
    base.wait_element_click(base.find_xpath("刷新报表缓存", "确定"))
    base.wait_element(base.find_xpath_by_tag_name("任务托管列表", "a"))
    time.sleep(1)
    base.wait_element_click(base.find_xpath_by_tag_name("任务托管列表", "a"))
    time.sleep(2)
    base.wait_table_refresh(base.find_xpath("组合查询"), 1, "三十天销量")
    result = base.get_column_text("三十天销量")
    for i in result:
        assert i == str(sales_num)
    result = base.get_column_text("七天销量")
    for i in result:
        assert i == str(sales_num)
    print(f"新建订单：{order_code},并发货出库,此时每个规格可销售库存减10，库存减10，余额减200，暂存位库存减10,销量加10，")
    base.scroll_to(4)
    print(f"再次新建订单，单不发货只审核，验证占用数增加10，销量增加10，其他不变")
    vip_name = base.get_now_string()
    vip_interface.new_vip(vip_name)
    print(f"商品信息是{sku_info}")
    order_info = order_interface.new_order(vip_name, sku_info)
    order_id = order_info["ID"]
    order_code = order_info["Code"]
    print(f"创建订单单号:{order_code}")
    result = order_interface.approve_order(order_id)
    print(f"审核订单的信息是：{result}")
    base.wait_table_refresh(base.find_xpath("组合查询"), 1, "可销库存数")
    marketability_inventory -= 10
    sales_num += 10
    occupy_num = 10
    result = base.get_column_text("可销库存数")
    for i in result:
        assert i == str(marketability_inventory)
    result = base.get_column_text("库存预警值", "库存数")
    for i in result:
        assert i == str(inventory)
    result = base.get_column_text("余额")
    for i in result:
        assert i == format(balance, '.2f')
    result = base.get_column_text("暂存位库存")
    for i in result:
        assert i == str(temporary_inventory)
    result = base.get_column_text("最新进价")
    for i in result:
        assert i == format(purchase_price, '.2f')
    result = base.get_column_text("成本价")
    for i in result:
        assert i == format(cost_price, '.2f')
    result = base.get_column_text("采购在途数")
    for i in result:
        assert i == str(purchase_num)
    base.wait_element_click(base.find_xpath("刷新报表"))
    base.wait_element(base.find_xpath("刷新报表缓存", "确定"))
    time.sleep(1)
    base.wait_element_click(base.find_xpath("刷新报表缓存", "确定"))
    base.wait_element(base.find_xpath_by_tag_name("任务托管列表", "a"))
    time.sleep(1)
    base.wait_element_click(base.find_xpath_by_tag_name("任务托管列表", "a"))
    time.sleep(2)
    base.wait_table_refresh(base.find_xpath("组合查询"), 1, "三十天销量")
    result = base.get_column_text("三十天销量")
    for i in result:
        assert i == str(sales_num)
    result = base.get_column_text("七天销量")
    for i in result:
        assert i == str(sales_num)
    result = base.get_column_text("占用数")
    for i in result:
        assert i == str(occupy_num)
    print(f"再次新建订单，不审核，验证占用数增加10，销量增加10，其他不变")
    vip_name = base.get_now_string()
    vip_interface.new_vip(vip_name)
    print(f"商品信息是{sku_info}")
    order_info = order_interface.new_order(vip_name, sku_info)
    order_id = order_info["ID"]
    order_code = order_info["Code"]
    print(f"创建订单单号:{order_code}")
    base.wait_table_refresh(base.find_xpath("组合查询"), 1, "可销库存数")
    marketability_inventory -= 10
    sales_num += 10
    occupy_num += 10
    result = base.get_column_text("可销库存数")
    for i in result:
        assert i == str(marketability_inventory)
    result = base.get_column_text("库存预警值", "库存数")
    for i in result:
        assert i == str(inventory)
    result = base.get_column_text("余额")
    for i in result:
        assert i == format(balance, '.2f')
    result = base.get_column_text("暂存位库存")
    for i in result:
        assert i == str(temporary_inventory)
    result = base.get_column_text("最新进价")
    for i in result:
        assert i == format(purchase_price, '.2f')
    result = base.get_column_text("成本价")
    for i in result:
        assert i == format(cost_price, '.2f')
    result = base.get_column_text("采购在途数")
    for i in result:
        assert i == str(purchase_num)
    base.wait_element_click(base.find_xpath("刷新报表"))
    base.wait_element(base.find_xpath("刷新报表缓存", "确定"))
    time.sleep(1)
    base.wait_element_click(base.find_xpath("刷新报表缓存", "确定"))
    base.wait_element(base.find_xpath_by_tag_name("任务托管列表", "a"))
    time.sleep(1)
    base.wait_element_click(base.find_xpath_by_tag_name("任务托管列表", "a"))
    time.sleep(2)
    base.wait_table_refresh(base.find_xpath("组合查询"), 1, "三十天销量")
    result = base.get_column_text("三十天销量")
    for i in result:
        assert i == str(sales_num)
    result = base.get_column_text("七天销量")
    for i in result:
        assert i == str(sales_num)
    result = base.get_column_text("占用数")
    for i in result:
        assert i == str(occupy_num)