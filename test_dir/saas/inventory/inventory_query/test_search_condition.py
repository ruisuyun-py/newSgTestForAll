import sys
import time
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
    base.open_page("库存", "库存查询", "库存查询框架")
    element = ''
    try:
        element = base.wait_element(base.find_xpath("刷新报表缓存", "天数"), 5)
    except AssertionError as ae:
        print(ae)
    if element != '':
        time.sleep(1)
        base.wait_element_click(base.find_xpath("刷新报表缓存", "取消"))


def setup_function():
    base.open_page("库存", "库存查询", "库存查询框架")


def teardown_function():
    base.close_page("库存查询")


def teardown_module():
    base.browser_close()


def test_brand_search_condition():
    brand_name_list = ["阿迪达斯", "安踏", "波司登"]
    for brand_name in brand_name_list:
        base.wait_element_click(base.find_xpath_by_placeholder("请选择品牌"))
        base.wait_element_click(base.find_xpath("品牌", brand_name))
        time.sleep(1)
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
        base.wait_element_click(base.find_xpath("选择供应商", "确定"))
        base.change_frame("库存查询框架")
        base.wait_element(base.find_xpath('组合查询'))
        time.sleep(1)
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


def test_product_name_search_condition():
    product_name_list = list(set(base.get_column_text("商品名称")))
    for product in product_name_list:
        if product == "":
            continue
        print(f"需要搜索的货号是：{product}")
        base.wait_element(base.find_xpath_by_placeholder("商品名称")).send_keys(Keys.CONTROL + 'a')
        base.wait_element(base.find_xpath_by_placeholder("商品名称")).send_keys(product)
        base.wait_table_refresh(base.find_xpath('组合查询'), 1, "货号")
        result_num = base.wait_element(base.find_xpath("已选择", "本页共")).text
        if result_num == '本页共0条数据':
            print(f"商品名称[{product}]没数据不用查看")
        else:
            result = base.get_column_text("商品名称")
            for i in result:
                assert product in i


def test_sku_name_search_condition():
    sku_name_list = list(set(base.get_column_text("规格名称")))
    for sku in sku_name_list:
        if sku == "":
            continue
        print(f"需要搜索的规格名称是：{sku}")
        base.wait_element(base.find_xpath_by_placeholder("规格名称")).send_keys(Keys.CONTROL + 'a')
        base.wait_element(base.find_xpath_by_placeholder("规格名称")).send_keys(sku)
        base.wait_table_refresh(base.find_xpath('组合查询'), 1, "货号")
        result_num = base.wait_element(base.find_xpath("已选择", "本页共")).text
        if result_num == '本页共0条数据':
            print(f"规格名称[{sku}]没数据不用查看")
        else:
            result = base.get_column_text("规格名称")
            for i in result:
                assert sku in i


def test_barcode_search_condition():
    print(f"先用商家编码获取条码单个搜索，再用货号批量搜索")
    sku_code_list = {
        "2009290026958",
        "2009290027054",
        "2009290026965",
        "2009290027061",
        "2009290026972",
        "2009290027078",
        "2009290026989",
        "2009290027085",
        "2009290027184",
        "2009290027160",
        "2009290027153",
        "2009290027146",
        "2009290027177",
        "2009290027092",
        "2009290027191",
        "2009290027108",
        "2009290027207",
        "2009290027115",
        "2009290027214",
    }
    for barcode in sku_code_list:
        print(f"需要搜索的商品条码是{barcode}")
        base.wait_element(base.find_xpath_by_placeholder("条码")).send_keys(Keys.CONTROL+'a')
        base.wait_element(base.find_xpath_by_placeholder("条码")).send_keys(barcode)
        time.sleep(1)
        base.wait_table_refresh(base.find_xpath("组合查询"), 1, "商家编码")
        result_num = base.wait_element(base.find_xpath("已选择", "本页共")).text
        if result_num == '本页共0条数据':
            print(f"商品条码[{barcode}]没数据不用查看")
        else:
            result = base.get_column_text("商品条码")
            for i in result:
                assert barcode == i

    base.wait_element(base.find_xpath_by_placeholder("条码")).send_keys(Keys.CONTROL + 'a')
    for barcode in sku_code_list:
        print(f"需要搜索的商品条码是{barcode}")
        base.wait_element(base.find_xpath_by_placeholder("条码")).send_keys(barcode)
        base.wait_element(base.find_xpath_by_placeholder("条码")).send_keys(Keys.ENTER)
    base.wait_table_refresh(base.find_xpath("组合查询"), 1, "商品条码")
    result_num = base.wait_element(base.find_xpath("已选择", "本页共")).text
    if result_num == '本页共0条数据':
        print(f"没数据不用查看")
    else:
        result = base.get_unique_column_text("商品条码")
        for i in result:
            assert i in sku_code_list


def test_category_search_condition():
    category_list = ["裤子", "上衣"]
    for category in category_list:
        print(f"本次搜索的分类:{category}")
        base.wait_element_click(base.find_xpath_by_placeholder("商品分类"))
        base.change_frame("选择分类")
        base.wait_element(base.find_xpath(category))
        time.sleep(1)
        base.wait_element_click(base.find_xpath(category))
        base.change_frame()
        base.wait_element_click(base.find_xpath("选择分类", "确定"))
        base.change_frame("库存查询框架")
        base.wait_table_refresh(base.find_xpath("组合查询"), 1, "商家编码")
        result_num = base.wait_element(base.find_xpath("已选择", "本页共")).text
        if result_num == '本页共0条数据':
            print(f"没数据不用查看")
        else:
            result = base.get_unique_column_text("货号")
            for product_code in result:
                category_result = product_interface.get_sku_info(product_code)["data"]["Items"][0]["ProductCategory"]
                print(f"本次搜索的货号:{product_code}的分类是{category_result}")
                assert category_result == category


def test_bin_name_search_condition():
    bin_name_list = ["A", "A1", "A1-2", "A1-2-", "A1-2-1"]
    time.sleep(1)
    for b in bin_name_list:
        base.wait_element(base.find_xpath_by_placeholder("固定库位")).send_keys(Keys.CONTROL+'a')
        base.wait_element(base.find_xpath_by_placeholder("固定库位")).send_keys(b)
        base.wait_table_refresh(base.find_xpath("组合查询"), 1, "货号")
        result = base.get_column_text("固定库位")
        for i in result:
            assert b in i, f"库存查询页面固定库位搜索条件失效，输入库位{b}之后搜索结果不正确"


def test_inventory_search_condition():
    base.wait_element(base.find_xpath_by_placeholder("库存大于等于")).send_keys(Keys.CONTROL + 'a')
    base.wait_element(base.find_xpath_by_placeholder("库存大于等于")).send_keys(100)
    base.wait_element(base.find_xpath_by_placeholder("库存小于")).send_keys(Keys.CONTROL + 'a')
    base.wait_element(base.find_xpath_by_placeholder("库存小于")).send_keys(1000)
    base.wait_text_locate(base.find_xpath_by_placeholder("库存小于"), "1000")
    time.sleep(1)
    base.wait_table_refresh(base.find_xpath("组合查询"), 1, "货号")
    result = base.get_column_text("库存预警值", "库存数")
    for i in result:
        assert 100 <= int(i) < 1000


def test_marketability_inventory():
    time.sleep(1)
    base.wait_element(base.find_xpath_by_placeholder("可销库存数大于等于")).send_keys(Keys.CONTROL + 'a')
    base.wait_element(base.find_xpath_by_placeholder("可销库存数大于等于")).send_keys(100)
    base.wait_element(base.find_xpath_by_placeholder("可销库存数小于")).send_keys(Keys.CONTROL + 'a')
    base.wait_element(base.find_xpath_by_placeholder("可销库存数小于")).send_keys(1000)
    base.wait_table_refresh(base.find_xpath("组合查询"), 1, "货号")
    result = base.get_column_text("可销库存数")
    for i in result:
        assert 100 <= int(i) < 1000


def test_show_zero_inventory_search_condition():
    time.sleep(1)
    base.wait_element_click(base.find_xpath("显示0库存", "是"))
    base.wait_table_refresh(base.find_xpath("组合查询"), 1, "货号")
    result = base.get_column_text("库存预警值", "库存数")
    for i in result:
        assert i == "0"
    base.wait_element_click(base.find_xpath("显示0库存", "否"))
    base.wait_table_refresh(base.find_xpath("组合查询"), 1, "货号")
    result = base.get_column_text("库存预警值", "库存数")
    for i in result:
        assert i != "0"


if __name__ == '__main__':
    pytest.main()


