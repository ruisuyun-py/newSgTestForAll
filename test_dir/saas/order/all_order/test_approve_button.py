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
    print(f"先修改设置开启自动合单设置")
    setting_info = {"开启": "true"}
    setting_interface.save_auto_merge_setting(setting_info)
    time.sleep(5)
    print(f"修改设置之后等待5秒")
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
    base.fuzzy_search("订单编码", order_code)
    base.wait_element_click(base.get_cell_xpath(order_code, "订单编码"))
    base.select_all()
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
    base.fuzzy_search("订单编码", order_code)
    base.select_all()
    order.turn_to_normal("黑名单")
    base.wait_text_locate(base.get_cell_xpath(order_code, "订单状态"), "待审核")
    # TODO:(RUI)全部订单页面审核已终结的订单报错：当前数据可能被其他人操作了，请刷新后重试！，需要优化下报错，比如 订单:/TD200918013有异常：标记异常 常用异常2
    # order.turn_to_exception("终结")
    # base.wait_text_locate(base.get_cell_xpath(order_code, "订单状态"), "已终结")
    # order.turn_to_normal("已终结")
    # base.wait_text_locate(base.get_cell_xpath(order_code, "订单状态"), "待审核")
    base.fuzzy_search("订单编码", order_code)
    base.select_all()
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
    print(f"审核待合并订单，则需要报错待合并订单异常")
    base.fuzzy_search("订单编码", merge_order_code)
    base.select_all()
    base.wait_element_click(base.find_xpath("审核"))
    try:
        base.wait_element(base.find_xpath("信息", f"待合并订单:/{order_code}有异常：标记异常 异常测试"))
    except AssertionError as e:
        print(e)
        assert 1 == 2, f"全部订单页面审核标记异常订单不能正常弹窗报错"
    time.sleep(1)
    base.wait_element_click(base.find_xpath("信息", "确定"))
    base.fuzzy_search("订单编码", order_code)
    base.select_all()
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
    print(f"审核待合并订单，则需要报错待合并订单异常")
    base.fuzzy_search("订单编码", merge_order_code)
    base.select_all()
    base.wait_element_click(base.find_xpath("审核"))
    try:
        base.wait_element(base.find_xpath("信息", f"待合并订单:/{order_code}有异常：标记异常 常用异常2"))
    except AssertionError as e:
        print(e)
        assert 1 == 2, f"全部订单页面审核标记异常订单不能正常弹窗报错"
    time.sleep(1)
    base.wait_element_click(base.find_xpath("信息", "确定"))
    base.fuzzy_search("订单编码", order_code)
    base.select_all()
    order.turn_to_normal("标记异常")
    base.wait_text_locate(base.get_cell_xpath(order_code, "订单状态"), "待审核")
    print(f"先设置不允许负库存，然后审核报错，再设置允许负库存，审核订单")
    setting_info = {"允许负库存": "false"}
    setting_interface.save_base_setting(setting_info)
    time.sleep(5)
    print(f"设置不允许负库存之后，等待5秒设置生效")
    base.fuzzy_search("订单编码", order_code)
    base.select_all()
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
    setting_info = {"开启": "false"}
    setting_interface.save_auto_merge_setting(setting_info)
    time.sleep(5)
    print(f"修改设置之后等待5秒")


def test_auto_merge_setting():
    print(f"先修改设置，开启自动合单")
    setting_info = {"开启": "true"}
    setting_interface.save_auto_merge_setting(setting_info)
    time.sleep(5)
    print(f"修改设置之后等待5秒")
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
    base.fuzzy_search("订单编码", vip_name)
    base.wait_element_click(base.get_cell_xpath(1, "订单编码"))
    base.click_space()
    element = base.wait_element(base.get_cell_xpath(1, "订单状态"))
    text = element.text
    base.wait_element_click(base.find_xpath("审核"))
    base.wait_element_refresh(element, text)
    with base.operate_page("订单", "打印发货", "打印发货框架") as e:
        base.fuzzy_search("发货单号", vip_name)
        base.scroll_to(6)
        merge_order_code_result = base.wait_element(base.get_cell_xpath(order_code, "订单编号")).text
        assert order_code in merge_order_code_result
        assert merge_order_code in merge_order_code_result
    print(f"关闭设置之后不能合并")
    setting_info = {"开启": "false"}
    setting_interface.save_auto_merge_setting(setting_info)
    time.sleep(5)
    print(f"修改设置之后等待5秒")
    base.open_page("订单", "全部订单", "全部订单框架")
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
    base.fuzzy_search("订单编码", vip_name)
    base.wait_element_click(base.get_cell_xpath(1, "订单编码"))
    base.click_space()
    element = base.wait_element(base.get_cell_xpath(1, "订单状态"))
    text = element.text
    base.wait_element_click(base.find_xpath("审核"))
    base.wait_element_refresh(element, text)
    base.fuzzy_search("订单编码", vip_name)
    order_status = base.get_column_text("订单状态")
    assert len(order_status) == 2
    assert "待审核" in order_status
    assert "发货中" in order_status
    print(f"""----------------------------------店铺相同-----------------------------------------------""")
    print(f"新建两个店铺不同的订单，开启设置之后不能合并")
    setting_info = {"开启": "true", "店铺相同": "false"}
    setting_interface.save_auto_merge_setting(setting_info)
    time.sleep(5)
    print(f"修改设置之后等待5秒")
    vip_name = "会员" + base.get_now_string()
    vip_interface.new_vip(vip_name)
    print(f"{vip_name}")
    product_code = base.get_now_string()
    product_interface.new_product(product_code)
    sku_code = product_interface.get_sku_code(product_code)[0]
    product_interface.modify_sku_price(sku_code, "100")
    sku_info = [{'商家编码': sku_code, '数量': '2'}, ]
    order_code = order_interface.new_order(vip_name, sku_info)["Code"]
    merge_order_code = order_interface.new_order(vip_name, sku_info, "主仓库", "买家自提", "巨淘气")["Code"]
    base.fuzzy_search("订单编码", vip_name)
    base.wait_element_click(base.get_cell_xpath(1, "订单编码"))
    base.click_space()
    element = base.wait_element(base.get_cell_xpath(1, "订单状态"))
    text = element.text
    base.wait_element_click(base.find_xpath("审核"))
    base.wait_element_refresh(element, text)
    with base.operate_page("订单", "打印发货", "打印发货框架") as e:
        base.fuzzy_search("发货单号", vip_name)
        base.scroll_to(6)
        merge_order_code_result = base.wait_element(base.get_cell_xpath(order_code, "订单编号")).text
        assert order_code in merge_order_code_result
        assert merge_order_code in merge_order_code_result
    print(f"勾选店铺相同之后不能合并")
    setting_info = {"开启": "true", "店铺相同": "true"}
    setting_interface.save_auto_merge_setting(setting_info)
    time.sleep(5)
    print(f"修改设置之后等待5秒")
    base.open_page("订单", "全部订单", "全部订单框架")
    vip_name = "会员" + base.get_now_string()
    vip_interface.new_vip(vip_name)
    print(f"{vip_name}")
    product_code = base.get_now_string()
    product_interface.new_product(product_code)
    sku_code = product_interface.get_sku_code(product_code)[0]
    product_interface.modify_sku_price(sku_code, "100")
    sku_info = [{'商家编码': sku_code, '数量': '2'}, ]
    order_code = order_interface.new_order(vip_name, sku_info)["Code"]
    merge_order_code = order_interface.new_order(vip_name, sku_info, "主仓库", "买家自提", "巨淘气")["Code"]
    base.fuzzy_search("订单编码", vip_name)
    base.wait_element_click(base.get_cell_xpath(1, "订单编码"))
    base.click_space()
    element = base.wait_element(base.get_cell_xpath(1, "订单状态"))
    text = element.text
    base.wait_element_click(base.find_xpath("审核"))
    base.wait_element_refresh(element, text)
    base.fuzzy_search("订单编码", vip_name)
    order_status = base.get_column_text("订单状态")
    assert len(order_status) == 2
    assert "待审核" in order_status
    assert "发货中" in order_status
    print(f"----------------------------------------会员相同-------------------------------------------------------")
    print(f"新建两个会员不同的订单，不开启设置能合并")
    setting_info = {"开启": "true", "会员相同": "false"}
    setting_interface.save_auto_merge_setting(setting_info)
    time.sleep(5)
    print(f"修改设置之后等待5秒")
    rand_str = base.get_now_string()
    other_info = {"收货人": rand_str, "手机": rand_str, "地址": rand_str}
    vip_name = "会员" + base.get_now_string()
    vip_interface.new_vip(vip_name, other_info)
    print(f"{vip_name}")
    product_code = base.get_now_string()
    product_interface.new_product(product_code)
    sku_code = product_interface.get_sku_code(product_code)[0]
    product_interface.modify_sku_price(sku_code, "100")
    sku_info = [{'商家编码': sku_code, '数量': '2'}, ]
    order_code = order_interface.new_order(vip_name, sku_info)["Code"]
    vip_name = "会员" + base.get_now_string()
    vip_interface.new_vip(vip_name, other_info)
    print(f"{vip_name}")
    merge_order_code = order_interface.new_order(vip_name, sku_info)["Code"]
    base.fuzzy_search("订单编码", vip_name)
    base.wait_element_click(base.get_cell_xpath(1, "订单编码"))
    base.click_space()
    element = base.wait_element(base.get_cell_xpath(1, "订单状态"))
    text = element.text
    base.wait_element_click(base.find_xpath("审核"))
    base.wait_element_refresh(element, text)
    with base.operate_page("订单", "打印发货", "打印发货框架") as e:
        base.wait_element(base.find_xpath("组合查询"))
        time.sleep(1)
        base.fuzzy_search("发货单号", order_code)
        base.scroll_to(6)
        merge_order_code_result = base.wait_element(base.get_cell_xpath(order_code, "订单编号")).text
        assert order_code in merge_order_code_result
        assert merge_order_code in merge_order_code_result
    print(f"勾选会员相同之后不能合并")
    setting_info = {"开启": "true", "会员相同": "true"}
    setting_interface.save_auto_merge_setting(setting_info)
    time.sleep(5)
    print(f"修改设置之后等待5秒")
    base.open_page("订单", "全部订单", "全部订单框架")
    rand_str = base.get_now_string()
    other_info = {"收货人": rand_str, "手机": rand_str, "地址": rand_str}
    vip_name = "会员" + base.get_now_string()
    vip_interface.new_vip(vip_name, other_info)
    print(f"{vip_name}")
    order_code = order_interface.new_order(vip_name, sku_info)["Code"]
    vip_name = "会员" + base.get_now_string()
    vip_interface.new_vip(vip_name, other_info)
    print(f"{vip_name}")
    merge_order_code = order_interface.new_order(vip_name, sku_info)["Code"]
    base.fuzzy_search("订单编码", vip_name)
    base.wait_element_click(base.get_cell_xpath(1, "订单编码"))
    base.click_space()
    element = base.wait_element(base.get_cell_xpath(1, "订单状态"))
    text = element.text
    base.wait_element_click(base.find_xpath("审核"))
    base.wait_element_refresh(element, text)
    base.fuzzy_search("订单编码", rand_str)
    order_status = base.get_column_text("订单状态")
    assert len(order_status) == 2
    assert "待审核" in order_status
    assert "发货中" in order_status
    print(f"""----------------------------------快递相同-----------------------------------------------""")
    print(f"新建两个快递不同的订单，开启设置之后不能合并")
    setting_info = {"开启": "true", "快递相同": "false"}
    setting_interface.save_auto_merge_setting(setting_info)
    time.sleep(5)
    print(f"修改设置之后等待5秒")
    vip_name = "会员" + base.get_now_string()
    vip_interface.new_vip(vip_name)
    print(f"{vip_name}")
    product_code = base.get_now_string()
    product_interface.new_product(product_code)
    sku_code = product_interface.get_sku_code(product_code)[0]
    product_interface.modify_sku_price(sku_code, "100")
    sku_info = [{'商家编码': sku_code, '数量': '2'}, ]
    order_code = order_interface.new_order(vip_name, sku_info)["Code"]
    merge_order_code = order_interface.new_order(vip_name, sku_info, "主仓库", "邮政小包电子面单")["Code"]
    base.fuzzy_search("订单编码", vip_name)
    base.wait_element_click(base.get_cell_xpath(1, "订单编码"))
    base.click_space()
    element = base.wait_element(base.get_cell_xpath(1, "订单状态"))
    text = element.text
    base.wait_element_click(base.find_xpath("审核"))
    base.wait_element_refresh(element, text)
    with base.operate_page("订单", "打印发货", "打印发货框架") as e:
        base.fuzzy_search("发货单号", vip_name)
        base.scroll_to(5)
        merge_order_code_result = base.wait_element(base.get_cell_xpath(order_code, "订单编号")).text
        assert order_code in merge_order_code_result
        assert merge_order_code in merge_order_code_result
    print(f"勾选店铺相同之后不能合并")
    setting_info = {"开启": "true", "快递相同": "true"}
    setting_interface.save_auto_merge_setting(setting_info)
    time.sleep(5)
    print(f"修改设置之后等待5秒")
    base.open_page("订单", "全部订单", "全部订单框架")
    vip_name = "会员" + base.get_now_string()
    vip_interface.new_vip(vip_name)
    print(f"{vip_name}")
    product_code = base.get_now_string()
    product_interface.new_product(product_code)
    sku_code = product_interface.get_sku_code(product_code)[0]
    product_interface.modify_sku_price(sku_code, "100")
    sku_info = [{'商家编码': sku_code, '数量': '2'}, ]
    order_code = order_interface.new_order(vip_name, sku_info)["Code"]
    merge_order_code = order_interface.new_order(vip_name, sku_info, "主仓库", "邮政小包电子面单")["Code"]
    base.fuzzy_search("订单编码", vip_name)
    base.wait_element_click(base.get_cell_xpath(1, "订单编码"))
    base.click_space()
    element = base.wait_element(base.get_cell_xpath(1, "订单状态"))
    text = element.text
    base.wait_element_click(base.find_xpath("审核"))
    base.wait_element_refresh(element, text)
    base.fuzzy_search("订单编码", vip_name)
    order_status = base.get_column_text("订单状态")
    assert len(order_status) == 2
    assert "待审核" in order_status
    assert "发货中" in order_status
    print(f"""----------------------------------仓库相同-----------------------------------------------""")
    print(f"新建两个店铺不同的订单，开启设置之后不能合并")
    setting_info = {"开启": "true", "仓库相同": "false"}
    setting_interface.save_auto_merge_setting(setting_info)
    time.sleep(5)
    print(f"修改设置之后等待5秒")
    vip_name = "会员" + base.get_now_string()
    vip_interface.new_vip(vip_name)
    print(f"{vip_name}")
    product_code = base.get_now_string()
    product_interface.new_product(product_code)
    sku_code = product_interface.get_sku_code(product_code)[0]
    product_interface.modify_sku_price(sku_code, "100")
    sku_info = [{'商家编码': sku_code, '数量': '2'}, ]
    order_code = order_interface.new_order(vip_name, sku_info)["Code"]
    merge_order_code = order_interface.new_order(vip_name, sku_info, "测试仓")["Code"]
    base.fuzzy_search("订单编码", vip_name)
    base.wait_element_click(base.get_cell_xpath(1, "订单编码"))
    base.click_space()
    element = base.wait_element(base.get_cell_xpath(1, "订单状态"))
    text = element.text
    base.wait_element_click(base.find_xpath("审核"))
    base.wait_element_refresh(element, text)
    with base.operate_page("订单", "打印发货", "打印发货框架") as e:
        base.fuzzy_search("发货单号", vip_name)
        base.scroll_to(6)
        merge_order_code_result = base.wait_element(base.get_cell_xpath(order_code, "订单编号")).text
        assert order_code in merge_order_code_result
        assert merge_order_code in merge_order_code_result
    print(f"勾选店铺相同之后不能合并")
    setting_info = {"开启": "true", "仓库相同": "true"}
    setting_interface.save_auto_merge_setting(setting_info)
    time.sleep(5)
    print(f"修改设置之后等待5秒")
    base.open_page("订单", "全部订单", "全部订单框架")
    vip_name = "会员" + base.get_now_string()
    vip_interface.new_vip(vip_name)
    print(f"{vip_name}")
    product_code = base.get_now_string()
    product_interface.new_product(product_code)
    sku_code = product_interface.get_sku_code(product_code)[0]
    product_interface.modify_sku_price(sku_code, "100")
    sku_info = [{'商家编码': sku_code, '数量': '2'}, ]
    order_code = order_interface.new_order(vip_name, sku_info)["Code"]
    merge_order_code = order_interface.new_order(vip_name, sku_info, "测试仓")["Code"]
    base.fuzzy_search("订单编码", vip_name)
    base.wait_element_click(base.get_cell_xpath(1, "订单编码"))
    base.click_space()
    element = base.wait_element(base.get_cell_xpath(1, "订单状态"))
    text = element.text
    base.wait_element_click(base.find_xpath("审核"))
    base.wait_element_refresh(element, text)
    base.fuzzy_search("订单编码", vip_name)
    order_status = base.get_column_text("订单状态")
    assert len(order_status) == 2
    assert "待审核" in order_status
    assert "发货中" in order_status
    print(f"""----------------------------------有退款的搞不了-----------------------------------------------""")
    print(f"""----------------------------------不合并已配货订单-----------------------------------------------""")
    print(f"新建两个店铺不同的订单，开启设置之后不能合并")
    setting_info = {"开启": "true", "不合并已配货订单": "false"}
    setting_interface.save_auto_merge_setting(setting_info)
    time.sleep(5)
    print(f"修改设置之后等待5秒")
    vip_name = "会员" + base.get_now_string()
    vip_interface.new_vip(vip_name)
    print(f"{vip_name}")
    product_code = base.get_now_string()
    product_interface.new_product(product_code)
    sku_code = product_interface.get_sku_code(product_code)[0]
    product_interface.modify_sku_price(sku_code, "100")
    sku_info = [{'商家编码': sku_code, '数量': '2'}, ]
    order_code = order_interface.new_order(vip_name, sku_info)["Code"]
    base.fuzzy_search("订单编码", vip_name)
    base.wait_element_click(base.get_cell_xpath(1, "订单编码"))
    base.click_space()
    element = base.wait_element(base.get_cell_xpath(1, "订单状态"))
    text = element.text
    base.wait_element_click(base.find_xpath("审核"))
    base.wait_element_refresh(element, text)
    merge_order_code = order_interface.new_order(vip_name, sku_info)["Code"]
    base.fuzzy_search("订单编码", vip_name)
    base.wait_element_click(base.get_cell_xpath(1, "订单编码"))
    base.click_space()
    base.wait_element_click(base.find_xpath("审核"))
    base.wait_element(base.find_xpath("信息", "审核失败：存在已配货的待合并订单！"))
    time.sleep(1)
    base.wait_element_click(base.find_xpath("信息", "确定"))
    print(f"勾选之后不再提示")
    setting_info = {"开启": "true", "不合并已配货订单": "true"}
    setting_interface.save_auto_merge_setting(setting_info)
    time.sleep(5)
    print(f"修改设置之后等待5秒")
    base.open_page("订单", "全部订单", "全部订单框架")
    vip_name = "会员" + base.get_now_string()
    vip_interface.new_vip(vip_name)
    print(f"{vip_name}")
    product_code = base.get_now_string()
    product_interface.new_product(product_code)
    sku_code = product_interface.get_sku_code(product_code)[0]
    product_interface.modify_sku_price(sku_code, "100")
    sku_info = [{'商家编码': sku_code, '数量': '2'}, ]
    order_code = order_interface.new_order(vip_name, sku_info, "测试仓", "买家自提", "巨淘气", {"卖家备注": "111"})["Code"]
    base.fuzzy_search("订单编码", vip_name)
    base.wait_element_click(base.get_cell_xpath(1, "订单编码"))
    base.click_space()
    element = base.wait_element(base.get_cell_xpath(1, "订单状态"))
    text = element.text
    base.wait_element_click(base.find_xpath("审核"))
    base.wait_element_refresh(element, text)
    merge_order_code = order_interface.new_order(vip_name, sku_info, "测试仓", "买家自提", "巨淘气", {"卖家备注": "222"})["Code"]
    base.fuzzy_search("订单编码", vip_name)
    base.wait_element_click(base.get_cell_xpath(1, "订单编码"))
    base.click_space()
    element = base.wait_element(base.get_cell_xpath(1, "订单状态"))
    text = element.text
    base.wait_element_click(base.find_xpath("审核"))
    base.wait_element_refresh(element, text)
    base.fuzzy_search("订单编码", vip_name)
    order_status = base.get_column_text("订单状态")
    assert len(order_status) == 2
    for i in order_status:
        assert "发货中" == i
    print(f"""----------------------------------合并买家/卖家备注不加平台单号------------------------------------------""")
    print(f"平台单号弄不出来，就看下卖家备注能否合并")
    setting_info = {"开启": "true", "合并买家/卖家备注不加平台单号": "false"}
    setting_interface.save_auto_merge_setting(setting_info)
    time.sleep(5)
    print(f"修改设置之后等待5秒")
    vip_name = "会员" + base.get_now_string()
    vip_interface.new_vip(vip_name)
    print(f"{vip_name}")
    product_code = base.get_now_string()
    product_interface.new_product(product_code)
    sku_code = product_interface.get_sku_code(product_code)[0]
    product_interface.modify_sku_price(sku_code, "100")
    sku_info = [{'商家编码': sku_code, '数量': '2'}, ]
    order_code = order_interface.new_order(vip_name, sku_info, "测试仓", "买家自提", "巨淘气", {"卖家备注": "111"})["Code"]
    merge_order_code = order_interface.new_order(vip_name, sku_info, "测试仓", "买家自提", "巨淘气", {"卖家备注": "222"})["Code"]
    base.fuzzy_search("订单编码", vip_name)
    base.wait_element_click(base.get_cell_xpath(1, "订单编码"))
    base.click_space()
    element = base.wait_element(base.get_cell_xpath(1, "订单状态"))
    text = element.text
    base.wait_element_click(base.find_xpath("审核"))
    base.wait_element_refresh(element, text)
    with base.operate_page("订单", "打印发货", "打印发货框架") as e:
        base.fuzzy_search("发货单号", vip_name)
        merge_order_code_result = base.wait_element(base.get_cell_xpath(vip_name, "卖家备注")).text
        assert "111" in merge_order_code_result
        assert "222" in merge_order_code_result
    print(f"关闭设置")
    setting_info = {"开启": "false"}
    setting_interface.save_auto_merge_setting(setting_info)
    time.sleep(5)


def test_not_merge_approved_order():
    setting_info = {"开启": "true", "不合并已配货订单": "false"}
    setting_interface.save_auto_merge_setting(setting_info)
    time.sleep(5)
    print(f"修改设置之后等待5秒")
    vip_name = "会员" + base.get_now_string()
    vip_interface.new_vip(vip_name)
    print(f"{vip_name}")
    product_code = base.get_now_string()
    product_interface.new_product(product_code)
    sku_code = product_interface.get_sku_code(product_code)[0]
    product_interface.modify_sku_price(sku_code, "100")
    sku_info = [{'商家编码': sku_code, '数量': '2'}, ]
    order_code = order_interface.new_order(vip_name, sku_info, "主仓库", "邮政小包电子面单")["Code"]
    base.fuzzy_search("订单编码", vip_name)
    base.wait_element_click(base.get_cell_xpath(1, "订单编码"))
    base.click_space()
    element = base.wait_element(base.get_cell_xpath(1, "订单状态"))
    text = element.text
    base.wait_element_click(base.find_xpath("审核"))
    base.wait_element_refresh(element, text)
    merge_order_code = order_interface.new_order(vip_name, sku_info, "主仓库", "邮政小包电子面单")["Code"]
    base.fuzzy_search("订单编码", vip_name)
    base.wait_element_click(base.get_cell_xpath(1, "订单编码"))
    base.click_space()
    base.wait_element_click(base.find_xpath("审核"))
    base.wait_element(base.find_xpath("信息", "审核失败：存在已配货的待合并订单！"))
    time.sleep(1)
    base.wait_element_click(base.find_xpath("信息", "已配货的发货单"))
    base.wait_element_click(base.get_cell_xpath(order_code, "订单编号"))
    base.click_space()
    base.wait_element(base.find_xpath("已配货的发货单", "删除"))
    print(f"删除是将已审核的订单删回来，目前调用的是删除功能不是终止发货不会标记手工终止发货异常")
    time.sleep(1)
    base.wait_element_click(base.find_xpath("已配货的发货单", "删除"))
    base.wait_element(base.find_xpath("已配货的发货单", "取消"))
    time.sleep(1)
    base.wait_element_click(base.find_xpath("已配货的发货单", "取消"))
    base.fuzzy_search("订单编码", vip_name)
    base.wait_element_click(base.get_cell_xpath(1, "订单编码"))
    result = base.get_column_text("订单状态")
    for i in result:
        assert i == '待审核'
    base.select_all()
    element = base.wait_element(base.get_cell_xpath(1, "订单状态"))
    text = element.text
    base.wait_element_click(base.find_xpath("审核"))
    base.wait_element_refresh(element, text)
    with base.operate_page("订单", "打印发货", "打印发货框架") as e:
        base.fuzzy_search("发货单号", vip_name)
        base.scroll_to(6)
        merge_order_code_result = base.wait_element(base.get_cell_xpath(order_code, "订单编号")).text
        assert order_code in merge_order_code_result
        assert merge_order_code in merge_order_code_result
    print(f"----------------------------------再试下强制审核-----------------------------------------")
    base.open_page("订单", "全部订单", "全部订单框架")
    vip_name = "会员" + base.get_now_string()
    vip_interface.new_vip(vip_name)
    print(f"{vip_name}")
    product_code = base.get_now_string()
    product_interface.new_product(product_code)
    sku_code = product_interface.get_sku_code(product_code)[0]
    product_interface.modify_sku_price(sku_code, "100")
    sku_info = [{'商家编码': sku_code, '数量': '2'}, ]
    order_code = order_interface.new_order(vip_name, sku_info, "主仓库", "邮政小包电子面单")["Code"]
    base.fuzzy_search("订单编码", vip_name)
    base.wait_element_click(base.get_cell_xpath(1, "订单编码"))
    base.click_space()
    element = base.wait_element(base.get_cell_xpath(1, "订单状态"))
    text = element.text
    base.wait_element_click(base.find_xpath("审核"))
    base.wait_element_refresh(element, text)
    merge_order_code = order_interface.new_order(vip_name, sku_info, "主仓库", "邮政小包电子面单")["Code"]
    base.fuzzy_search("订单编码", vip_name)
    base.wait_element_click(base.get_cell_xpath(1, "订单编码"))
    base.click_space()
    base.wait_element_click(base.find_xpath("审核"))
    base.wait_element(base.find_xpath("信息", "审核失败：存在已配货的待合并订单！"))
    time.sleep(1)
    base.wait_element_click(base.find_xpath("信息", "已配货的发货单"))
    base.wait_element_click(base.get_cell_xpath(order_code, "订单编号"))
    base.click_space()
    base.wait_element(base.find_xpath("已配货的发货单", "强制审核"))
    print(f"强制审核只是将待审核的订单审核过去，不合单")
    time.sleep(1)
    base.wait_element_click(base.find_xpath("已配货的发货单", "强制审核"))
    base.wait_element(base.find_xpath("已配货的发货单", "取消"))
    time.sleep(1)
    base.wait_element_click(base.find_xpath("已配货的发货单", "取消"))
    base.fuzzy_search("订单编码", vip_name)
    base.wait_element_click(base.get_cell_xpath(1, "订单编码"))
    result = base.get_column_text("订单状态")
    for i in result:
        assert i == '发货中'
    print(f"-------------------------开启不合并已配货订单之后不再有提示-------------------")
    setting_info = {"开启": "true", "不合并已配货订单": "true"}
    setting_interface.save_auto_merge_setting(setting_info)
    time.sleep(5)
    print(f"修改设置之后等待5秒")
    base.open_page("订单", "全部订单", "全部订单框架")
    vip_name = "会员" + base.get_now_string()
    vip_interface.new_vip(vip_name)
    print(f"{vip_name}")
    product_code = base.get_now_string()
    product_interface.new_product(product_code)
    sku_code = product_interface.get_sku_code(product_code)[0]
    product_interface.modify_sku_price(sku_code, "100")
    sku_info = [{'商家编码': sku_code, '数量': '2'}, ]
    order_code = order_interface.new_order(vip_name, sku_info, "测试仓", "买家自提", "巨淘气", {"卖家备注": "111"})["Code"]
    base.fuzzy_search("订单编码", vip_name)
    base.wait_element_click(base.get_cell_xpath(1, "订单编码"))
    base.click_space()
    element = base.wait_element(base.get_cell_xpath(1, "订单状态"))
    text = element.text
    base.wait_element_click(base.find_xpath("审核"))
    base.wait_element_refresh(element, text)
    merge_order_code = order_interface.new_order(vip_name, sku_info, "测试仓", "买家自提", "巨淘气", {"卖家备注": "222"})["Code"]
    base.fuzzy_search("订单编码", vip_name)
    base.wait_element_click(base.get_cell_xpath(1, "订单编码"))
    base.click_space()
    element = base.wait_element(base.get_cell_xpath(1, "订单状态"))
    text = element.text
    base.wait_element_click(base.find_xpath("审核"))
    base.wait_element_refresh(element, text)
    base.fuzzy_search("订单编码", vip_name)
    order_status = base.get_column_text("订单状态")
    assert len(order_status) == 2
    for i in order_status:
        assert "发货中" == i
    setting_info = {"开启": "true"}
    setting_interface.save_auto_merge_setting(setting_info)
    time.sleep(5)
    print(f"修改设置之后等待5秒")


if __name__ == '__main__':
    pytest.main()