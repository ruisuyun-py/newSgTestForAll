import sys
import time
import copy
import pytest
from os.path import dirname, abspath
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import page.login_page as login
import page.base_page as base
import page.interface as interface

sys.path.insert(0, dirname(dirname(dirname(abspath(__file__)))))


def setup_module():
    base.driver = webdriver.Chrome()
    base.cookies = login.login()
    print("预设会员价明细测试开始")


def setup_function():
    base.open_page("会员", "预设会员价明细", "预设会员价明细框架")


def teardown_function():
    base.close_page("预设会员价明细")


def teardown_module():
    base.browser_close()
    print("预设会员价明细测试结束")


# 验证预设会员价页面在修改时记录预设价格设置下（直接记录的模式后期基本就替代掉了）能否正确显示数据
def test_vip_price_detail():
    # 先确定下设置
    setting_info = {
        "记录会员上次交易价：手工单或者门店单保存时，记录会员的商品交易价格": "true",
        "记录会员上次交易价 同款同价：手工单或者门店单保存时，记录会员的商品交易价格 同款同价": "false",
        "只有手工修改售价才会记录预设价格": "true",
    }
    interface.save_order_setting(setting_info)
    print("这就为了换个行")
    print("非同款同价模式+修改才记录会员价设置完成，修改设置之后等5秒，让设置生效")
    time.sleep(5)
    base.close_page("预设会员价明细")
    base.open_page("会员", "预设会员价明细", "预设会员价明细框架")
    # 新建会员
    vip_name = base.get_now_string()
    print(f"新建一个会员，会员名称：{vip_name}")
    interface.new_vip(vip_name)
    print(f"新建的会员：{vip_name}在预设会员价页面没有任何记录")
    # 查询确认新会员没有任何记录
    base.wait_element(base.find_xpath_by_placeholder("会员")).click()
    base.change_frame("预设会员价明细框架")
    base.switch_to_frame(base.find_frame("选择会员"))
    base.chose_vip(vip_name)
    base.change_frame("预设会员价明细框架")
    base.wait_element(base.find_xpath("本页共0条数据"))
    print(f"新建会员：{vip_name}确定在预设会员价页面没有任何记录")
    # 新建商品
    product_code = base.get_now_string()
    print(f"新建商品货号：{product_code}")
    # 新建商品
    interface.new_product(product_code)
    # 获取一个sku_code查看会员价格
    sku_code = interface.get_sku_code(product_code)[0]
    print(f"取出一个商品：{sku_code}查看售价，此时售价应该为0")
    with base.operate_page("订单", "门店收银", "门店收银框架") as e:
        base.change_frame("门店收银框架", "选择会员")
        base.chose_vip(vip_name)
        base.change_frame("门店收银框架")
        base.wait_element_focus(base.find_xpath_by_placeholder("请扫描商品条码"))
        base.wait_element(base.find_xpath_by_placeholder("商品货号")).send_keys(product_code)
        base.wait_element(base.find_xpath("搜索")).click()
        time.sleep(1)
        base.wait_element(base.find_xpath(product_code)).click()
        base.change_frame("门店收银框架")
        base.switch_to_frame(base.find_frame("商品选择"))
        price = base.wait_element(base.get_old_cell_xpath("红色 XS", "交易价格")).get_attribute("value")
        assert price == '0'
    print(f"确定{sku_code}的售价是0")
    # 设置商品的标准售价，第二价格，第三价格，第四价格
    interface.modify_sku_price(sku_code, "100", "200", "300", "400")
    print(f"设置{sku_code}的价格分别为100,200,300,400，此时商品的价格应该是100")
    # 再次到门店开单页面查看售价是否是标准售价=100
    with base.operate_page("订单", "门店收银", "门店收银框架") as e:
        base.change_frame("门店收银框架", "选择会员")
        base.chose_vip(vip_name)
        base.change_frame("门店收银框架")
        base.wait_element_focus(base.find_xpath_by_placeholder("请扫描商品条码"))
        base.wait_element(base.find_xpath_by_placeholder("商品货号")).send_keys(product_code)
        base.wait_element(base.find_xpath("搜索")).click()
        time.sleep(1)
        base.wait_element(base.find_xpath(product_code)).click()
        base.change_frame("门店收银框架")
        base.switch_to_frame(base.find_frame("商品选择"))
        price = base.wait_element(base.get_old_cell_xpath("红色 XS", "交易价格")).get_attribute("value")
        assert price == '100'
    print(f"确定{sku_code}的售价是100")
    # 设置会员等级为8折，再次查看售价是否是80
    print(f"将会员{vip_name}的会员等级设置为8折，此时售价应该是100*0.8")
    vip_level = "8折"
    interface.modify_vip_level(vip_name, vip_level)
    with base.operate_page("订单", "门店收银", "门店收银框架") as e:
        base.change_frame("门店收银框架", "选择会员")
        base.chose_vip(vip_name)
        base.change_frame("门店收银框架")
        base.wait_element_focus(base.find_xpath_by_placeholder("请扫描商品条码"))
        base.wait_element(base.find_xpath_by_placeholder("商品货号")).send_keys(product_code)
        base.wait_element(base.find_xpath("搜索")).click()
        time.sleep(1)
        base.wait_element(base.find_xpath(product_code)).click()
        base.change_frame("门店收银框架")
        base.switch_to_frame(base.find_frame("商品选择"))
        price = base.wait_element(base.get_old_cell_xpath("红色 XS", "交易价格")).get_attribute("value")
        assert price == '80'
    print(f"确定会员：{vip_name}商品{sku_code}的售价是80")
    # 门店开单，不修改商品价格，还是没有记录
    # sku_info_list 商品信息列表
    sku_info_list = []
    sku_info = {}
    product_info = interface.get_sku_info('', product_code)
    i = 1
    for sku in product_info["data"]["Items"]:
        sku_info["SkuCode"] = sku["SkuCode"]
        i += 1
        sku_info["Qty"] = i
        sku_info["Price"] = int(sku["StandardPrice"]) * int(
            interface.get_vip_level_info(vip_level)["data"]["Items"][0]["Discount"]) / 10
        sku_info_list.append(dict(sku_info))
    print("不改变任何sku价格是商品明细列表信息：")
    for i in sku_info_list:
        print(i)
    print("不修改sku价格，预设会员价明细页面不应该有任何记录")
    # 商品数据确定之后直接开单
    interface.new_pos_oder(vip_name, sku_info_list)
    # 再次核对预设会员价明细页面还是0
    base.open_page("会员", "预设会员价明细", "预设会员价明细框架")
    base.wait_element(base.find_xpath_by_placeholder("会员")).click()
    base.change_frame("预设会员价明细框架")
    base.switch_to_frame(base.find_frame("选择会员"))
    base.chose_vip(vip_name)
    base.change_frame("预设会员价明细框架")
    time.sleep(1)
    base.wait_element(base.find_xpath("本页共0条数据"))
    print("确定不修改售价不会有任何记录")
    # 再次开单，修改其中一个规则的价格，必须有一条记录
    # 修改商品信息
    modify_info = {}
    for i in range(0, 1):
        modify_sku_code = sku_info_list[i]["SkuCode"]
        modify_price = sku_info_list[i]["Price"] + 10
        sku_info_list[i]["Price"] = copy.copy(modify_price)
        modify_info[modify_sku_code] = modify_price
    for k, v in modify_info.items():
        print(f"修改{k}的价格为{v}")
    for i in sku_info_list:
        print(i)
    print("修改一个商品的售价之后，预设会员价明细页面应该有一条记录")
    # 商品数据确定之后直接开单
    interface.new_pos_oder(vip_name, sku_info_list)
    # 再次核对预设会员价明细页面有一条记录
    base.open_page("会员", "预设会员价明细", "预设会员价明细框架")
    base.wait_element(base.find_xpath_by_placeholder("会员")).click()
    base.change_frame("预设会员价明细框架")
    base.switch_to_frame(base.find_frame("选择会员"))
    base.chose_vip(vip_name)
    base.change_frame("预设会员价明细框架")
    time.sleep(2)
    base.wait_element(base.find_xpath("本页共1条数据"))
    result = base.get_column_text("商家编码")
    assert len(result) == 1
    for r in result:
        assert r in modify_info.keys()
        vip_price = base.wait_element(base.get_cell_xpath(r, "预设价格")).text
        assert float(modify_info[r]) == float(vip_price)
    print("修改一个商品的售价之后，预设会员价页面记录的只有一条记录，并且sku_code，预设价格核对无误")
    # 修改两个规格的价格，预设会员价明细页面会有两条明细
    # 还是先修改商品价格
    modify_info.clear()
    j = 10
    for i in range(0, 2):
        modify_sku_code = sku_info_list[i]["SkuCode"]
        j += 7
        modify_price = sku_info_list[i]["Price"] + j
        sku_info_list[i]["Price"] = modify_price
        modify_info[modify_sku_code] = modify_price
    for k, v in modify_info.items():
        print(f"修改{k}的价格为{v}")
    print("修改两个sku价格之后的商品信息列表是：")
    for i in sku_info_list:
        print(i)
    print("修改两个商品价格之后开单，会员预设价页面应该有两条数据")
    # 商品数据确定之后直接开单
    interface.new_pos_oder(vip_name, sku_info_list)
    # 再次核对预设会员价明细页面有两条记录
    base.open_page("会员", "预设会员价明细", "预设会员价明细框架")
    base.wait_element(base.find_xpath_by_placeholder("会员")).click()
    base.change_frame("预设会员价明细框架")
    base.switch_to_frame(base.find_frame("选择会员"))
    base.chose_vip(vip_name)
    base.change_frame("预设会员价明细框架")
    time.sleep(1)
    base.wait_element(base.find_xpath("本页共2条数据"))
    result = base.get_column_text("商家编码")
    assert len(result) == 2
    for r in result:
        assert r in modify_info.keys()
        vip_price = base.wait_element(base.get_cell_xpath(r, "预设价格")).text
        assert float(modify_info[r]) == float(vip_price)
    print("修改两个商品之后开单，会员预设价页面只有两条记录,商家编码，预设价格经核实无误")
    # 全部更改则需要显示全部该商品的全部记录
    modify_info.clear()
    for i in sku_info_list:
        modify_sku_code = i["SkuCode"]
        j += 5
        modify_price = i["Price"] + j
        i["Price"] = modify_price
        modify_info[modify_sku_code] = modify_price
    for k, v in modify_info.items():
        print(f"修改{k}的价格为：{v}")
    print("修改全部商品价格之后的商品信息列表是：")
    for i in sku_info_list:
        print(i)
    print("修改全部商品的价格之后，预设会员价页面应该有该款所有商品的记录")
    # 商品数据确定之后直接开单
    interface.new_pos_oder(vip_name, sku_info_list)
    # 再次核对预设会员价明细页面有两条记录
    base.open_page("会员", "预设会员价明细", "预设会员价明细框架")
    base.wait_element(base.find_xpath_by_placeholder("会员")).click()
    base.change_frame("预设会员价明细框架")
    base.switch_to_frame(base.find_frame("选择会员"))
    base.chose_vip(vip_name)
    base.change_frame("预设会员价明细框架")
    time.sleep(1)
    base.wait_element(base.find_xpath(f"本页共{len(sku_info_list)}条数据"))
    result = base.get_column_text("商家编码")
    assert len(result) == len(sku_info_list)
    for r in result:
        assert r in modify_info.keys()
        vip_price = base.wait_element(base.get_cell_xpath(r, "预设价格")).text
        assert float(modify_info[r]) == float(vip_price)
    print("预设会员价页面有该款商品的全部记录，并且商家编码预设价格核对无误")
    print("在选择会员的情况下，核实下标准售价，第二价格，第三价格，第四价格，会员价格取值是否正确")
    result = base.get_column_text("标准售价")
    for r in result:
        print(f"标准售价应该是100实际是：{r},")
        assert r == '100'
    result = base.get_column_text("第二价格")
    for r in result:
        print(f"第二价格应该是200实际是：{r},")
        assert r == '200'
    result = base.get_column_text("第三价格")
    for r in result:
        print(f"第三价格应该是300实际是：{r},")
        assert r == '300'
    result = base.get_column_text("第四价格")
    for r in result:
        print(f"第四价格应该是400实际是：{r},")
        assert r == '400'
    result = base.get_column_text("会员价")
    for r in result:
        print(f"会员价应该是80实际是：{r},")
        assert r == '80'
    print("确定在选择会员的情况下，核实下标准售价，第二价格，第三价格，第四价格，会员价格取值是否正确")
    print("清空搜索条件之后，搜索货号，查看所有价格的取值是否正确")
    base.wait_table_refresh(base.find_xpath("清空"), 1, "货号")
    base.wait_element_click(base.find_xpath_by_placeholder("商品货号")).send_keys(product_code)
    base.wait_table_refresh(base.find_xpath("组合查询"), 1, "货号")
    result = base.get_column_text("标准售价")
    for r in result:
        print(f"标准售价应该是100实际是：{r},")
        assert r == '100'
    result = base.get_column_text("第二价格")
    for r in result:
        print(f"第二价格应该是200实际是：{r},")
        assert r == '200'
    result = base.get_column_text("第三价格")
    for r in result:
        print(f"第三价格应该是300实际是：{r},")
        assert r == '300'
    result = base.get_column_text("第四价格")
    for r in result:
        print(f"第四价格应该是400实际是：{r},")
        assert r == '400'
    result = base.get_column_text("会员价")
    for r in result:
        print(f"会员价应该是80实际是：{r},")
        assert r == '80'
    print("确定清空搜索条件之后，搜索货号，查看所有价格的取值是否正确")
    # 修改设置，再来一遍
    print("修改设置为同款同价再跑一遍")
    print("修改设置为同款同价再跑一遍")
    print("修改设置为同款同价再跑一遍")
    setting_info = {
        "记录会员上次交易价：手工单或者门店单保存时，记录会员的商品交易价格": "true",
        "记录会员上次交易价 同款同价：手工单或者门店单保存时，记录会员的商品交易价格 同款同价": "true",
        "只有手工修改售价才会记录预设价格": "true",
    }
    interface.save_order_setting(setting_info)
    print("同款同价模式且只有修改时记录会员价格设置完成，")
    print("修改设置之后等待5秒等设置生效")
    time.sleep(5)
    base.close_page("预设会员价明细")
    base.open_page("会员", "预设会员价明细", "预设会员价明细框架")
    # 新建会员
    vip_name = base.get_now_string()
    print(f"新建会员会员名称：{vip_name}")
    interface.new_vip(vip_name)
    # 查询确认新会员没有任何记录
    base.wait_element(base.find_xpath_by_placeholder("会员")).click()
    base.change_frame("预设会员价明细框架")
    base.switch_to_frame(base.find_frame("选择会员"))
    base.chose_vip(vip_name)
    base.change_frame("预设会员价明细框架")
    base.wait_element(base.find_xpath("本页共0条数据"))
    # 新建商品
    product_code = base.get_now_string()
    print(f"新建商品货号：{product_code}")
    # 解析出第一个skuCode
    print("验证没有设置价格时，售价为0")
    sku_code = interface.new_product(product_code)["data"]["ProductSkus"][0]["Code"]
    with base.operate_page("订单", "门店收银", "门店收银框架") as e:
        base.change_frame("门店收银框架", "选择会员")
        base.chose_vip(vip_name)
        base.change_frame("门店收银框架")
        base.wait_element_focus(base.find_xpath_by_placeholder("请扫描商品条码"))
        base.wait_element(base.find_xpath_by_placeholder("商品货号")).send_keys(product_code)
        base.wait_element(base.find_xpath("搜索")).click()
        time.sleep(1)
        base.wait_element(base.find_xpath(product_code)).click()
        base.change_frame("门店收银框架")
        base.switch_to_frame(base.find_frame("商品选择"))
        price = base.wait_element(base.get_old_cell_xpath("红色 XS", "交易价格")).get_attribute("value")
        assert price == '0'
    print("确定没有设置价格时，售价为0")
    # 设置商品的标准售价，第二价格，第三价格，第四价格
    interface.modify_sku_price(sku_code, "100", "200", "300", "400")
    # 再次到门店开单页面查看售价是否是标准售价=100
    print("验证标准售价设置为100，之后售价应该为100")
    with base.operate_page("订单", "门店收银", "门店收银框架") as e:
        base.change_frame("门店收银框架", "选择会员")
        base.chose_vip(vip_name)
        base.change_frame("门店收银框架")
        base.wait_element_focus(base.find_xpath_by_placeholder("请扫描商品条码"))
        base.wait_element(base.find_xpath_by_placeholder("商品货号")).send_keys(product_code)
        base.wait_element(base.find_xpath("搜索")).click()
        time.sleep(1)
        base.wait_element(base.find_xpath(product_code)).click()
        base.change_frame("门店收银框架")
        base.switch_to_frame(base.find_frame("商品选择"))
        price = base.wait_element(base.get_old_cell_xpath("红色 XS", "交易价格")).get_attribute("value")
        assert price == '100'
    print("确定标准售价设置为100，之后售价应该为100")
    print("验证会员等级设置为8折之后，售价应该是80")
    # 设置会员等级为8折，再次查看售价是否是80
    vip_level = "8折"
    interface.modify_vip_level(vip_name, vip_level)
    with base.operate_page("订单", "门店收银", "门店收银框架") as e:
        base.change_frame("门店收银框架", "选择会员")
        base.chose_vip(vip_name)
        base.change_frame("门店收银框架")
        base.wait_element_focus(base.find_xpath_by_placeholder("请扫描商品条码"))
        base.wait_element(base.find_xpath_by_placeholder("商品货号")).send_keys(product_code)
        base.wait_element(base.find_xpath("搜索")).click()
        time.sleep(1)
        base.wait_element(base.find_xpath(product_code)).click()
        base.change_frame("门店收银框架")
        base.switch_to_frame(base.find_frame("商品选择"))
        price = base.wait_element(base.get_old_cell_xpath("红色 XS", "交易价格")).get_attribute("value")
        assert price == '80'
    print("确定会员等级设置为8折之后，售价应该是80")
    # 门店开单，不修改商品价格，还是没有记录
    # sku_info_list 商品信息列表
    sku_info_list = []
    sku_info = {}
    product_info = interface.get_sku_info('', product_code)
    i = 1
    for sku in product_info["data"]["Items"]:
        sku_info["SkuCode"] = sku["SkuCode"]
        i += 1
        sku_info["Qty"] = i
        sku_info["Price"] = int(sku["StandardPrice"]) * int(
            interface.get_vip_level_info(vip_level)["data"]["Items"][0]["Discount"]) / 10
        sku_info_list.append(dict(sku_info))
    print("不改变任何sku价格是商品明细列表信息：")
    for i in sku_info_list:
        print(i)
    print("验证不改变商品售价时，预设会员价页面没有记录")
    # 商品数据确定之后直接开单
    interface.new_pos_oder(vip_name, sku_info_list)
    # 再次核对预设会员价明细页面还是0
    base.open_page("会员", "预设会员价明细", "预设会员价明细框架")
    base.wait_element(base.find_xpath_by_placeholder("会员")).click()
    base.change_frame("预设会员价明细框架")
    base.switch_to_frame(base.find_frame("选择会员"))
    base.chose_vip(vip_name)
    base.change_frame("预设会员价明细框架")
    time.sleep(1)
    base.wait_element(base.find_xpath("本页共0条数据"))
    # 再次开单，修改其中一个规则的价格，必须有一条记录
    print("确定不改变商品售价时，预设会员价页面没有记录")
    print("验证修改一个商品售价之后，预设会员价页面有该款记录")
    # 修改商品信息
    modify_info = {}
    for i in range(0, 1):
        modify_sku_code = sku_info_list[i]["SkuCode"]
        modify_price = sku_info_list[i]["Price"] + 10
        sku_info_list[i]["Price"] = copy.copy(modify_price)
        modify_info[modify_sku_code] = modify_price
    for k, v in modify_info.items():
        print(f"修改{k}的价格为{v}")
    for i in sku_info_list:
        print(i)
    # 商品数据确定之后直接开单
    interface.new_pos_oder(vip_name, sku_info_list)
    # 再次核对预设会员价明细页面有一条记录
    base.open_page("会员", "预设会员价明细", "预设会员价明细框架")
    base.wait_element(base.find_xpath_by_placeholder("会员")).click()
    base.change_frame("预设会员价明细框架")
    base.switch_to_frame(base.find_frame("选择会员"))
    base.chose_vip(vip_name)
    base.change_frame("预设会员价明细框架")
    time.sleep(2)
    base.wait_element(base.find_xpath("本页共1条数据"))
    result = base.get_column_text("货号")
    assert len(result) == 1
    for r in result:
        assert r == product_code
        vip_price = base.wait_element(base.get_cell_xpath(r, "预设价格")).text
        assert float(vip_price) in modify_info.values()
    print("确定修改一个商品售价之后，预设会员价页面有该款记录")
    print("修改整款商品价格之后，预设会员价页面也只有一个价格")
    # 修改所有商品价格
    modify_info.clear()
    for i in sku_info_list:
        modify_sku_code = i["SkuCode"]
        j += 5
        modify_price = 195
        i["Price"] = modify_price
        modify_info[modify_sku_code] = modify_price
    for k, v in modify_info.items():
        print(f"修改{k}的价格为：{v}")
    print("修改全部商品价格之后的商品信息列表是：")
    for i in sku_info_list:
        print(i)
    # 商品数据确定之后直接开单
    interface.new_pos_oder(vip_name, sku_info_list)
    base.open_page("会员", "预设会员价明细", "预设会员价明细框架")
    base.wait_element(base.find_xpath_by_placeholder("会员")).click()
    base.change_frame("预设会员价明细框架")
    base.switch_to_frame(base.find_frame("选择会员"))
    base.chose_vip(vip_name)
    base.change_frame("预设会员价明细框架")
    time.sleep(1)
    base.wait_element(base.find_xpath("本页共1条数据"))
    result = base.get_column_text("货号")
    assert len(result) == 1
    for r in result:
        assert r == product_code
        vip_price = base.wait_element(base.get_cell_xpath(r, "预设价格")).text
        assert float(vip_price) in modify_info.values()
    print("修改整款商品价格之后，预设会员价页面也只有一个价格")
    print("预设会员价页面有该款商品的全部记录，并且商家编码预设价格核对无误")
    print("在选择会员的情况下，核实下标准售价，第二价格，第三价格，第四价格，会员价格取值是否正确")
    result = base.get_column_text("标准售价")
    for r in result:
        print(f"标准售价应该是100实际是：{r},")
        assert r == '100'
    result = base.get_column_text("第二价格")
    for r in result:
        print(f"第二价格应该是200实际是：{r},")
        assert r == '200'
    result = base.get_column_text("第三价格")
    for r in result:
        print(f"第三价格应该是300实际是：{r},")
        assert r == '300'
    result = base.get_column_text("第四价格")
    for r in result:
        print(f"第四价格应该是400实际是：{r},")
        assert r == '400'
    result = base.get_column_text("会员价")
    for r in result:
        print(f"会员价应该是80实际是：{r},")
        assert r == '80'
    print("确定在选择会员的情况下，核实下标准售价，第二价格，第三价格，第四价格，会员价格取值是否正确")
    print("清空搜索条件之后，搜索货号，查看所有价格的取值是否正确")
    base.wait_table_refresh(base.find_xpath("清空"), 1, "货号")
    base.wait_element_click(base.find_xpath_by_placeholder("商品货号")).send_keys(product_code)
    base.wait_table_refresh(base.find_xpath("组合查询"), 1, "货号")
    result = base.get_column_text("标准售价")
    for r in result:
        print(f"标准售价应该是100实际是：{r},")
        assert r == '100'
    result = base.get_column_text("第二价格")
    for r in result:
        print(f"第二价格应该是200实际是：{r},")
        assert r == '200'
    result = base.get_column_text("第三价格")
    for r in result:
        print(f"第三价格应该是300实际是：{r},")
        assert r == '300'
    result = base.get_column_text("第四价格")
    for r in result:
        print(f"第四价格应该是400实际是：{r},")
        assert r == '400'
    result = base.get_column_text("会员价")
    for r in result:
        print(f"会员价应该是80实际是：{r},")
        assert r == '80'
    print("确定清空搜索条件之后，搜索货号，查看所有价格的取值是否正确")


def test_search_condition():
    # 先确定下设置
    setting_info = {
        "记录会员上次交易价：手工单或者门店单保存时，记录会员的商品交易价格": "true",
        "记录会员上次交易价 同款同价：手工单或者门店单保存时，记录会员的商品交易价格 同款同价": "false",
        "只有手工修改售价才会记录预设价格": "true",
    }
    interface.save_order_setting(setting_info)
    print("这就为了换个行")
    print("非同款同价模式+修改才记录会员价设置完成，修改设置之后等5秒，让设置生效")
    time.sleep(5)
    base.close_page("预设会员价明细")
    base.open_page("会员", "预设会员价明细", "预设会员价明细框架")
    print("测试商品货号测试条件")
    base.wait_element_click(base.find_xpath_by_placeholder("商品货号")).send_keys("测试商品1")
    base.wait_table_refresh(base.find_xpath("组合查询"), 1, "商家编码")
    product_code_list = base.get_column_text("货号")
    for i in product_code_list:
        assert i == "测试商品1"
    print("清空搜索条件")
    base.wait_table_refresh(base.find_xpath("清空"), 1, "商家编码")
    print("验证预设会员价范围条件是否生效")
    print("先测试大于会员价")
    base.wait_element_click(base.find_xpath_with_spaces("大于会员价格"))
    base.wait_table_refresh(base.find_xpath("组合查询"), 1, "商家编码")
    for i in range(1, 10):
        vip_price = base.wait_element(base.get_cell_xpath(i, "会员价")).text
        preset_price = base.wait_element(base.get_cell_xpath(i, "预设价格")).text
        assert float(preset_price) > float(vip_price)
    print("再测试小于会员价")
    base.wait_element_click(base.find_xpath_with_spaces("小于会员价格"))
    base.wait_table_refresh(base.find_xpath("组合查询"), 1, "商家编码")
    for i in range(1, 10):
        vip_price = base.wait_element(base.get_cell_xpath(i, "会员价")).text
        preset_price = base.wait_element(base.get_cell_xpath(i, "预设价格")).text
        assert float(preset_price) < float(vip_price)
    print("再测试等于会员价")
    base.wait_element_click(base.find_xpath_with_spaces("等于会员价格"))
    base.wait_table_refresh(base.find_xpath("组合查询"), 1, "商家编码")
    for i in range(1, 10):
        vip_price = base.wait_element(base.get_cell_xpath(i, "会员价")).text
        preset_price = base.wait_element(base.get_cell_xpath(i, "预设价格")).text
        assert float(preset_price) == float(vip_price)
    print("清空搜索条件")
    base.wait_table_refresh(base.find_xpath("清空"), 1, "商家编码")
    print("测试价格差异")
    base.wait_element(base.find_xpath_by_placeholder("价格差异大于等于")).send_keys("10")
    base.wait_element(base.find_xpath_by_placeholder("价格差异小于")).send_keys("50")
    base.wait_table_refresh(base.find_xpath("组合查询"), 1, "商家编码")
    vip_price = base.wait_element(base.get_cell_xpath(i, "会员价")).text
    preset_price = base.wait_element(base.get_cell_xpath(i, "预设价格")).text
    assert 10.0 <= abs(float(preset_price)-float(vip_price)) <= 50.0
    print("清空搜索条件")
    base.wait_table_refresh(base.find_xpath("清空"), 1, "商家编码")
    print("测试价格差异百分比")
    base.wait_element(base.find_xpath_by_placeholder("价格差异百分比大于等于")).send_keys("10")
    base.wait_element(base.find_xpath_by_placeholder("价格差异百分比小于")).send_keys("50")
    base.wait_table_refresh(base.find_xpath("组合查询"), 1, "商家编码")
    for i in range(1, 10):
        vip_price = base.wait_element(base.get_cell_xpath(i, "会员价")).text
        preset_price = base.wait_element(base.get_cell_xpath(i, "预设价格")).text
        if float(vip_price) >= float(preset_price):
            higher_price = float(vip_price)
        else:
            higher_price = float(preset_price)
        assert 10.0 <= abs(float(preset_price) - float(vip_price))/higher_price*100 <= 50.0
    # 先确定下设置
    print("修改设置为同款同价，修改时才记录预设价格")
    print("修改设置为同款同价，修改时才记录预设价格")
    print("修改设置为同款同价，修改时才记录预设价格")
    setting_info = {
        "记录会员上次交易价：手工单或者门店单保存时，记录会员的商品交易价格": "true",
        "记录会员上次交易价 同款同价：手工单或者门店单保存时，记录会员的商品交易价格 同款同价": "true",
        "只有手工修改售价才会记录预设价格": "true",
    }
    interface.save_order_setting(setting_info)
    print("非同款同价模式+修改才记录会员价设置完成，修改设置之后等5秒，让设置生效")
    time.sleep(5)
    base.close_page("预设会员价明细")
    base.open_page("会员", "预设会员价明细", "预设会员价明细框架")
    print("测试商品货号测试条件")
    base.wait_element_click(base.find_xpath_by_placeholder("商品货号")).send_keys("测试商品1")
    base.wait_table_refresh(base.find_xpath("组合查询"), 1, "货号")
    product_code_list = base.get_column_text("货号")
    for i in product_code_list:
        assert i == "测试商品1"
    print("清空搜索条件")
    base.wait_table_refresh(base.find_xpath("清空"), 1, "货号")
    print("验证预设会员价范围条件是否生效")
    print("先测试大于会员价")
    base.wait_element_click(base.find_xpath_with_spaces("大于会员价格"))
    base.wait_table_refresh(base.find_xpath("组合查询"), 1, "货号")
    for i in range(1, 10):
        vip_price = base.wait_element(base.get_cell_xpath(i, "会员价")).text
        preset_price = base.wait_element(base.get_cell_xpath(i, "预设价格")).text
        assert float(preset_price) > float(vip_price)
    print("再测试小于会员价")
    base.wait_element_click(base.find_xpath_with_spaces("小于会员价格"))
    base.wait_table_refresh(base.find_xpath("组合查询"), 1, "货号")
    for i in range(1, 10):
        vip_price = base.wait_element(base.get_cell_xpath(i, "会员价")).text
        preset_price = base.wait_element(base.get_cell_xpath(i, "预设价格")).text
        assert float(preset_price) < float(vip_price)
    print("再测试等于会员价")
    base.wait_element_click(base.find_xpath_with_spaces("等于会员价格"))
    base.wait_table_refresh(base.find_xpath("组合查询"), 1, "货号")
    for i in range(1, 10):
        vip_price = base.wait_element(base.get_cell_xpath(i, "会员价")).text
        preset_price = base.wait_element(base.get_cell_xpath(i, "预设价格")).text
        assert float(preset_price) == float(vip_price)
    print("清空搜索条件")
    base.wait_table_refresh(base.find_xpath("清空"), 1, "货号")
    print("测试价格差异")
    base.wait_element(base.find_xpath_by_placeholder("价格差异大于等于")).send_keys("10")
    base.wait_element(base.find_xpath_by_placeholder("价格差异小于")).send_keys("50")
    base.wait_table_refresh(base.find_xpath("组合查询"), 1, "货号")
    vip_price = base.wait_element(base.get_cell_xpath(i, "会员价")).text
    preset_price = base.wait_element(base.get_cell_xpath(i, "预设价格")).text
    assert 10.0 <= abs(float(preset_price) - float(vip_price)) <= 50.0
    print("清空搜索条件")
    base.wait_table_refresh(base.find_xpath("清空"), 1, "货号")
    print("测试价格差异百分比")
    base.wait_element(base.find_xpath_by_placeholder("价格差异百分比大于等于")).send_keys("10")
    base.wait_element(base.find_xpath_by_placeholder("价格差异百分比小于")).send_keys("50")
    base.wait_table_refresh(base.find_xpath("组合查询"), 1, "货号")
    for i in range(1, 10):
        vip_price = base.wait_element(base.get_cell_xpath(i, "会员价")).text
        preset_price = base.wait_element(base.get_cell_xpath(i, "预设价格")).text
        if float(vip_price) >= float(preset_price):
            higher_price = float(vip_price)
        else:
            higher_price = float(preset_price)
        assert 10.0 <= abs(float(preset_price) - float(vip_price)) / higher_price * 100 <= 50.0


def test_function_button():
    setting_info = {
        "记录会员上次交易价：手工单或者门店单保存时，记录会员的商品交易价格": "true",
        "记录会员上次交易价 同款同价：手工单或者门店单保存时，记录会员的商品交易价格 同款同价": "false",
        "只有手工修改售价才会记录预设价格": "true",
    }
    interface.save_order_setting(setting_info)
    print("非同款同价模式+修改才记录会员价设置完成，修改设置之后等5秒，让设置生效")
    time.sleep(5)
    print("先准备测试数据：")
    vip_name = "会员"+base.get_now_string()
    interface.new_vip(vip_name)
    print(f"新建会员{vip_name}")
    product_code = base.get_now_string()
    interface.new_product(product_code)
    print(f"新建货号{product_code}")
    sku_code = interface.get_sku_code(product_code)[0]
    interface.modify_sku_price(sku_code, "100")
    print(f"通过{sku_code}将{product_code}整款标准售价设置为100")
    interface.modify_vip_level(vip_name, "8折")
    print(f"修改会员{vip_name}的会员等级为：8折")
    interface.modify_preset_price(vip_name, product_code, 0, 200)
    print(f"修改会员{vip_name}的商品{product_code}预设价格为200")
    base.close_page("预设会员价明细")
    base.open_page("会员", "预设会员价明细", "预设会员价明细框架")
    base.wait_element_click(base.find_xpath_by_placeholder("商品货号")).send_keys(product_code)
    base.wait_table_refresh(base.find_xpath("组合查询"), 1, "货号")
    base.select_all()
    base.wait_element_click(base.find_xpath_with_spaces("批量修改预设价格"))
    base.wait_element_click("//input[@id='price']").clear()
    base.wait_element_click("//input[@id='price']").send_keys("300")
    element = base.wait_element(base.get_cell_xpath(1, "预设价格"))
    text = element.text
    base.wait_element_click(base.find_xpath("修改"))
    base.wait_element_refresh(element, text)
    print(f"修改商品的价格为300")
    print(f"验证所有商品的价格是300")
    result = base.get_column_text("预设价格")
    for i in result:
        assert i == "300"
    print(f"确定所有商品的价格是300")
    sku_code_list = interface.get_sku_code(product_code)
    for i in sku_code_list[0: 3]:
        base.wait_element_click(base.get_cell_xpath(i, "会员名"))
        base.click_space()
    base.wait_element_click(base.find_xpath_with_spaces("批量删除预设价格"))
    time.sleep(1)
    base.wait_element_click(base.find_xpath("是否确认删除", "确认"))
    base.wait_table_refresh(base.find_xpath("组合查询"), 1, "商家编码")
    result = base.get_column_text("商家编码")
    assert result == sku_code_list[3:]
    print(result)
    print(sku_code_list[3:])
    print("修改设置再来")
    print("修改设置再来")
    setting_info = {
        "记录会员上次交易价：手工单或者门店单保存时，记录会员的商品交易价格": "true",
        "记录会员上次交易价 同款同价：手工单或者门店单保存时，记录会员的商品交易价格 同款同价": "true",
        "只有手工修改售价才会记录预设价格": "true",
    }
    interface.save_order_setting(setting_info)
    print("非同款同价模式+修改才记录会员价设置完成，修改设置之后等5秒，让设置生效")
    time.sleep(5)
    print("先准备测试数据：")
    vip_name = "会员" + base.get_now_string()
    interface.new_vip(vip_name)
    print(f"新建会员{vip_name}")
    product_code = base.get_now_string()
    interface.new_product(product_code)
    print(f"新建货号{product_code}")
    sku_code = interface.get_sku_code(product_code)[0]
    interface.modify_sku_price(sku_code, "100")
    print(f"通过{sku_code}将{product_code}整款标准售价设置为100")
    interface.modify_vip_level(vip_name, "8折")
    print(f"修改会员{vip_name}的会员等级为：8折")
    interface.modify_preset_price(vip_name, product_code, 0, 200)
    print(f"修改会员{vip_name}的商品{product_code}预设价格为200")
    base.close_page("预设会员价明细")
    base.open_page("会员", "预设会员价明细", "预设会员价明细框架")
    base.wait_element_click(base.find_xpath_by_placeholder("商品货号")).send_keys(product_code)
    base.wait_table_refresh(base.find_xpath("组合查询"), 1, "货号")
    base.select_all()
    base.wait_element_click(base.find_xpath_with_spaces("批量修改预设价格"))
    base.wait_element_click("//input[@id='price']").clear()
    base.wait_element_click("//input[@id='price']").send_keys("300")
    element = base.wait_element(base.get_cell_xpath(1, "预设价格"))
    text = element.text
    base.wait_element_click(base.find_xpath("修改"))
    base.wait_element_refresh(element, text)
    print(f"修改商品的价格为300")
    print(f"验证所有商品的价格是300")
    result = base.get_column_text("预设价格")
    for i in result:
        assert i == "300"
    print(f"确定所有商品的价格是300")
    base.select_all()
    base.wait_element_click(base.find_xpath_with_spaces("批量删除预设价格"))
    time.sleep(1)
    base.wait_element_click(base.find_xpath("是否确认删除", "确认"))
    base.wait_table_refresh(base.find_xpath("组合查询"), 1, "货号")
    base.wait_element(base.find_xpath("本页共0条数据"))


def test_001():
    modi1 = "111"
    modi12 = "222"
    modify_price = modi1
    a = modify_price
    b = copy.copy(modify_price)
    print()
    print(f"a={a}")
    print(f"b={b}")
    modify_price += modi12
    print("修改值之后：")
    print(f"a={a}")
    print(f"b={b}")


if __name__ == '__main__':
    pytest.main()
