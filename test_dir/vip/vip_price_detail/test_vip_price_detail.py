import sys
import time
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


def test_vip_price_detail():
    """
    先设置为不同款同价+只有手工修改售价才会记录预设价格
    新建一个会员
    查询会员，此时应该是没有数据，通过<div class="fl">本页共0条数据</div>判断没有记录
    新建一个商品，再次查询会员，还是没有记录
    门店收银页面开单，商品此时没有设置预设会员价，售价显示为0，关闭商品窗口
    设置商品标准售价，第二价格，第三价格，第四价格，此时再打开页面，显示为标准售价
    再修改会员等级，设置会员等级为8折，此时价格应该是标准售价*0.8
    直接开单，此时价格没有任何修改，不需要记录，再次查询，仍然是没有记录
    再次开单，修改其中一个规格价格，再次查询记录，有一条记录，核对商家编码和预设价格等信息
    再次开单，修改多个规格价格，再次查询，此时应该有多条记录，核对商家编码和预设价格等信息
    再次新建一个商品，并直接设置标准售价，第二价格，第三价格，第四价格，再次开单包含两种商品，修改两种商品全部价格，再次查询此时应该
    有两种商品的所有价格记录
    修改所有商品价格，然后核对，再删除所有商品价格
    修改设置为 同款同价+只有手工修改售价才会记录预设价格
    新建一个会员
    新建一个商品修改标准售价，第二价格，第三价格，第四价格
    门店开单，不修改价格，没有任何记录
    再次门店开单，修改一款价格，则只有一款记录
    再次门店开单，这次试用两款，修改两款价格，这时有两款的记录

    """
    # 先确定下设置
    setting_info = {
        "记录会员上次交易价：手工单或者门店单保存时，记录会员的商品交易价格": "true",
        "记录会员上次交易价 同款同价：手工单或者门店单保存时，记录会员的商品交易价格 同款同价": "false",
        "只有手工修改售价才会记录预设价格": "true",
    }
    interface.save_order_setting(setting_info)
    time.sleep(5)
    base.close_page("预设会员价明细")
    base.open_page("会员", "预设会员价明细", "预设会员价明细框架")
    # 新建会员
    vip_name = base.get_now_string()
    print("会员名称：")
    print(vip_name)
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
    print("商品货号：")
    print(product_code)
    # 解析出第一个skuCode
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
    # 设置商品的标准售价，第二价格，第三价格，第四价格
    interface.modify_sku_price(sku_code, "100", "200", "300", "400")
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
    # 设置会员等级为8折，再次查看售价是否是80
    vip_level = "8折"
    interface.modify_vip(vip_name, vip_level)
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
    # 门店开单，不修改商品价格，还是没有记录
    # sku_info_list 商品信息列表
    sku_info_list = []
    sku_info = {}
    product_info = interface.get_sku_info('', product_code)
    print("product_info:")
    print(product_info)
    i = 1
    for sku in product_info["data"]["Items"]:
        sku_info["SkuCode"] = sku["SkuCode"]
        print('sku_info["SkuCode"]:')
        print(sku_info["SkuCode"])
        i += 1
        sku_info["Qty"] = i
        sku_info["Price"] = int(sku["StandardPrice"])*int(interface.get_vip_level_info(vip_level)["data"]["Items"][0]["Discount"])/10
        print("sku_info:")
        print(sku_info)
        sku_info_list.append(dict(sku_info))
        print("sku_info_list:")
        print(sku_info_list)
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
    # 修改商品信息
    print("sku_info_list:")
    print(sku_info_list)
    print("sku_info_list[0]:")
    print(sku_info_list[0])
    modify_sku_code = sku_info_list[0]["SkuCode"]
    modify_price = sku_info_list[0]["Price"] + 10
    sku_info_list[0]["Price"] = sku_info_list[0]["Price"] + 10
    print("sku_info_list:")
    print(sku_info_list)
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
    result = base.get_column_text("预设价格")
    assert len(result) == 1
    for r in result:
        assert float(r) == float(modify_price)
    result = base.get_column_text("商家编码")
    assert len(result) == 1
    for r in result:
        assert r == modify_sku_code
    # 修改两个规格的价格，预设会员价明细页面会有两条明细
    # 还是先修改商品价格
    modify_info = {}
    j = 10
    for i in range(0, 2):
        modify_sku_code = sku_info_list[i]["SkuCode"]
        j += 10
        sku_info_list[i]["Price"] = float(sku_info_list[i]["Price"] + j)
        print("sku_info_list:")
        print(sku_info_list)
        modify_info[modify_sku_code] = float(sku_info_list[i]["Price"] + j)
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
    # 全部更改则需要显示全部该商品的全部记录
    modify_info = {}
    for i in sku_info_list:
        modify_sku_code = i["SkuCode"]
        j += 10
        i["Price"] = float(i["Price"] + j)
        print("sku_info_list:")
        print(sku_info_list)
        modify_info[modify_sku_code] = float(i["Price"] + j)
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
    # 修改设置，再来一遍
    """
    _________________________修改设置，再来一遍____________________________________________
    __________________________修改设置，再来一遍___________________________________________
    ____________________________修改设置，再来一遍_________________________________________
    """

    setting_info = {
        "记录会员上次交易价：手工单或者门店单保存时，记录会员的商品交易价格": "true",
        "记录会员上次交易价 同款同价：手工单或者门店单保存时，记录会员的商品交易价格 同款同价": "true",
        "只有手工修改售价才会记录预设价格": "true",
    }
    interface.save_order_setting(setting_info)
    time.sleep(5)
    base.close_page("预设会员价明细")
    base.open_page("会员", "预设会员价明细", "预设会员价明细框架")
    # 新建会员
    vip_name = base.get_now_string()
    print("会员名称：")
    print(vip_name)
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
    print("商品货号：")
    print(product_code)
    # 解析出第一个skuCode
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
    # 设置商品的标准售价，第二价格，第三价格，第四价格
    interface.modify_sku_price(sku_code, "100", "200", "300", "400")
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
    # 设置会员等级为8折，再次查看售价是否是80
    vip_level = "8折"
    interface.modify_vip(vip_name, vip_level)
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
    # 门店开单，不修改商品价格，还是没有记录
    # sku_info_list 商品信息列表
    sku_info_list = []
    sku_info = {}
    product_info = interface.get_sku_info('', product_code)
    print("product_info:")
    print(product_info)
    i = 1
    for sku in product_info["data"]["Items"]:
        sku_info["SkuCode"] = sku["SkuCode"]
        print('sku_info["SkuCode"]:')
        print(sku_info["SkuCode"])
        i += 1
        sku_info["Qty"] = i
        sku_info["Price"] = int(sku["StandardPrice"]) * int(
            interface.get_vip_level_info(vip_level)["data"]["Items"][0]["Discount"]) / 10
        print("sku_info:")
        print(sku_info)
        sku_info_list.append(dict(sku_info))
        print("sku_info_list:")
        print(sku_info_list)
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
    # 修改商品信息
    print("sku_info_list:")
    print(sku_info_list)
    print("sku_info_list[0]:")
    print(sku_info_list[0])
    sku_info_list[0]["Price"] = float(sku_info_list[0]["Price"] + 10)
    print("sku_info_list:")
    print(sku_info_list)
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
    result = base.get_column_text("预设价格")
    assert len(result) == 1
    for r in result:
        assert float(r) == float(modify_price)
    result = base.get_column_text("货号")
    assert len(result) == 1
    for r in result:
        assert r == product_code
    # 修改两个规格的价格，预设会员价明细页面会有两条明细
    # 还是先修改商品价格
    modify_info = {}
    j = 10
    for i in range(0, 2):
        modify_sku_code = sku_info_list[i]["SkuCode"]
        j += 10
        sku_info_list[i]["Price"] = float(sku_info_list[i]["Price"] + j)
        print("sku_info_list:")
        print(sku_info_list)
        modify_info[modify_sku_code] = float(sku_info_list[i]["Price"] + j)
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
    base.wait_element(base.find_xpath("本页共1条数据"))
    result = base.get_column_text("货号")
    assert len(result) == 1
    assert result[0] == product_code
    vip_price = base.wait_element(base.get_cell_xpath(r, "预设价格")).text
    assert vip_price in modify_info.values()
    # 全部更改则需要显示全部该商品的全部记录
    modify_info = {}
    for i in sku_info_list:
        modify_sku_code = i["SkuCode"]
        j += 10
        i["Price"] = float(i["Price"] + j)
        print("sku_info_list:")
        print(sku_info_list)
        modify_info[modify_sku_code] = float(i["Price"] + j)
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
    base.wait_element(base.find_xpath("本页共1条数据"))
    result = base.get_column_text("货号")
    assert len(result) == 1
    assert result[0] == product_code
    vip_price = base.wait_element(base.get_cell_xpath(r, "预设价格")).text
    assert vip_price in modify_info.values()
    # 重构打印数据的可读性


def test_001():
    setting_info = {
        "记录会员上次交易价：手工单或者门店单保存时，记录会员的商品交易价格": "false",
        "记录会员上次交易价 同款同价：手工单或者门店单保存时，记录会员的商品交易价格 同款同价": "false",
        "只有手工修改售价才会记录预设价格": "true",
    }
    interface.save_order_setting(setting_info)


if __name__ == '__main__':
    pytest.main()
