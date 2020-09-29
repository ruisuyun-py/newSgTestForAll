import os
import sys
import time
import datetime
import pytest
from os.path import dirname, abspath
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
import test_dir.test_base as test
import page.login_page as login
import page.base_page as base
import page.order.all_order_page as order
import page.order.print_and_delivery_page as delivery_order
import interface.interface as interface
import interface.order.delivery_order_interface as delivery_interface
import interface.supplier.supplier_interface as supplier_interface
import interface.setting.setting_interface as setting_interface
import interface.order.order_interface as order_interface
import interface.product.product_interface as product_interface
import interface.vip.vip_interface as vip_interface
import interface.inventory.inventory_interface as inventory_interface
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
    base.wait_element(base.find_xpath("新增订单"))
    time.sleep(1)
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
    base.wait_element(base.get_cell_xpath(1, "订单编码"))
    time.sleep(2)
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


# 批量审核
def test_multi_approve_button():
    base.wait_element(base.find_xpath("订单状态", "待审核（无备注）"))
    time.sleep(1)
    base.wait_element_click(base.find_xpath("订单状态", "待审核（无备注）"))
    base.wait_table_refresh(base.find_xpath("组合查询"), 1, "订单编码")
    order_code = base.wait_element(base.get_cell_xpath(1, "订单编码")).text
    base.wait_element(base.find_xpath_by_placeholder("模糊搜索")).send_keys(order_code)
    base.wait_element_click(base.find_xpath("批量审核"))
    base.wait_element(base.find_xpath("提示", "根据当前查询条件共查询出"))
    time.sleep(1)
    base.wait_element_click(base.find_xpath("根据当前查询条件共查询出", "确定"))
    base.change_frame("全部订单框架", "任务托管列表")
    base.wait_text_locate(base.get_cell_xpath(1, "进度条"), '100%')
    base.change_frame("全部订单框架")
    base.wait_element_click(base.find_xpath_by_tag_name("任务托管列表", "a"))


# 转正常转异常
def test_turn_to_exception():
    """
    新建一个单子，先转异常然后再转正常如此反复
    """
    vip_name = "会员"+base.get_now_string()
    vip_interface.new_vip(vip_name)
    print(f"{vip_name}")
    sku_info = [{'商家编码': '测试商品1-红色 XS', '数量': '2'}, ]
    order_code = order_interface.new_order(vip_name, sku_info)["Code"]
    base.fuzzy_search("订单编码", order_code)
    base.select_all()
    order.turn_to_exception("黑名单")
    base.wait_text_locate(base.get_cell_xpath(order_code, "订单状态"), "黑名单")
    order.turn_to_normal("黑名单")
    base.wait_text_locate(base.get_cell_xpath(order_code, "订单状态"), "待审核")
    order.turn_to_exception("终结")
    base.wait_text_locate(base.get_cell_xpath(order_code, "订单状态"), "已终结")
    order.turn_to_normal("已终结")
    base.wait_text_locate(base.get_cell_xpath(order_code, "订单状态"), "待审核")
    order.turn_to_exception("标记异常", "手工标记异常测试")
    base.wait_text_locate(base.get_cell_xpath(order_code, "订单状态"), "手工标记异常测试")
    order.turn_to_normal("标记异常")
    base.wait_text_locate(base.get_cell_xpath(order_code, "订单状态"), "待审核")
    order.turn_to_exception("常用异常", "常用异常2")
    base.wait_text_locate(base.get_cell_xpath(order_code, "订单状态"), "常用异常2")
    order.turn_to_normal("标记异常")
    base.wait_text_locate(base.get_cell_xpath(order_code, "订单状态"), "待审核")


def test_manual_split_order():# TODO:(RUI) 有BUG：全部订单页面，手工拆弹功能，拆包配货页面需要切换新表格组件，图片有问题，没做处理，当前重量字段应该是剩余可拆分数*商品重量，但是目前失效
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
    base.wait_element_click(base.find_xpath("拆单"))
    base.wait_element(base.find_xpath("拆单", "手工拆单"))
    time.sleep(1)
    base.wait_element_click(base.find_xpath("拆单", "手工拆单"))
    base.change_frame("全部订单框架", "拆包配货")
    base.wait_element(base.get_old_cell_input_xpath(1, "拆分数量")).send_keys(Keys.CONTROL+'a')
    base.wait_element(base.get_old_cell_input_xpath(1, "拆分数量")).send_keys("1")
    base.wait_element(base.find_xpath("立即拆分"))
    time.sleep(1)
    base.wait_element_click(base.find_xpath("立即拆分"))
    base.wait_element(base.find_xpath("提示", "请确认需要拆分出来1个商品？"))
    time.sleep(1)
    base.wait_element_click(base.find_xpath("提示", "确定"))
    base.change_frame("全部订单框架")
    base.wait_element_refresh(element, text)
    result = base.wait_element(base.get_cell_xpath(order_code, "订单状态")).text
    assert result == "部分审核"
    base.wait_element_click(base.get_cell_xpath(order_code, "商品信息"))
    other_info = order.get_float_sku_info_text(sku_code, "其他信息")
    assert "已审1件" in other_info


def test_multi_split_to_one_piece():
    vip_name = "会员" + base.get_now_string()
    vip_interface.new_vip(vip_name)
    print(f"{vip_name}")
    product_code = base.get_now_string()
    product_interface.new_product(product_code)
    sku_code = product_interface.get_sku_code(product_code)[0]
    product_interface.modify_sku_price(sku_code, "100")
    sku_info = [{'商家编码': sku_code, '数量': '20'}, ]
    order_code = order_interface.new_order(vip_name, sku_info)["Code"]
    base.fuzzy_search("订单编码", vip_name)
    base.wait_element_click(base.get_cell_xpath(1, "订单编码"))
    base.click_space()
    element = base.wait_element(base.get_cell_xpath(1, "订单状态"))
    text = element.text
    base.wait_element_click(base.find_xpath("拆单"))
    base.wait_element(base.find_xpath("拆单", "批量拆分成单件"))
    time.sleep(1)
    base.wait_element_click(base.find_xpath("拆单", "批量拆分成单件"))
    base.wait_element(base.find_xpath("提示", "订单会被拆分成商品数量为1的发货单发货，是否继续操作？"))
    time.sleep(1)
    base.wait_element_click(base.find_xpath("提示", "确定"))
    with base.operate_page("订单", "打印发货", "打印发货框架"):
        start = datetime.datetime.now()
        while (datetime.datetime.now() - start).seconds < 30:
            base.fuzzy_search("发货单号", order_code)
            product_num_list = base.get_column_text("商品数")
            if len(product_num_list) == 20:
                for i in product_num_list:
                    assert int(i) == 1
                break


def test_multi_split_with_warehouse():
    vip_name = "会员" + base.get_now_string()
    vip_interface.new_vip(vip_name)
    print(f"{vip_name}")
    product_code = base.get_now_string()
    product_interface.new_product(product_code)
    main_sku_code = product_interface.get_sku_code(product_code)[0]
    product_interface.modify_sku_price(main_sku_code, "100")
    sku_id_list = product_interface.get_sku_id("", product_code)
    modify_info_dict = {"优先出库仓": "主仓库"}
    product_interface.multi_modify_sku_info(sku_id_list, modify_info_dict)
    sku_info = [{'商家编码': main_sku_code, '数量': '2'}]
    product_code = base.get_now_string()
    product_interface.new_product(product_code)
    test_sku_code = product_interface.get_sku_code(product_code)[0]
    product_interface.modify_sku_price(test_sku_code, "100")
    sku_id_list = product_interface.get_sku_id("", product_code)
    modify_info_dict = {"优先出库仓": "测试仓"}
    product_interface.multi_modify_sku_info(sku_id_list, modify_info_dict)
    sku_info.append({'商家编码': test_sku_code, '数量': '2'})
    print(f"商品信息是：{sku_info}")
    order_code = order_interface.new_order(vip_name, sku_info)["Code"]
    base.fuzzy_search("订单编码", order_code)
    base.wait_element_click(base.get_cell_xpath(1, "订单编码"))
    base.click_space()
    element = base.wait_element(base.get_cell_xpath(1, "订单状态"))
    text = element.text
    base.wait_element_click(base.find_xpath("拆单"))
    base.wait_element(base.find_xpath("拆单", "按仓库拆包"))
    time.sleep(1)
    base.wait_element_click(base.find_xpath("拆单", "按仓库拆包"))
    time.sleep(1)
    with base.operate_page("订单", "打印发货", "打印发货框架"):
        start = datetime.datetime.now()
        while (datetime.datetime.now() - start).seconds < 30:
            base.fuzzy_search("发货单号", order_code)
            base.scroll_to(2)
            warehouse_list = base.get_column_text("仓库")
            if len(warehouse_list) == 2:
                assert "主仓库" in warehouse_list
                assert "测试仓" in warehouse_list
                break
        base.scroll_to(0)
        base.wait_element_click(base.get_cell_xpath("主仓库", "商品信息"))
        sku_code_list = delivery_order.get_all_float_sku_info("商家编码")
        for i in sku_code_list:
            assert i == main_sku_code
        base.wait_element_click(base.get_cell_xpath("测试仓", "商品信息"))
        sku_code_list = delivery_order.get_all_float_sku_info("商家编码")
        for i in sku_code_list:
            assert i == test_sku_code


def test_multi_split_with_weight():
    vip_name = "会员" + base.get_now_string()
    vip_interface.new_vip(vip_name)
    print(f"{vip_name}")
    product_code = base.get_now_string()
    product_interface.new_product(product_code)
    sku_code = product_interface.get_sku_code(product_code)[0]
    product_interface.modify_sku_price(sku_code, "100")
    sku_id_list = product_interface.get_sku_id("", product_code)
    modify_info_dict = {"重量": "1.0"}
    product_interface.multi_modify_sku_info(sku_id_list, modify_info_dict)
    sku_info = [{'商家编码': sku_code, '数量': '10'}]
    print(f"商品信息是：{sku_info}")
    order_code = order_interface.new_order(vip_name, sku_info)["Code"]
    base.fuzzy_search("订单编码", order_code)
    base.wait_element_click(base.get_cell_xpath(1, "订单编码"))
    base.click_space()
    element = base.wait_element(base.get_cell_xpath(1, "订单状态"))
    text = element.text
    base.wait_element_click(base.find_xpath("拆单"))
    base.wait_element(base.find_xpath("拆单", "按重量拆包"))
    time.sleep(1)
    base.wait_element_click(base.find_xpath("拆单", "按重量拆包"))
    time.sleep(1)
    with base.operate_page("订单", "打印发货", "打印发货框架"):
        start = datetime.datetime.now()
        while (datetime.datetime.now() - start).seconds < 30:
            base.fuzzy_search("发货单号", order_code)
            product_num_list = base.get_column_text("商品数")
            if len(product_num_list) == 4:
                assert ['1', '3', '3', '3'] == product_num_list
                break


def test_multi_split_with_inventory():
    # TODO:(RUI):全部订单页面 按照库存拆单报错：当前数据可能被其他人操作了，请刷新后重试！，请排查下审核问题，数据：测试专用 测试  8888     订单编码：TD200925016  正常情况下不会报错
    vip_name = "会员" + base.get_now_string()
    vip_interface.new_vip(vip_name)
    print(f"{vip_name}")
    product_code = base.get_now_string()
    product_interface.new_product(product_code)
    enough_sku_code_list = product_interface.get_sku_code(product_code)
    product_interface.modify_sku_price(enough_sku_code_list[0], "100")
    stock_in_sku_info = []
    stock_in_num = 0
    for enough_sku_code in enough_sku_code_list:
        stock_in_num += 2
        stock_in_sku_info .append({'商家编码': enough_sku_code, '数量': stock_in_num})
    stock_in_order_id = inventory_interface.new_stock_in_order("主仓库", "供应商1", stock_in_sku_info)["ID"]
    inventory_interface.stock_in_stock_in_order(stock_in_order_id)
    sku_info = []
    for enough_sku_code in enough_sku_code_list:
        sku_info .append({'商家编码': enough_sku_code, '数量': '3'})
    print(f"商品信息是：{sku_info}")
    product_code = base.get_now_string()
    product_interface.new_product(product_code)
    lack_sku_code_list = product_interface.get_sku_code(product_code)
    product_interface.modify_sku_price(lack_sku_code_list[0], "100")
    for lack_sku_code in lack_sku_code_list:
        sku_info.append({'商家编码': lack_sku_code, '数量': '5'})
    print(f"商品信息是：{sku_info}")
    order_code = order_interface.new_order(vip_name, sku_info)["Code"]
    base.fuzzy_search("订单编码", order_code)
    base.wait_element_click(base.get_cell_xpath(1, "订单编码"))
    base.click_space()
    element = base.wait_element(base.get_cell_xpath(1, "订单状态"))
    text = element.text
    base.wait_element_click(base.find_xpath("拆单"))
    base.wait_element(base.find_xpath("拆单", "按库存拆包"))
    time.sleep(1)
    base.wait_element_click(base.find_xpath("拆单", "按库存拆包"))
    time.sleep(1)
    with base.operate_page("订单", "打印发货", "打印发货框架"):
        start = datetime.datetime.now()
        while (datetime.datetime.now() - start).seconds < 30:
            base.fuzzy_search("发货单号", order_code)
            product_num_list = base.wait_element(base.get_cell_xpath(vip_name, "商品数")).text
            if int(product_num_list) == 9:
                print(f"按库存拆分：库存充足的库存全部拆包配货，库存不足的留下")
                break


def test_multi_split_to_one_sku_one_package():
    vip_name = "会员" + base.get_now_string()
    vip_interface.new_vip(vip_name)
    print(f"{vip_name}")
    product_code = base.get_now_string()
    product_interface.new_product(product_code)
    enough_sku_code_list = product_interface.get_sku_code(product_code)
    product_interface.modify_sku_price(enough_sku_code_list[0], "100")
    sku_info = []
    for enough_sku_code in enough_sku_code_list:
        sku_info.append({'商家编码': enough_sku_code, '数量': '3'})
    print(f"商品信息是：{sku_info}")
    sku_info.append({'商家编码': "测试商品1-红色 XS", '数量': '3'})
    order_code = order_interface.new_order(vip_name, sku_info)["Code"]
    base.fuzzy_search("订单编码", order_code)
    base.wait_element_click(base.get_cell_xpath(1, "订单编码"))
    base.click_space()
    element = base.wait_element(base.get_cell_xpath(1, "订单状态"))
    text = element.text
    base.wait_element_click(base.find_xpath("拆单"))
    base.wait_element(base.find_xpath("拆单", "单件成包"))
    time.sleep(1)
    base.wait_element_click(base.find_xpath("拆单", "单件成包"))
    time.sleep(1)
    with base.operate_page("订单", "打印发货", "打印发货框架"):
        start = datetime.datetime.now()
        while (datetime.datetime.now() - start).seconds < 30:
            base.fuzzy_search("发货单号", order_code)
            product_num_list = base.get_column_text("商品数")
            if int(len(product_num_list)) == 4:
                break
        assert ["21", "1", "1", "1"].sort() == product_num_list.sort()
        print(f"{product_num_list.sort()}")
        for i in range(1, 5):
            product_num_text = base.wait_element(base.get_cell_xpath(i, "商品数")).text
            print(product_num_text)
            if product_num_text == "1":
                base.wait_element_click(base.get_cell_xpath(i, "商品信息"))
                result = delivery_order.get_all_float_sku_info("商家编码")
                print(result)
                for j in result:
                    assert j == "测试商品1-红色 XS"
            elif product_num_text == "21":
                base.wait_element_click(base.get_cell_xpath(i, "商品信息"))
                result = delivery_order.get_all_float_sku_info("商家编码")
                print(result)
                assert result.sort() == enough_sku_code_list.sort()
            else:
                assert 1 == 2, "单件成包拆包结果不符合预期，请核实"


def test_multi_split_to_multi_sku_one_package():
    vip_name = "会员" + base.get_now_string()
    vip_interface.new_vip(vip_name)
    print(f"{vip_name}")
    product_code = base.get_now_string()
    product_interface.new_product(product_code)
    enough_sku_code_list = product_interface.get_sku_code(product_code)
    product_interface.modify_sku_price(enough_sku_code_list[0], "100")
    sku_info = []
    for enough_sku_code in enough_sku_code_list:
        sku_info.append({'商家编码': enough_sku_code, '数量': '3'})
    print(f"商品信息是：{sku_info}")
    sku_info.append({'商家编码': "测试商品1-红色 XXXXXXL", '数量': '3'})
    sku_info.append({'商家编码': "测试商品1-红色 6XL", '数量': '3'})
    order_code = order_interface.new_order(vip_name, sku_info)["Code"]
    base.fuzzy_search("订单编码", order_code)
    base.wait_element_click(base.get_cell_xpath(1, "订单编码"))
    base.click_space()
    element = base.wait_element(base.get_cell_xpath(1, "订单状态"))
    text = element.text
    base.wait_element_click(base.find_xpath("拆单"))
    base.wait_element(base.find_xpath("拆单", "多件成包"))
    time.sleep(1)
    base.wait_element_click(base.find_xpath("拆单", "多件成包"))
    time.sleep(1)
    with base.operate_page("订单", "打印发货", "打印发货框架"):
        start = datetime.datetime.now()
        while (datetime.datetime.now() - start).seconds < 30:
            base.fuzzy_search("发货单号", order_code)
            product_num_list = base.get_column_text("商品数")
            if int(len(product_num_list)) == 2:
                break
        assert ["21", "6"].sort() == product_num_list.sort()
        print(f"{product_num_list.sort()}")
        for i in range(1, 3):
            product_num_text = base.wait_element(base.get_cell_xpath(i, "商品数")).text
            print(product_num_text)
            if product_num_text == "6":
                base.wait_element_click(base.get_cell_xpath(i, "商品信息"))
                result = delivery_order.get_all_float_sku_info("商家编码")
                print(result)
                assert ["测试商品1-红色 XXXXXXL", "测试商品1-红色 6XL"].sort() == result.sort()
            elif product_num_text == "21":
                base.wait_element_click(base.get_cell_xpath(i, "商品信息"))
                result = delivery_order.get_all_float_sku_info("商家编码")
                print(result)
                assert result.sort() == enough_sku_code_list.sort()
            else:
                assert 1 == 2, "单件成包拆包结果不符合预期，请核实"


def test_modify_warehouse_and_express():
    vip_name = "会员" + base.get_now_string()
    vip_interface.new_vip(vip_name)
    print(f"{vip_name}")
    product_code = base.get_now_string()
    product_interface.new_product(product_code)
    enough_sku_code_list = product_interface.get_sku_code(product_code)
    product_interface.modify_sku_price(enough_sku_code_list[0], "100")
    sku_info = [{'商家编码': enough_sku_code_list[0], '数量': '3'}]
    order_code = order_interface.new_order(vip_name, sku_info)["Code"]
    base.fuzzy_search("订单编码", order_code)
    base.wait_element_click(base.get_cell_xpath(1, "订单编码"))
    base.click_space()
    modify_info = {"仓库": "测试仓", "快递": "EMS", }
    order.modify_warehouse_and_express(order_code, modify_info)
    warehouse_name = base.wait_element(base.get_cell_xpath(order_code, "仓库")).text
    assert "测试仓" in warehouse_name
    express_name = base.wait_element(base.get_cell_xpath(order_code, "快递")).text
    assert "EMS" in express_name


def test_modify_seller_memo():
    vip_name = "会员" + base.get_now_string()
    vip_interface.new_vip(vip_name)
    print(f"{vip_name}")
    product_code = base.get_now_string()
    product_interface.new_product(product_code)
    enough_sku_code_list = product_interface.get_sku_code(product_code)
    product_interface.modify_sku_price(enough_sku_code_list[0], "100")
    sku_info = [{'商家编码': enough_sku_code_list[0], '数量': '3'}]
    first_order_code = order_interface.new_order(vip_name, sku_info)["Code"]
    second_order_code = order_interface.new_order(vip_name, sku_info)["Code"]
    base.fuzzy_search("订单编码", vip_name)
    base.wait_element_click(base.get_cell_xpath(first_order_code, "订单编码"))
    base.click_space()
    modify_info = {"旗帜": "红旗", "备注": "第一次"}
    order.modify_seller_memo(first_order_code, modify_info)
    result = base.wait_element(base.get_cell_xpath(first_order_code, "卖家备注")).text
    assert "第一次" in result
    result = base.wait_element(base.get_cell_xpath(first_order_code, "旗帜")).text
    assert "红旗" in result
    modify_info = {"旗帜": "绿旗", "备注": "第二次", "追加": True}
    order.modify_seller_memo(first_order_code, modify_info)
    result = base.wait_element(base.get_cell_xpath(first_order_code, "卖家备注")).text
    assert "第二次" in result
    assert "第一次" in result
    result = base.wait_element(base.get_cell_xpath(first_order_code, "旗帜")).text
    assert "绿旗" in result
    print(f"再测试常用备注")
    modify_info = {"旗帜": "黄旗", "常用备注": "常用备注1"}
    order.modify_seller_memo(first_order_code, modify_info)
    result = base.wait_element(base.get_cell_xpath(first_order_code, "卖家备注")).text
    assert "常用备注1" in result
    assert "第二次" in result
    assert "第一次" in result
    result = base.wait_element(base.get_cell_xpath(first_order_code, "旗帜")).text
    assert "黄旗" in result
    base.select_all()
    print(f"----------------------------------试下勾选多个订单修改备注-------------------------------------")
    modify_info = {"旗帜": "蓝旗", "备注": "第三次"}
    order.modify_seller_memo(first_order_code, modify_info)
    result = base.get_column_text("卖家备注")
    for i in result:
        assert "第三次" in i
    result = base.get_column_text("旗帜")
    for i in result:
        assert "蓝旗" in result
    modify_info = {"旗帜": "紫旗", "备注": "第四次", "追加": True}
    order.modify_seller_memo(first_order_code, modify_info)
    result = base.get_column_text("卖家备注")
    for i in result:
        assert "第四次" in i
        assert "第三次" in i
    result = base.get_column_text("旗帜")
    for i in result:
        assert "紫旗" in result
    print(f"再测试常用备注")
    modify_info = {"旗帜": "黄旗", "常用备注": "常用备注2"}
    order.modify_seller_memo(first_order_code, modify_info)
    result = base.get_column_text("卖家备注")
    for i in result:
        assert "常用备注2" in i
    result = base.get_column_text("旗帜")
    for i in result:
        assert "黄旗" in result


def test_modify_note():
    vip_name = "会员" + base.get_now_string()
    vip_interface.new_vip(vip_name)
    print(f"{vip_name}")
    product_code = base.get_now_string()
    product_interface.new_product(product_code)
    enough_sku_code_list = product_interface.get_sku_code(product_code)
    product_interface.modify_sku_price(enough_sku_code_list[0], "100")
    sku_info = [{'商家编码': enough_sku_code_list[0], '数量': '3'}]
    first_order_code = order_interface.new_order(vip_name, sku_info)["Code"]
    second_order_code = order_interface.new_order(vip_name, sku_info)["Code"]
    base.fuzzy_search("订单编码", vip_name)
    base.wait_element_click(base.get_cell_xpath(first_order_code, "订单编码"))
    base.click_space()
    modify_info = {"便签": "第一次", "追加": False}
    order.modify_note(first_order_code, modify_info)
    result = base.wait_element(base.get_cell_xpath(first_order_code, "便签")).text
    assert "第一次" in result
    modify_info = {"便签": "第二次", "追加": True}
    order.modify_note(first_order_code, modify_info)
    result = base.wait_element(base.get_cell_xpath(first_order_code, "便签")).text
    assert "第二次" in result
    assert "第一次" in result
    print(f"再测试常用便签")
    modify_info = {"常用便签": "常用便签1", "追加": False}
    order.modify_note(first_order_code, modify_info)
    result = base.wait_element(base.get_cell_xpath(first_order_code, "便签")).text
    assert "常用便签1" in result
    assert "第二次" not in result
    assert "第一次" not in result
    print(f"再测试系统标签")
    modify_info = {"系统便签": "爆款订单", "追加": True}
    order.modify_note(first_order_code, modify_info)
    result = base.wait_element(base.get_cell_xpath(first_order_code, "便签")).text
    assert "常用便签1" in result
    assert "爆款订单" in result
    base.select_all()
    print(f"----------------------------------试下勾选多个订单修改备注-------------------------------------")
    modify_info = {"便签": "第三次", "追加": False}
    order.modify_note(first_order_code, modify_info)
    result = base.get_column_text("便签")
    for i in result:
        assert "第三次" in i
    modify_info = {"便签": "第四次", "追加": True}
    order.modify_note(first_order_code, modify_info)
    result = base.get_column_text("便签")
    for i in result:
        assert "第四次" in i
        assert "第三次" in i
    print(f"再测试常用便签")
    modify_info = {"常用便签": "常用便签2", "追加": False}
    order.modify_note(first_order_code, modify_info)
    result = base.get_column_text("便签")
    for i in result:
        assert "常用便签2" in i
    print(f"再测试系统便签")
    modify_info = {"系统便签": "装车拦截", "追加": True}
    order.modify_note(first_order_code, modify_info)
    result = base.get_column_text("便签")
    for i in result:
        assert "常用便签2" in i
        assert "装车拦截" in i


def test_modify_address():
    vip_name = "会员" + base.get_now_string()
    vip_interface.new_vip(vip_name)
    print(f"{vip_name}")
    product_code = base.get_now_string()
    product_interface.new_product(product_code)
    enough_sku_code_list = product_interface.get_sku_code(product_code)
    product_interface.modify_sku_price(enough_sku_code_list[0], "100")
    sku_info = [{'商家编码': enough_sku_code_list[0], '数量': '3'}]
    first_order_code = order_interface.new_order(vip_name, sku_info)["Code"]
    second_order_code = order_interface.new_order(vip_name, sku_info)["Code"]
    base.fuzzy_search("订单编码", vip_name)
    base.wait_element_click(base.get_cell_xpath(first_order_code, "订单编码"))
    base.click_space()
    modify_seller_memo_info = {"备注": "修改地址显示卖家备注"}
    order.modify_seller_memo(first_order_code, modify_seller_memo_info)
    modify_info = {"收货地址": "江苏省南京市鼓楼区鼓楼大道1185号", "收货人名": "芮苏云", "联系电话": "02133668823", "联系手机": "13772839830",
                   "邮政编码": "211458", "核对备注": "修改地址显示卖家备注"}
    order.modify_address(first_order_code, modify_info)
    result = base.wait_element(base.get_cell_xpath(first_order_code, "收货地址")).text
    assert "鼓楼大道1185号" in result
    result = base.wait_element(base.get_cell_xpath(first_order_code, "省")).text
    assert "江苏省" in result
    result = base.wait_element(base.get_cell_xpath(first_order_code, "市")).text
    assert "南京市" in result
    result = base.wait_element(base.get_cell_xpath(first_order_code, "区")).text
    assert "鼓楼区" in result
    result = base.wait_element(base.get_cell_xpath(first_order_code, "收货人")).text
    assert "芮苏云" in result
    result = base.wait_element(base.get_cell_xpath(first_order_code, "手机号")).text
    assert "13772839830" in result
    base.select_all()
    print(f"----------------------------------试下勾选多个订单修改地址-------------------------------------")
    modify_info = {"选择地址": f"芮苏云,13772839830,江苏省 南京市 鼓楼区 鼓楼大道1185号"}
    order.modify_address(vip_name, modify_info)
    result_list = base.get_column_text('收货地址')
    for i in result_list:
        assert "江苏省 南京市 鼓楼区 鼓楼大道1185号" in i
    result_list = base.get_column_text('省')
    for i in result_list:
        assert "江苏省" in i
    result_list = base.get_column_text('市')
    for i in result_list:
        assert "南京市" in i
    result_list = base.get_column_text('区')
    for i in result_list:
        assert "鼓楼区" in i
    result_list = base.get_column_text('收货人')
    for i in result_list:
        assert "芮苏云" in i
    result_list = base.get_column_text('手机号')
    for i in result_list:
        assert "13772839830" in i


def test_multi_mark_memo_processed():
    setting_info = {"开启": "true", "会员相同": "true"}
    setting_interface.save_auto_merge_setting(setting_info)
    time.sleep(5)
    print(f"开启合单设置之后等待五秒生效")
    vip_name = "会员" + base.get_now_string()
    vip_interface.new_vip(vip_name)
    print(f"{vip_name}")
    product_code = base.get_now_string()
    product_interface.new_product(product_code)
    enough_sku_code_list = product_interface.get_sku_code(product_code)
    product_interface.modify_sku_price(enough_sku_code_list[0], "100")
    sku_info = [{'商家编码': enough_sku_code_list[0], '数量': '3'}]
    first_order_code = order_interface.new_order(vip_name, sku_info, "主仓库", "买家自提", "巨淘气", {"卖家备注": "111"})["Code"]
    second_order_code = order_interface.new_order(vip_name, sku_info, "主仓库", "买家自提", "巨淘气", {"买家备注": "222"})["Code"]
    third_order_code = order_interface.new_order(vip_name, sku_info)["Code"]
    base.wait_element_click(base.find_xpath("订单状态", "待审核（有备注）"))
    time.sleep(1)
    base.fuzzy_search("订单编码", vip_name)
    result = base.get_column_text("会员名")
    assert len(result) == 3
    base.wait_element_click(base.get_cell_xpath(first_order_code, "订单编码"))
    base.click_space()
    base.wait_element_click(base.find_xpath("修改&标记"))
    with base.wait_refresh(base.get_cell_xpath(first_order_code, "卖家备注")):
        base.wait_element_click(base.find_xpath("修改&标记", "标记备注已处理"))
    result = base.wait_element(base.get_cell_xpath(first_order_code, "卖家备注")).text
    print(f"{result}")
    assert result.replace("\n改", "").endswith("#")




if __name__ == '__main__':
    pytest.main()
