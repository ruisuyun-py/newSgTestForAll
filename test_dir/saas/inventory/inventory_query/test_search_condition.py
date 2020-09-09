import sys
from os.path import dirname, abspath
import pytest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import page.login_page as login
import page.base_page as base
import interface.order.delivery_order_interface as delivery_interface
import interface.supplier.supplier_interface as supplier_interface
import interface.purchase.purchase_interface as purchase_interface
import interface.product.product_interface as product_interface
import interface.inventory.inventory_interface as inventory_interface
import interface.order.order_interface as order_interface
import interface.vip.vip_interface as vip_interface
import interface.pda.pda_interface as pda_interface
import interface.setting.setting_interface as setting_interface

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


def test_brand_search_condition():
    brand_name_list = ["阿迪达斯", "安踏", "波司登"]
    for brand_name in brand_name_list:
        base.wait_element_click(base.find_xpath_by_tag_name("品牌", "select"))
        base.wait_element_click(base.find_xpath(brand_name))
        base.wait_table_refresh(base.find_xpath('组合查询'), 1, "货号")
        result_num = base.wait_element(base.find_xpath("已选择", "本页共")).text
        if result_num == '本页共0条数据':
            print(f"品牌[{brand_name}]没数据不用查看")
        else:
            result = base.get_column_text("商家编码")
            for i in result:
                brand_name = product_interface.get_sku_info(i)["data"]["Items"][0]["BrandName"]
                assert brand_name == brand_name


def test_supplier_name_search_condition():
    supplier_name_list = ["供应商1", "供应商2", "供应商3", "供应商4", "供应商5"]
    for supplier_name in supplier_name_list:
        base.wait_element_click(base.find_xpath_by_placeholder("供应商"))
        base.change_frame("选择供应商")
        base.chose_supplier_by_text(supplier_name)
        base.change_frame()
        base.wait_element_click(base.find_xpath("选择供应商", "确认"))
        base.change_frame("库存查询框架")
        base.wait_table_refresh(base.find_xpath('组合查询'), 1, "货号")
        result_num = base.wait_element(base.find_xpath("已选择", "本页共")).text
        if result_num == '本页共0条数据':
            print(f"供应商[{supplier_name}]没数据不用查看")
        else:
            result = base.get_column_text("商家编码")
            for i in result:
                if "+" in i:
                    continue
                print(f"需要校验供应商的商家编码：{i}")
                name = product_interface.get_sku_info(i)["data"]["Items"][0]["SupplierName"]
                assert supplier_name == name


def test_sku_code_search_condition():
    sku_code_list = base.get_column_text("商家编码")
    for sku in sku_code_list:
        print(f"需要搜索的商家编码是：{sku}")
        base.wait_element(base.find_xpath_by_placeholder("商家编码")).send_keys(Keys.CONTROL+'a')
        base.wait_element(base.find_xpath_by_placeholder("商家编码")).send_keys(sku)
        base.wait_table_refresh(base.find_xpath('组合查询'), 1, "货号")
        result_num = base.wait_element(base.find_xpath("已选择", "本页共")).text
        if result_num == '本页共0条数据':
            print(f"商家编码[{sku}]没数据不用查看")
        else:
            result = base.get_column_text("商家编码")
            for i in result:
                assert sku in i


def test_product_code_search_condition():
    product_code_list = list(set(base.get_column_text("货号")))
    for product in product_code_list:
        if product == "":
            continue
        print(f"需要搜索的货号是：{product}")
        base.wait_element(base.find_xpath_by_placeholder("货号")).send_keys(Keys.CONTROL + 'a')
        base.wait_element(base.find_xpath_by_placeholder("货号")).send_keys(product)
        base.wait_table_refresh(base.find_xpath('组合查询'), 1, "货号")
        result_num = base.wait_element(base.find_xpath("已选择", "本页共")).text
        if result_num == '本页共0条数据':
            print(f"货号[{product}]没数据不用查看")
        else:
            result = base.get_column_text("货号")
            for i in result:
                assert product in i


if __name__ == '__main__':
    pytest.main()


