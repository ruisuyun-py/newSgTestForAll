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


# 测试批量搜索功能
def test_multi_search():  # TODO:("RUI"):优化刷新方法
    # 测试批量搜索会员名称
    """
    目前支持的类型共有4种：会员名称，平台单号，物流单号，地址（未发货）
    1.先进行会员名称批量搜索
        先打开文件，读取数据，然后使用批量搜索并对比结果
        会员名称可以搜索所有订单的会员，包括 未审核，已审核，已出库等
    2.再进行物流单号批量搜索
        物流单号可搜索所哟状态，包括已出库，未出库
    3.之后是平台单号
        只要是系统中的平台单号都能搜索，platform_order_code.txt 中包含未审核，发货中，已出库的平台单号
    4.最后是地址
            地址比较特殊，只搜索未审核的订单地址，包含未审核，和部分审核，文件中给了3种
            address_list.txt 中是未审核，部分审核的
            not_found_address_list.txt 包含已审核，已出库的地址和找不到的地址
    全部通过数据文件使用固定数据进行测试
    批量搜索提示不要超过200，其实超过了没事，只不过可能查询时间会比较长
    """
    # ————————————————————————————
    # 111111111111111111111111111111
    # 先进行会员名称测试
    # 111111111111111111111111111111
    # ————————————————————————————
    # 获取当前文件的目录
    cur_path = os.path.abspath(os.path.dirname(__file__))
    # 获取根目录
    root_path = cur_path[:cur_path.find("newSgTestForAll\\") + len("newSgTestForAll\\")]
    with open(root_path + '/test_dir/saas/order/all_order/file_for_multi_search/vip_list.txt', 'r',
              encoding='UTF-8') as f:
        vip_list = f.readlines()
    f.close()
    with open(root_path + '/test_dir/saas/order/all_order/file_for_multi_search/not_found_vip_list.txt', 'r',
              encoding='UTF-8') as f:
        not_found_vip_list = f.readlines()
    f.close()
    base.wait_element_click(order.locations["批量搜索下拉按钮"])
    base.wait_element(base.find_xpath("搜索类型", "买家账号")).click()
    for v in vip_list:
        base.wait_element(order.locations["批量搜索文本框"]).send_keys(v)
    for v in not_found_vip_list:
        base.wait_element(order.locations["批量搜索文本框"]).send_keys(v)
    base.wait_table_refresh(base.find_xpath("每行一个", "确认"), 1, "会员名")
    base.driver.switch_to.default_content()
    not_found_vip_result = base.wait_element(base.find_xpath("信息", "以下买家账号没有搜索到")).text.split("\n")
    not_found_vip_result.pop(0)
    print(not_found_vip_result)
    for v in not_found_vip_result:
        assert v + '\n' in not_found_vip_list
    time.sleep(1)
    base.wait_element(base.find_xpath("信息", "确定")).click()
    base.driver.switch_to.default_content()
    base.switch_to_frame(base.locations["全部订单框架"])
    vip_result = base.get_column_text("会员名")
    for v in vip_result:
        assert v + '\n' in vip_list
    # ————————————————————————————
    # 22222222222222222222222222222222
    # 再进行物流单号测试
    # 22222222222222222222222222222222
    # ————————————————————————————
    time.sleep(1)
    base.wait_table_refresh(base.find_xpath('清空'), 1, '会员名')
    # 测试批量搜索物流单号
    with open(root_path + '/test_dir/saas/order/all_order/file_for_multi_search/express_code.txt', 'r',
              encoding='UTF-8') as f:
        express_code_list = f.readlines()
    f.close()
    with open(root_path + '/test_dir/saas/order/all_order/file_for_multi_search/not_found_express_code_list.txt', 'r',
              encoding='UTF-8') as f:
        not_found_express_code_list = f.readlines()
    f.close()
    base.wait_element_click(order.locations["批量搜索下拉按钮"])
    base.wait_element(base.find_xpath("搜索类型", "物流单号")).click()
    for v in express_code_list:
        base.wait_element(order.locations["批量搜索文本框"]).send_keys(v)
    for v in not_found_express_code_list:
        base.wait_element(order.locations["批量搜索文本框"]).send_keys(v)
    base.wait_table_refresh(base.find_xpath("每行一个", "确认"), 1, "会员名")
    base.driver.switch_to.default_content()
    not_found_express_code_result = base.wait_element(base.find_xpath("信息", "以下物流单号没有搜索到")).text.split("\n")
    print(not_found_express_code_result)
    not_found_express_code_result.pop(0)
    print(not_found_express_code_result)
    for v in not_found_express_code_result:
        assert v + '\n' in not_found_express_code_list
    time.sleep(1)
    base.wait_element(base.find_xpath("信息", "确定")).click()
    base.driver.switch_to.default_content()
    base.switch_to_frame(base.locations["全部订单框架"])
    vip_result = base.get_column_text("会员名")
    # 全部订单页面没有物流单号字段只能使用会员名称替代下
    with open(root_path + '/test_dir/saas/order/all_order/file_for_multi_search/express_code_vip_name_result.txt', 'r',
              encoding='UTF-8') as f:
        vip_name_result = f.readlines()
    f.close()
    for v in vip_result:
        assert v + '\n' in vip_name_result
    # ————————————————————————————
    # 33333333333333333333333333333333
    # 之后是平台单号测试
    # 33333333333333333333333333333333
    # ————————————————————————————
    time.sleep(1)
    base.wait_table_refresh(base.find_xpath('清空'), 1, '会员名')
    # 开始平台单号批量搜索测试
    with open(root_path + '/test_dir/saas/order/all_order/file_for_multi_search/platform_order_code.txt', 'r',
              encoding='UTF-8') as f:
        platform_order_code_list = f.readlines()
    f.close()
    with open(root_path + '/test_dir/saas/order/all_order/file_for_multi_search/not_found_platform_order_code.txt', 'r',
              encoding='UTF-8') as f:
        not_found_platform_order_code_list = f.readlines()
    f.close()
    base.wait_element_click(order.locations["批量搜索下拉按钮"])
    base.wait_element(base.find_xpath("搜索类型", "平台单号")).click()
    for v in platform_order_code_list:
        base.wait_element(order.locations["批量搜索文本框"]).send_keys(v)
    for v in not_found_platform_order_code_list:
        base.wait_element(order.locations["批量搜索文本框"]).send_keys(v)
    base.wait_table_refresh(base.find_xpath("每行一个", "确认"), 1, "会员名")
    base.driver.switch_to.default_content()
    not_found_platform_order_code_result = base.wait_element(base.find_xpath("信息", "以下")).text.split("\n")
    print(not_found_platform_order_code_result)
    not_found_platform_order_code_result.pop(0)
    print(not_found_platform_order_code_result)
    for v in not_found_platform_order_code_result:
        assert v + '\n' in not_found_platform_order_code_list
    time.sleep(1)
    base.wait_element(base.find_xpath("信息", "确定")).click()
    base.driver.switch_to.default_content()
    base.switch_to_frame(base.locations["全部订单框架"])
    platform_order_code_result = base.get_column_text("平台单号")
    for v in platform_order_code_result:
        assert v + '\n' in platform_order_code_list
    # ————————————————————————————
    # 4444444444444444444444444444444444
    # 最后是地址
    # 4444444444444444444444444444444444
    # ————————————————————————————
    time.sleep(1)
    base.wait_table_refresh(base.find_xpath('清空'), 1, '会员名')
    # 最后开始地址（未发货）批量搜索测试
    with open(root_path + '/test_dir/saas/order/all_order/file_for_multi_search/address_list.txt', 'r',
              encoding='UTF-8') as f:
        address_list = f.readlines()
    f.close()
    print(address_list)
    with open(root_path + '/test_dir/saas/order/all_order/file_for_multi_search/not_found_address_list.txt', 'r',
              encoding='UTF-8') as f:
        not_found_address_list = f.readlines()
    f.close()
    print(not_found_address_list)
    base.wait_element_click(order.locations["批量搜索下拉按钮"])
    base.wait_element(base.find_xpath("搜索类型", "地址")).click()
    for v in address_list:
        base.wait_element(order.locations["批量搜索文本框"]).send_keys(v)
    for v in not_found_address_list:
        base.wait_element(order.locations["批量搜索文本框"]).send_keys(v)
    base.wait_table_refresh(base.find_xpath("每行一个", "确认"), 1, "会员名")
    base.driver.switch_to.default_content()
    not_found_address_result = base.wait_element(base.find_xpath("信息", "以下")).text.split("\n")
    print(not_found_address_result)
    not_found_address_result.pop(0)
    print(not_found_address_result)
    for v in not_found_address_result:
        assert v + '\n' in not_found_address_list
    time.sleep(1)
    base.wait_element(base.find_xpath("信息", "确定")).click()
    base.driver.switch_to.default_content()
    base.switch_to_frame(base.locations["全部订单框架"])
    base.scroll_to(5)
    address_result = base.get_column_text("收货地址")
    for v in address_result:
        assert v.replace('\n改', '') + '\n' in address_list


# 测试模糊搜索功能
def test_fuzzy_search():
    """
    订单编码，平台单号，买家帐号，收货人姓名，收货人手机，收货人电话，物流单号
    """
    column_name_list = ["订单编码", "平台单号", "会员名", "收货人", "手机号"]
    for i in column_name_list:
        test.fuzzy_search_test(i)
    result = delivery_interface.get_delivered_order_info({}, ["物流单号", "会员名称"])
    print(result)
    for i in range(0, 10):
        express_code = result[i]["物流单号"]
        vip_name = result[i]["会员名称"]
        print(f"物流单号:{express_code}")
        print(f"会员名：{vip_name}")
        base.fuzzy_search("会员名", express_code)
        vip_name_search_result = base.get_column_text("会员名")[0]
        print(f"会员名搜索结果：{vip_name_search_result}")
        assert vip_name == vip_name_search_result


# 待审核（无备注）
def test_wait_to_approve_with_out_memo():
    print("验证待审核无备注订单的状态均为待审核，且买家备注和卖家备注均为空或者以#结尾")
    base.wait_element(base.find_xpath_with_spaces("待审核（无备注）"))
    time.sleep(1)
    base.wait_element_click(base.find_xpath_with_spaces("待审核（无备注）"))
    base.wait_table_refresh(base.find_xpath("组合查询"), 1, "订单编码")
    result = base.get_column_text("订单状态")
    for i in result:
        assert i == "待审核"
    seller_memo = base.get_column_text("卖家备注")
    buyer_memo = base.get_column_text("买家备注")
    for i in range(0, len(seller_memo)):
        assert (seller_memo[i] == "" or seller_memo[i].endswith("#")) and (
                buyer_memo[i] == "" or buyer_memo[i].endswith("#"))
    print(f"验证商品信息没有任何商品被审核")
    elements = base.wait_elements(base.get_column_xpath("商品信息"))
    j = 0
    for e in elements:
        j += 1
        e.click()
        other_inf = order.get_all_float_sku_info("其他信息")
        has_no_sku_approve = True
        for i in range(0, len(other_inf)):
            print(f"第{j}行订单的第{i + 1}行的其他信息：{other_inf[i]}")
            if "审" in other_inf[i]:
                has_no_sku_approve = False
                break
        assert has_no_sku_approve


# 待审核（有备注）
def test_wait_to_approve_with_memo():
    print("验证待审核有备注的订单状态为待审核，并且买家备注买家备注中必须有一个不为空，且不以# 结尾")
    base.wait_element_click(base.find_xpath_with_spaces("待审核（有备注）"))
    base.wait_table_refresh(base.find_xpath("组合查询"), 1, "订单编码")
    result = base.get_column_text("订单状态")
    for i in result:
        assert i == "待审核"
    seller_memo = base.get_column_text("卖家备注")
    buyer_memo = base.get_column_text("买家备注")
    for i in range(0, len(seller_memo)):
        print(f"seller_memo:{seller_memo[i]} +buyer_memo:{buyer_memo[i]}")
        has_memo = (seller_memo[i] != "" and not seller_memo[i].endswith("#")) or (
                buyer_memo[i] != "" and not buyer_memo[i].endswith("#"))
        if not has_memo:
            print(f"待合并订单备注则该订单也算有备注，但凡买家备注，卖家备注均为空，则必然存在一个待合并订单有买家备注，卖家备注")
            order_sum = base.wait_element(base.get_cell_xpath(i + 1, "订单数")).text
            assert int(order_sum) >= 2
            base.wait_element_click(base.get_cell_xpath(i + 1, "订单数", order_sum))
            base.change_frame("全部订单框架", "会员未出库订单页面")
            old_seller_memo = base.get_old_column_text("卖家备注")
            print("未出库订单的卖家备注为：")
            for k in old_seller_memo:
                print(f"{k}")
            old_buyer_memo = base.get_old_column_text("买家备注")
            print(f"未出库订单的买家备注为：")
            for k in old_buyer_memo:
                print(f"{k}")
            one_order_has_memo = False
            for j in range(0, len(old_seller_memo)):
                one_order_has_memo = (old_seller_memo[j] != "" and not old_seller_memo[j].endswith("#")) or (
                        old_buyer_memo[j] != "" and not old_buyer_memo[j].endswith("#"))
                if one_order_has_memo:
                    print(f"未出库订单有备注的行号是{j + 1}")
                    order_info = base.wait_element(base.get_old_cell_xpath(j + 1, "订单编码+平台单号")).text
                    print(f"有备注的待合并订单信息为{order_info}")
                    print(f"待合并订单的卖家备注为{old_seller_memo[j]}，买家备注为{old_buyer_memo[j]}")
                    break
            base.change_frame("全部订单框架")
            base.wait_element_click(base.find_xpath_by_tag_name("会员未出库订单页面", "a"))
            print(f"")
            assert one_order_has_memo
    print(f"验证商品信息没有任何商品被审核")
    base.wait_table_refresh(base.find_xpath("组合查询"), 1, "订单编码")
    elements = base.wait_elements(base.get_column_xpath("商品信息"))
    j = 0
    for e in elements:
        j += 1
        e.click()
        other_inf = order.get_all_float_sku_info("其他信息")
        has_no_sku_approve = True
        for i in range(0, len(other_inf)):
            print(f"第{j}行订单的第{i + 1}行的其他信息：{other_inf[i]}")
            if "审" in other_inf[i]:
                has_no_sku_approve = False
                break
        assert has_no_sku_approve


# 待审核（拆单）
def test_wait_to_approve_with_split():
    base.wait_element_click(base.find_xpath_with_spaces("待审核（拆单）"))
    base.wait_table_refresh(base.find_xpath("组合查询"), 1, "订单编码")
    result = base.get_column_text("订单状态")
    for i in result:
        assert i == "部分审核"
    elements = base.wait_elements(base.get_column_xpath("商品信息"))
    j = 0
    for e in elements:
        j += 1
        e.click()
        other_inf = order.get_all_float_sku_info("其他信息")
        print(f"必须有至少一个商品被审核")
        has_one_sku_approve = False
        for i in range(0, len(other_inf)):
            print(f"第{j}行订单的第{i + 1}行的其他信息：{other_inf[i]}")
            if "审" in other_inf[i]:
                has_one_sku_approve = True
                break
        assert has_one_sku_approve
        print("必须至少有一个商品没有被全部审核")
        has_one_sku_not_approve_all = False
        for i in range(0, len(other_inf)):
            print(f"第{j}行订单的第{i + 1}行的其他信息：{other_inf[i]}")
            if "已全审" not in other_inf[i]:
                has_one_sku_not_approve_all = True
                break
        assert has_one_sku_not_approve_all


# 发货中
def test_delivery():
    base.wait_element_click(base.find_xpath_with_spaces("发货中"))
    base.wait_table_refresh(base.find_xpath("组合查询"), 1, "订单编码")
    result = base.get_column_text("订单状态")
    for i in result:
        assert "发货中" in i or "部分审核" in i


# 已发货
def test_delivered():
    base.wait_element_click(base.find_xpath_with_spaces("已发货"))
    base.wait_table_refresh(base.find_xpath("组合查询"), 1, "订单编码")
    result = base.get_column_text("订单状态")
    for i in result:
        assert "已发货" in i
    elements = base.wait_elements(base.get_column_xpath("商品信息"))
    j = 0
    for e in elements:
        j += 1
        e.click()
        other_inf = order.get_all_float_sku_info("其他信息")
        print(f"所有商品必须全部发货")
        has_one_sku_not_delivered = False
        for i in range(0, len(other_inf)):
            print(f"第{j}行订单的第{i + 1}行的其他信息：{other_inf[i]}")
            if "已全审全部出库" not in other_inf[i]:
                has_one_sku_not_delivered = True
                break
        assert not has_one_sku_not_delivered


# 已终结
def test_ended():
    base.wait_element_click(base.find_xpath_with_spaces("已终结"))
    base.wait_table_refresh(base.find_xpath("组合查询"), 1, "订单编码")
    result = base.get_column_text("订单状态")
    for i in result:
        assert "已终结" in i


# 黑名单
def test_black_list():
    base.wait_element_click(base.find_xpath("异常", "未审核有异常"))
    base.wait_element_click(base.find_xpath("未审核有异常", "黑名单"))
    base.wait_table_refresh(base.find_xpath("组合查询"), 1, "订单编码")
    order_sum_text = base.wait_element(base.find_xpath("已选择", "本页共")).text
    if order_sum_text == "本页共0条数据":
        print(f"没数据不用看")
    else:
        result = base.get_column_text("订单状态")
        for i in result:
            assert "黑名单" in i


# 线上改商品
def test_modify_sku_info_online():
    base.wait_element_click(base.find_xpath("异常", "未审核有异常"))
    base.wait_element_click(base.find_xpath("未审核有异常", "线上改商品"))
    base.wait_table_refresh(base.find_xpath("组合查询"), 1, "订单编码")
    order_sum_text = base.wait_element(base.find_xpath("已选择", "本页共")).text
    if order_sum_text == "本页共0条数据":
        print(f"没数据不用看")
    else:
        result = base.get_column_text("订单状态")
        for i in result:
            assert "线上改商品" in i


# 标记异常
def test_mark_exception():
    base.wait_element_click(base.find_xpath("异常", "未审核有异常"))
    base.wait_element_click(base.find_xpath("未审核有异常", "标记异常"))
    base.wait_table_refresh(base.find_xpath("组合查询"), 1, "订单编码")
    order_sum_text = base.wait_element(base.find_xpath("已选择", "本页共")).text
    if order_sum_text == "本页共0条数据":
        print(f"没数据不用看")
    else:
        result = base.get_column_text("订单状态")
        for i in result:
            assert "未审核" not in i
        elements = base.wait_elements(base.get_column_xpath("商品信息"))
        j = 0
        print(f"必须没有一个商品被审核")
        for e in elements:
            j += 1
            e.click()
            other_inf = order.get_all_float_sku_info("其他信息")
            has_one_sku_approved = False
            for i in range(0, len(other_inf)):
                print(f"第{j}行订单的第{i + 1}行的其他信息：{other_inf[i]}")
                if "审" in other_inf[i]:
                    has_one_sku_approved = True
                    break
            assert not has_one_sku_approved
    base.wait_element_click(base.find_xpath_by_placeholder("搜索异常"))
    normal_exception_list = order.get_normal_exception()
    print(f"常用异常列表：")
    for i in normal_exception_list:
        print(i)
    for i in normal_exception_list:
        base.wait_element_click(base.find_xpath_by_placeholder("搜索异常"))
        base.wait_element_click(base.find_xpath("线上改商品", i))
        element = base.wait_element(base.find_xpath("已选择", "加载"))
        text = element.text
        base.wait_element_click(base.find_xpath("组合查询"))
        base.wait_element_refresh(element, text)
        order_sum_text = base.wait_element(base.find_xpath("已选择", "本页共")).text
        if order_sum_text == "本页共0条数据":
            print(f"没数据不用看")
        else:
            result = base.get_column_text("订单状态")
            for j in result:
                assert i in j


# 线上改地址
def test_modify_address_online_exception():
    base.wait_element_click(base.find_xpath("异常", "未审核有异常"))
    base.wait_element_click(base.find_xpath("未审核有异常", "线上修改地址"))
    base.wait_table_refresh(base.find_xpath("组合查询"), 1, "订单编码")
    order_sum_text = base.wait_element(base.find_xpath("已选择", "本页共")).text
    if order_sum_text == "本页共0条数据":
        print(f"没数据不用看")
    else:
        result = base.get_column_text("订单状态")
        for i in result:
            assert "线上修改地址" in i


# 未设置仓库
def test_no_warehouse_exception():
    base.wait_element_click(base.find_xpath("异常", "未审核有异常"))
    base.wait_element_click(base.find_xpath("未审核有异常", "未设置仓库"))
    base.wait_table_refresh(base.find_xpath("组合查询"), 1, "订单编码")
    order_sum_text = base.wait_element(base.find_xpath("已选择", "本页共")).text
    if order_sum_text == "本页共0条数据":
        print(f"没数据不用看")
    else:
        result = base.get_column_text("订单状态")
        for i in result:
            assert "未设置仓库" in i


# 未设置快递
def test_no_express_exception():
    base.wait_element_click(base.find_xpath("异常", "未审核有异常"))
    base.wait_element_click(base.find_xpath("未审核有异常", "未设置快递"))
    base.wait_table_refresh(base.find_xpath("组合查询"), 1, "订单编码")
    order_sum_text = base.wait_element(base.find_xpath("已选择", "本页共")).text
    if order_sum_text == "本页共0条数据":
        print(f"没数据不用看")
    else:
        result = base.get_column_text("订单状态")
        for i in result:
            assert "未设置快递" in i


# 收货信息不完整
def test_incomplete_receiving_information_exception():
    base.wait_element_click(base.find_xpath("异常", "未审核有异常"))
    base.wait_element_click(base.find_xpath("未审核有异常", "收货信息不完整"))
    base.wait_table_refresh(base.find_xpath("组合查询"), 1, "订单编码")
    order_sum_text = base.wait_element(base.find_xpath("已选择", "本页共")).text
    if order_sum_text == "本页共0条数据":
        print(f"没数据不用看")
    else:
        result = base.get_column_text("订单状态")
        for i in result:
            assert "收货信息不完整" in i


# 手工终止发货
def test_manual_ended_exception():
    base.wait_element_click(base.find_xpath("异常", "未审核有异常"))
    base.wait_element_click(base.find_xpath("未审核有异常", "手工终止发货"))
    base.wait_table_refresh(base.find_xpath("组合查询"), 1, "订单编码")
    order_sum_text = base.wait_element(base.find_xpath("已选择", "本页共")).text
    if order_sum_text == "本页共0条数据":
        print(f"没数据不用看")
    else:
        result = base.get_column_text("订单状态")
        for i in result:
            assert "手工终止发货" in i


# 商品未匹配异常
def test_product_not_matched_exception():
    base.wait_element_click(base.find_xpath("异常", "未审核有异常"))
    base.wait_element_click(base.find_xpath("未审核有异常", "商品未匹配"))
    base.wait_table_refresh(base.find_xpath("组合查询"), 1, "订单编码")
    order_sum_text = base.wait_element(base.find_xpath("已选择", "本页共")).text
    if order_sum_text == "本页共0条数据":
        print(f"没数据不用看")
    else:
        result = base.get_column_text("订单状态")
        for i in result:
            assert "商品未匹配" in i


# 付款异常
def test_payment_exception():
    base.wait_element_click(base.find_xpath("异常", "未审核有异常"))
    base.wait_element_click(base.find_xpath("未审核有异常", "付款异常"))
    base.wait_table_refresh(base.find_xpath("组合查询"), 1, "订单编码")
    order_sum_text = base.wait_element(base.find_xpath("已选择", "本页共")).text
    if order_sum_text == "本页共0条数据":
        print(f"没数据不用看")
    else:
        result = base.get_column_text("订单状态")
        for i in result:
            assert "付款异常" in i
        base.scroll_to(5)
        result = base.get_column_text("未付金额")
        for i in result:
            assert float(i) != 0.00


def test_all_refund_exception():
    base.wait_element_click(base.find_xpath("异常", "未审核有异常"))
    base.wait_element_click(base.find_xpath("未审核有异常", "全部退款"))
    base.wait_table_refresh(base.find_xpath("组合查询"), 1, "订单编码")
    order_sum_text = base.wait_element(base.find_xpath("已选择", "本页共")).text
    if order_sum_text == "本页共0条数据":
        print(f"没数据不用看")
    else:
        result = base.get_column_text("订单状态")
        for i in result:
            assert "全部退款" in i


# 部分退款
def test_part_refund_exception():
    base.wait_element_click(base.find_xpath("异常", "未审核有异常"))
    base.wait_element_click(base.find_xpath("未审核有异常", "部分退款"))
    base.wait_table_refresh(base.find_xpath("组合查询"), 1, "订单编码")
    order_sum_text = base.wait_element(base.find_xpath("已选择", "本页共")).text
    if order_sum_text == "本页共0条数据":
        print(f"没数据不用看")
    else:
        result = base.get_column_text("订单状态")
        for i in result:
            assert "部分退款" in i


# 无商品信息
def test_with_out_sku_info_exception():
    base.wait_element_click(base.find_xpath("异常", "未审核有异常"))
    base.wait_element_click(base.find_xpath("未审核有异常", "无商品信息"))
    base.wait_table_refresh(base.find_xpath("组合查询"), 1, "订单编码")
    order_sum_text = base.wait_element(base.find_xpath("已选择", "本页共")).text
    if order_sum_text == "本页共0条数据":
        print(f"没数据不用看")
    else:
        result = base.get_column_text("订单状态")
        for i in result:
            assert "无商品信息" in i


# 其他erp已发货
def test_other_erp_delivered_exception():
    base.wait_element_click(base.find_xpath("异常", "未审核有异常"))
    base.wait_element_click(base.find_xpath("未审核有异常", "其他ERP已发货"))
    base.wait_table_refresh(base.find_xpath("组合查询"), 1, "订单编码")
    order_sum_text = base.wait_element(base.find_xpath("已选择", "本页共")).text
    if order_sum_text == "本页共0条数据":
        print(f"没数据不用看")
    else:
        result = base.get_column_text("订单状态")
        for i in result:
            assert "其他ERP已发货" in i


# 先上锁定异常
def test_locked_online_exception():
    base.wait_element_click(base.find_xpath("异常", "未审核有异常"))
    base.wait_element_click(base.find_xpath("未审核有异常", "线上锁定"))
    base.wait_table_refresh(base.find_xpath("组合查询"), 1, "订单编码")
    order_sum_text = base.wait_element(base.find_xpath("已选择", "本页共")).text
    if order_sum_text == "本页共0条数据":
        print(f"没数据不用看")
    else:
        result = base.get_column_text("订单状态")
        for i in result:
            assert "线上锁定" in i


# 待合并订单异常
def test_wait_merger_order_exception():
    base.wait_element_click(base.find_xpath("异常", "未审核有异常"))
    base.wait_element_click(base.find_xpath("未审核有异常", "待合并订单异常"))
    base.wait_table_refresh(base.find_xpath("组合查询"), 1, "订单编码")
    order_sum_text = base.wait_element(base.find_xpath("已选择", "本页共")).text
    if order_sum_text == "本页共0条数据":
        print(f"没数据不用看")
    else:
        result = base.get_column_text("订单状态")
        for i in result:
            assert i in ["待审核", "部分审核"]
        print("验证订单数必须大于2且必须至少有一个待合并订单状态异常")
        for i in range(1, len(result)):
            order_sum = base.wait_element(base.get_cell_xpath(i + 1, "订单数")).text
            assert int(order_sum) >= 2
            base.wait_element_click(base.get_cell_xpath(i + 1, "订单数", order_sum))
            base.change_frame("全部订单框架", "会员未出库订单页面")
            one_order_has_exception_at_least = False
            k = 0
            while not one_order_has_exception_at_least:
                k += 1
                order_status = base.wait_element(base.get_old_cell_xpath(k, "订单状态")).text
                if order_status not in ["待审核", "部分审核", "发货中"]:
                    one_order_has_exception_at_least = True
                    print(f"异常订单状态为: {order_status}")
                    break
            assert one_order_has_exception_at_least
            base.change_frame("全部订单框架")
            base.wait_element_click(base.find_xpath_by_tag_name("会员未出库订单页面", "a"))
            time.sleep(1)


def test_buyer_memo_search_condition():
    base.wait_element_click(base.find_xpath_with_spaces("买家留言"))
    base.wait_element_click(base.find_xpath("买家留言", "无留言"))
    base.wait_table_refresh(base.find_xpath("组合查询"), 1, "买家备注")
    result = list(set(base.get_column_text("买家备注")))
    for i in result:
        assert i == ""
    base.wait_element_click(base.find_xpath("买家留言", "有留言"))
    base.wait_table_refresh(base.find_xpath("组合查询"), 1, "买家备注")
    result = list(set(base.get_column_text("买家备注")))
    for i in result:
        assert i != ""
    for i in result:
        buyer_memo = i.strip("#")
        print(f"搜索买家留言：{buyer_memo}")
        base.wait_element(base.find_xpath_by_placeholder("买家留言模糊搜索")).send_keys(Keys.CONTROL + 'a')
        base.wait_element(base.find_xpath_by_placeholder("买家留言模糊搜索")).send_keys(buyer_memo)
        base.wait_table_refresh(base.find_xpath("组合查询"), 1, "买家备注")
        buyer_memo_list = list(set(base.get_column_text("买家备注")))
        for j in buyer_memo_list:
            print(f"搜索结果：{j}")
            assert buyer_memo in j


# 卖家备注
def test_seller_memo_search_condition():
    base.wait_element_click(base.find_xpath_with_spaces("卖家备注"))
    base.wait_element_click(base.find_xpath("卖家备注", "无备注"))
    base.wait_table_refresh(base.find_xpath("组合查询"), 1, "卖家备注")
    result = list(set(base.get_column_text("卖家备注")))
    for i in result:
        assert i == ""
    base.wait_element_click(base.find_xpath("卖家备注", "有备注"))
    base.wait_table_refresh(base.find_xpath("组合查询"), 1, "卖家备注")
    result = list(set(base.get_column_text("卖家备注")))
    for i in result:
        assert i != ""
    for i in result:
        buyer_memo = i.strip("#")
        print(f"搜索卖家备注：{buyer_memo}")
        base.wait_element(base.find_xpath_by_placeholder("卖家备注模糊搜索")).send_keys(Keys.CONTROL + 'a')
        base.wait_element(base.find_xpath_by_placeholder("卖家备注模糊搜索")).send_keys(buyer_memo)
        base.wait_table_refresh(base.find_xpath("组合查询"), 1, "卖家备注")
        buyer_memo_list = list(set(base.get_column_text("卖家备注")))
        for j in buyer_memo_list:
            print(f"搜索结果：{j}")
            assert buyer_memo in j


# 便签搜索条件
def test_note_search_condition():
    base.wait_element_click(base.find_xpath_with_spaces("便签"))
    base.wait_element_click(base.find_xpath("便签", "无便签"))
    base.wait_table_refresh(base.find_xpath("组合查询"), 1, "便签")
    result = list(set(base.get_column_text("便签")))
    for i in result:
        assert i == ""
    base.wait_element_click(base.find_xpath("便签", "有便签"))
    base.wait_table_refresh(base.find_xpath("组合查询"), 1, "便签")
    result = list(set(base.get_column_string("便签")))
    for i in result:
        assert i != ""
    note_list = ["常用便签2", "爆款订单", "第一次第二次", "第二次"]
    for i in note_list:
        print(f"搜索原文本：{i}")
        base.wait_element(base.find_xpath_by_placeholder("便签模糊搜索")).send_keys(Keys.CONTROL + 'a')
        base.wait_element(base.find_xpath_by_placeholder("便签模糊搜索")).send_keys(i)
        base.wait_table_refresh(base.find_xpath("组合查询"), 1, "便签")
        buyer_memo_list = base.get_column_string("便签")
        for j in buyer_memo_list:
            print(f"结果：{j}")
            assert i in j


# 旗帜
def test_flag_search_condition():
    base.wait_element_click(base.find_xpath_with_spaces("旗帜"))
    base.wait_element_click(base.find_xpath_by_tag_name("旗帜", "input"))
    # ['【 无旗帜 】', '红色旗帜', '黄色旗帜', '绿色旗帜', '蓝色旗帜', '紫色旗帜', '排除红色旗帜', '排除黄色旗帜', '排除绿色旗帜', '排除蓝色旗帜', '排除紫色旗帜']
    flag_id = {"红色旗帜": "红旗", "黄色旗帜": "黄旗", "绿色旗帜": "绿旗", "蓝色旗帜": "蓝旗", "紫色旗帜": "紫旗", }
    flag_list = order.get_flag_list()
    print(flag_list)
    for i in flag_list:
        print(f"搜索的旗帜类型：{i}")
        base.wait_element_click(base.find_xpath_by_tag_name("旗帜", "input"))
        base.wait_element_click(base.find_xpath(i))
        base.wait_table_refresh(base.find_xpath("组合查询"), 1, "旗帜")
        order_sum_text = base.wait_element(base.find_xpath("已选择", "本页共")).text
        if order_sum_text == "本页共0条数据":
            print(f"没数据不用看")
        else:
            result = list(set(base.get_column_text("旗帜")))
            if "无旗帜" in i:
                for j in result:
                    print(f"旗帜搜索结果：{j}")
                    assert j == "无旗帜"
            elif "排除" in i:
                flag = i.replace("排除", "")
                for j in result:
                    print(f"旗帜搜索结果：{j}")
                    assert flag_id[flag] != j
            else:
                for j in result:
                    print(f"旗帜搜索结果：{j}")
                    assert j == flag_id[i]


# 会员名
def test_vip_name_search_condition():
    base.wait_element_click(base.find_xpath_with_spaces("收货人信息"))
    vip_name_list = base.get_column_text("会员名")
    for i in vip_name_list:
        vip_name_keyword = base.get_random_substring(i)
        base.wait_element(base.find_xpath_by_placeholder("会员名")).send_keys(Keys.CONTROL + 'a')
        base.wait_element(base.find_xpath_by_placeholder("会员名")).send_keys(vip_name_keyword)
        base.wait_table_refresh(base.find_xpath("组合查询"), 1, "会员名")
        result = base.get_column_text("会员名")
        for j in result:
            assert vip_name_keyword in j


# 收货人姓名
def test_receiver_name():
    base.wait_element_click(base.find_xpath_with_spaces("收货人信息"))
    receiver_name_list = base.get_column_text("收货人")
    for i in receiver_name_list:
        receiver_name_keyword = base.get_random_substring(i)
        base.wait_element(base.find_xpath_by_placeholder("收货人姓名")).send_keys(Keys.CONTROL + 'a')
        base.wait_element(base.find_xpath_by_placeholder("收货人姓名")).send_keys(receiver_name_keyword)
        base.wait_table_refresh(base.find_xpath("组合查询"), 1, "收货人")
        result = base.get_column_text("收货人")
        for j in result:
            assert receiver_name_keyword in j


# 创建时间测试
def test_time_search_condition():
    name = base.get_now_string()
    interface.new_vip(name)
    sku_info = [{'SkuCode': '测试商品1-红色 XS', 'Qty': '2'}, ]
    order_info = interface.new_order(name, sku_info)
    base.scroll_to(5)
    test.time_component_test("创建时间")
    base.wait_table_refresh(base.find_xpath("清空"), 1, "创建时间")
    base.wait_element_click(base.find_xpath("时间"))
    test.time_component_test("付款时间")
    # TODO:(RUI):  no good idea with delivery time


# 商品信息:商家编码/商品名称/规格名称/平台商家编码/平台规格名称/平台商品ID
def test_sku_info():
    base.wait_element_click(base.find_xpath_with_spaces("待审核（无备注）"))
    base.wait_element_click(base.find_xpath_with_spaces("待审核（有备注）"))
    base.wait_element_click(base.find_xpath_with_spaces("待审核（拆单）"))
    base.scroll_to_view(base.find_xpath("订单类型", "订单来源"))
    base.wait_element_click(base.find_xpath("订单类型", "订单来源"))
    base.wait_element_click(base.find_xpath("订单来源", "自动下载"))
    base.wait_element_click(base.find_xpath("收货人信息", "商品信息"))
    base.wait_table_refresh(base.find_xpath("组合查询"), 1, "订单编码")
    order_code_list = base.get_column_text("订单编码")
    print(f"获取一批商品信息")
    sku_code_list = []
    product_name_list = []
    sku_name_list = []
    platform_sku_code_list = []
    platform_sku_name_list = []
    platform_sku_id_list = []
    for i in order_code_list:
        order_code = i[i.index("T"):]
        order_id_list = interface.get_order_info_by_fuzzy(order_code, ["ID"])
        for j in order_id_list:
            sku_info_list = interface.get_order_product_detail(j["ID"],
                                                               ["商家编码", "商品名称", "规格名称", "平台商家编码", "平台规格名称", "平台商品ID"])
            for s in sku_info_list:
                for k, v in s.items():
                    if k == "商家编码":
                        sku_code_list.append(v)
                    elif k == "商品名称":
                        product_name_list.append(v)
                    elif k == "规格名称":
                        sku_name_list.append(v)
                    elif k == "平台商家编码":
                        platform_sku_code_list.append(v)
                    elif k == "平台规格名称":
                        platform_sku_name_list.append(v)
                    elif k == "平台商品ID":
                        platform_sku_id_list.append(v)
    sku_code_list = list(set(sku_code_list))
    product_name_list = list(set(product_name_list))
    sku_name_list = list(set(sku_name_list))
    platform_sku_code_list = list(set(platform_sku_code_list))
    platform_sku_name_list = list(set(platform_sku_name_list))
    platform_sku_id_list = list(set(platform_sku_id_list))
    print(f"解析出需要的信息列表")
    print(f"sku_code_list：{sku_code_list}")
    base.wait_table_refresh(base.find_xpath("清空"), 1, "订单编码")
    test.sku_info_search_condition_test(sku_code_list, "商家编码")
    print(f"product_name_list：{product_name_list}")
    base.wait_table_refresh(base.find_xpath("清空"), 1, "订单编码")
    test.sku_info_search_condition_test(product_name_list, "商品名称")
    print(f"sku_name_list：{sku_name_list}")
    base.wait_table_refresh(base.find_xpath("清空"), 1, "订单编码")
    test.sku_info_search_condition_test(sku_name_list, "规格名称")
    print(f"platform_sku_code_list：{platform_sku_code_list}")
    base.wait_table_refresh(base.find_xpath("清空"), 1, "订单编码")
    test.sku_info_search_condition_test(platform_sku_code_list, "平台商家编码")
    print(f"platform_sku_name_list：{platform_sku_name_list}")
    base.wait_table_refresh(base.find_xpath("清空"), 1, "订单编码")
    test.sku_info_search_condition_test(platform_sku_name_list, "平台规格名称")
    print(f"platform_sku_id_list：{platform_sku_id_list}")
    base.wait_table_refresh(base.find_xpath("清空"), 1, "订单编码")
    test.sku_info_search_condition_test(platform_sku_id_list, "平台商品ID")


# 商品数量
def test_sku_num_search_condition():
    base.wait_element_click(base.find_xpath("商品信息"))
    base.wait_element_click(base.find_xpath_by_placeholder("数量大于等于")).send_keys("2")
    base.wait_element_click(base.find_xpath_by_placeholder("数量小于")).send_keys("10")
    base.wait_table_refresh(base.find_xpath("组合查询"), 1, "订单编码")
    result = base.get_unique_column_text("商品数量")
    for i in result:
        assert 2 <= int(i) < 10
    base.wait_table_refresh(base.find_xpath("清空"), 1, "订单编码")
    base.wait_element_click(base.find_xpath_by_placeholder("金额大于等于")).send_keys("2")
    base.wait_element_click(base.find_xpath_by_placeholder("金额小于")).send_keys("10")
    base.scroll_to(5)
    base.wait_table_refresh(base.find_xpath("组合查询"), 1, "总金额")
    result = base.get_unique_column_text("总金额")
    for i in result:
        assert 2.00 <= float(i) < 10.00
    base.wait_table_refresh(base.find_xpath("清空"), 1, "总金额")
    base.wait_element_click(base.find_xpath_by_placeholder("种类数大于等于")).send_keys("6")
    base.wait_element_click(base.find_xpath_by_placeholder("种类数小于")).send_keys("7")
    base.scroll_to(0)
    base.wait_table_refresh(base.find_xpath("组合查询"), 1, "订单编码")
    elements = base.wait_elements(base.get_column_xpath("商品信息"))
    for i in elements:
        i.click()
        sku_code_list = order.get_all_float_sku_info("商家编码")
        assert 6 <= len(sku_code_list) < 7


# 供应商/排除供应商搜索条件
def test_supplier_search_condition():
    base.wait_element_click(base.find_xpath("订单状态", "待审核（无备注）"))
    base.wait_element_click(base.find_xpath("商品信息"))
    supplier_name_list = [
        "供应商1",
        "供应商2",
        "供应商3",
        "供应商4",
        "供应商5",
    ]
    print(f"订单的所有明细供应商必须是指定供应商才符合供应商搜索条件")
    for i in supplier_name_list:
        time.sleep(1)
        base.wait_element_click(base.find_xpath_by_placeholder("供应商"))
        base.change_frame("选择供应商")
        base.chose_supplier_by_text(i)
        base.change_frame()
        base.wait_element_click(base.find_xpath("选择供应商", "确认"))
        base.change_frame("全部订单框架")
        element = base.wait_element(base.find_xpath("本页共", "加载"))
        text = element.text
        base.wait_element_click(base.find_xpath("组合查询"))
        base.wait_element_refresh(element, text)
        order_sum_text = base.wait_element(base.find_xpath("已选择", "本页共")).text
        if order_sum_text == "本页共0条数据":
            print(f"没数据不用看")
        else:
            order_code_list = base.get_column_text("订单编码")
            supplier_id = supplier_interface.get_supplier_info(i, ["供应商ID"])["供应商ID"]
            print(f"指定供应商: {i}的供应商id是: {supplier_id}")
            for order_code in order_code_list:
                print(f"order_code:{order_code}")
                order_id = interface.get_order_info_by_fuzzy(order_code, ["ID"])[0]["ID"]
                print(f"order_id:{order_id}")
                sku_code_result = order_interface.get_order_product_detail(order_id, ["商家编码"])
                for s in sku_code_result:
                    expect_supplier_id = product_interface.get_sku_info(s["商家编码"])["data"]["Items"][0]["SupplierId"]
                    print(f"订单商品的ID是{expect_supplier_id}")
                    assert expect_supplier_id == supplier_id
    print(f"再试下指定多个供应商：供应商1-5")
    supplier_id_list = []
    for i in supplier_name_list:
        supplier_id = supplier_interface.get_supplier_info(i, ["供应商ID"])["供应商ID"]
        supplier_id_list.append(supplier_id)
    print(f"供应商文本是")
    print(f"供应商id集合是{supplier_id_list}")
    print("指定多个供应商时，订单明细的供应商只要是指定供应商其中之一即可")
    time.sleep(1)
    base.wait_element_click(base.find_xpath_by_placeholder("供应商"))
    base.change_frame("选择供应商")
    base.chose_supplier_by_text(supplier_name_list)
    base.change_frame()
    base.wait_element_click(base.find_xpath("选择供应商", "确认"))
    base.change_frame("全部订单框架")
    element = base.wait_element(base.find_xpath("本页共", "加载"))
    text = element.text
    base.wait_element_click(base.find_xpath("组合查询"))
    base.wait_element_refresh(element, text)
    order_sum_text = base.wait_element(base.find_xpath("已选择", "本页共")).text
    if order_sum_text == "本页共0条数据":
        print(f"没数据不用看")
    else:
        order_code_list = base.get_column_text("订单编码")
        for order_code in order_code_list:
            # print(f"order_code:{order_code}")
            order_id = interface.get_order_info_by_fuzzy(order_code, ["ID"])[0]["ID"]
            # print(f"order_id:{order_id}")
            sku_code_result = order_interface.get_order_product_detail(order_id, ["商家编码"])
            for s in sku_code_result:
                expect_supplier_id = product_interface.get_sku_info(s["商家编码"])["data"]["Items"][0]["SupplierId"]
                print(f"订单商品的ID是{expect_supplier_id}")
                assert expect_supplier_id in supplier_id_list
    print(f"测试排除供应商，订单的所有商品必须全部不是指定供应商才符合条件")
    element = base.wait_element(base.find_xpath("本页共", "加载"))
    text = element.text
    base.wait_element_click(base.find_xpath("清空"))
    base.wait_element_refresh(element, text)
    base.wait_element_click(base.find_xpath("订单状态", "待审核（无备注）"))
    for i in supplier_name_list:
        print(f"供应商点快了没有用")
        time.sleep(1)
        base.wait_element_click(base.find_xpath_by_placeholder("排除供应商"))
        base.change_frame("选择供应商")
        base.chose_supplier_by_text(i)
        base.change_frame()
        base.wait_element_click(base.find_xpath("选择供应商", "确认"))
        base.change_frame("全部订单框架")
        element = base.wait_element(base.find_xpath("本页共", "加载"))
        text = element.text
        base.wait_element_click(base.find_xpath("组合查询"))
        base.wait_element_refresh(element, text)
        order_sum_text = base.wait_element(base.find_xpath("已选择", "本页共")).text
        if order_sum_text == "本页共0条数据":
            print(f"没数据不用看")
        else:
            order_code_list = base.get_column_text("订单编码")
            supplier_id = supplier_interface.get_supplier_info(i, ["供应商ID"])["供应商ID"]
            print(f"指定供应商: {i}的供应商id是: {supplier_id}")
            for order_code in order_code_list:
                # print(f"order_code:{order_code}")
                order_id = interface.get_order_info_by_fuzzy(order_code, ["ID"])[0]["ID"]
                # print(f"order_id:{order_id}")
                sku_code_result = order_interface.get_order_product_detail(order_id, ["商家编码"])
                for s in sku_code_result:
                    expect_supplier_id = product_interface.get_sku_info(s["商家编码"])["data"]["Items"][0]["SupplierId"]
                    print(f"订单商品的ID是{expect_supplier_id}")
                    assert expect_supplier_id != supplier_id
    print(f"供应商id集合是{supplier_id_list}")
    print("指定排除多个供应商时，订单明细的供应商不能是指定供应商其中之一")
    time.sleep(1)
    base.wait_element_click(base.find_xpath_by_placeholder("排除供应商"))
    base.change_frame("选择供应商")
    base.chose_supplier_by_text(supplier_name_list)
    base.change_frame()
    base.wait_element_click(base.find_xpath("选择供应商", "确认"))
    base.change_frame("全部订单框架")
    element = base.wait_element(base.find_xpath("本页共", "加载"))
    text = element.text
    base.wait_element_click(base.find_xpath("组合查询"))
    base.wait_element_refresh(element, text)
    order_sum_text = base.wait_element(base.find_xpath("已选择", "本页共")).text
    if order_sum_text == "本页共0条数据":
        print(f"没数据不用看")
    else:
        order_code_list = base.get_column_text("订单编码")
        for order_code in order_code_list:
            # print(f"order_code:{order_code}")
            order_id = interface.get_order_info_by_fuzzy(order_code, ["ID"])[0]["ID"]
            # print(f"order_id:{order_id}")
            sku_code_result = order_interface.get_order_product_detail(order_id, ["商家编码"])
            for s in sku_code_result:
                expect_supplier_id = product_interface.get_sku_info(s["商家编码"])["data"]["Items"][0]["SupplierId"]
                assert expect_supplier_id not in supplier_id_list


# 缺货类型
def test_shortage_status_search_condition():
    base.scroll_to(4)
    base.wait_element_click(base.find_xpath("缺货状态"))
    base.wait_element_click(base.find_xpath("缺货状态", "库存充足"))
    base.wait_table_refresh(base.find_xpath("组合查询"), 1, "缺货")
    result = base.get_column_text("缺货")
    for i in result:
        assert "库存充足" in i
    base.wait_element_click(base.find_xpath("缺货状态", "部分缺货"))
    base.wait_table_refresh(base.find_xpath("组合查询"), 1, "缺货")
    result = base.get_column_text("缺货")
    for i in result:
        assert "部分缺货" in i
    base.wait_element_click(base.find_xpath("缺货状态", "全部缺货"))
    base.wait_table_refresh(base.find_xpath("组合查询"), 1, "缺货")
    result = base.get_column_text("缺货")
    for i in result:
        assert "全部缺货" in i
    print(f"有缺货搜索出来的订单可以是全缺或者部分缺")
    base.wait_element_click(base.find_xpath("缺货状态", "有缺货"))
    base.wait_table_refresh(base.find_xpath("组合查询"), 1, "缺货")
    result = base.get_column_text("缺货")
    for i in result:
        assert "缺货" in i


# 店铺搜索条件
def test_shop_search_condition():
    base.wait_element_click(order.locations["店铺下拉按钮"])
    base.wait_element_click(base.find_xpath("巨淘气"))
    base.wait_table_refresh(base.find_xpath("组合查询"), 1, "订单编码")
    result = base.get_column_text("店铺")
    for i in result:
        assert "巨淘气" == i
    base.wait_element_click(base.find_xpath("阿里测试店铺01"))
    base.wait_table_refresh(base.find_xpath("组合查询"), 1, "订单编码")
    result = base.get_column_text("店铺")
    for i in result:
        assert "阿里测试店铺01" == i or "巨淘气" == i


# 仓库搜索条件
def test_warehouse_search_condition():
    base.wait_element_click(order.locations["仓库下拉按钮"])
    base.wait_element_click(base.find_xpath("主仓库"))
    base.wait_table_refresh(base.find_xpath("组合查询"), 1, "订单编码")
    result = base.get_column_text("仓库")
    for i in result:
        assert "主仓库" == i
    base.wait_element_click(base.find_xpath("测试仓"))
    base.wait_table_refresh(base.find_xpath("组合查询"), 1, "订单编码")
    result = base.get_column_text("仓库")
    for i in result:
        assert "主仓库" == i or "测试仓" == i


# 快递搜索条件
def test_express_search_condition():
    base.wait_element_click(order.locations["快递下拉按钮"])
    base.wait_element_click(base.find_xpath("EMS"))
    base.wait_table_refresh(base.find_xpath("组合查询"), 1, "订单编码")
    result = base.get_column_text("快递")
    for i in result:
        assert "EMS" == i
    base.wait_element_click(base.find_xpath("邮政小包电子面单"))
    base.wait_table_refresh(base.find_xpath("组合查询"), 1, "订单编码")
    result = base.get_column_text("快递")
    for i in result:
        assert "EMS" == i or "邮政小包电子面单" == i


# 订单类型
def test_order_type_search_condition():
    order_type_list = ["销售订单", "换货订单", "补发订单", "POS订单", "已发货订单", "冲红订单", "被冲红订单", "预售订单", "订阅订单", ]
    base.wait_element_click(base.find_xpath("订单类型"))
    base.scroll_to(5)
    for i in order_type_list:
        print(f"本次搜索的订单类型是:{i}")
        base.wait_element_click(base.find_xpath("订单类型", i))
        element = base.wait_element(base.find_xpath("本页共", "加载"))
        text = element.text
        base.wait_element_click(base.find_xpath("组合查询"))
        base.wait_element_refresh(element, text)
        order_num_text = base.wait_element_click(base.find_xpath("已选择", "本页共")).text
        if order_num_text == "本页共0条数据":
            print("没有数据不用看")
        else:
            result = base.get_column_text("订单类型")
            print(f"订单类型{i}的搜索结果是：")
            for j in result:
                print(f"{j}")
                assert j == i


# 订单来源
def test_order_source_search_condition():
    order_source_type_list = ["自动下载", "手工下载", "手工新增", "导入", "单据生成"]
    base.wait_element_click(base.find_xpath("订单来源"))
    for i in order_source_type_list:
        print(f"本次搜索的订单来源类型是：{i}")
        base.wait_element_click(base.find_xpath("订单来源", i))
        element = base.wait_element(base.find_xpath("本页共", "加载"))
        text = element.text
        base.wait_element_click(base.find_xpath("组合查询"))
        base.wait_element_refresh(element, text)
        order_num_text = base.wait_element_click(base.find_xpath("已选择", "本页共")).text
        if order_num_text == "本页共0条数据":
            print("没有数据不用看")
        else:
            order_code_list = base.get_column_text("订单编码")
            for order_code in order_code_list:
                base.wait_element(base.get_cell_xpath(order_code, "订单编码"))
                time.sleep(1)
                base.wait_element_click(base.get_cell_xpath(order_code, "订单编码"))
                base.wait_element_click(base.get_cell_xpath(order_code, "订单编码", "详"))
                base.change_frame("全部订单框架", "订单详情")
                order_detail_order_source_type = base.wait_element(base.find_xpath_by_tag_name("订单来源:", "div")).text
                assert order_detail_order_source_type == i
                base.change_frame("全部订单框架")
                base.wait_element_click(base.find_xpath_by_tag_name("订单详情", "a"))


# 省份搜索条件
def test_province_search_condition():
    base.wait_element_click(order.locations["省份下拉按钮"])
    province_list = order.get_province_list()
    for i in province_list:
        print(f"本次搜索的省份是：{i}")
        base.wait_element_click(base.find_xpath("省份", i))
        element = base.wait_element(base.find_xpath("本页共", "加载"))
        text = element.text
        base.wait_element_click(base.find_xpath("组合查询"))
        base.wait_element_refresh(element, text)
        order_num_text = base.wait_element_click(base.find_xpath("已选择", "本页共")).text
        if order_num_text == "本页共0条数据":
            print("没有数据不用看")
        else:
            result = base.get_column_text("省")
            for j in result:
                print(f"本次搜索出的省份是:{j}")
                assert j == i
        base.wait_element_click(base.find_xpath("省份", i))


# 订单状态
def test_order_status_search_condition():
    order_status_list = ["待发货", "已发货", "交易成功", "交易关闭", "已锁定", "异常", "有退款"]
    base.wait_element_click(base.find_xpath("其他"))
    base.wait_element_click(base.find_xpath_by_tag_name("其他", "select"))
    for i in order_status_list:
        base.wait_element_click(base.find_xpath("请选择交易状态", i))
        print(f"本次搜索的订单状态是：{i}")
        element = base.wait_element(base.find_xpath("本页共", "加载"))
        text = element.text
        base.wait_element_click(base.find_xpath("组合查询"))
        base.wait_element_refresh(element, text)
        order_num_text = base.wait_element_click(base.find_xpath("已选择", "本页共")).text
        if order_num_text == "本页共0条数据":
            print("没有数据不用看")
        else:
            sku_info_elements = base.wait_elements(base.get_column_xpath("商品信息"))
            for j in sku_info_elements:
                j.click()
                sku_other_info = order.get_all_float_sku_info("其他信息")
                print(f"订单状态信息是：{sku_other_info}")
                has_one_sku_contains_order_status = False
                if "交易成功" == i:
                    for k in sku_other_info:
                        if "交易完成" in k:
                            has_one_sku_contains_order_status = True
                            break
                else:
                    for k in sku_other_info:
                        if i in k:
                            has_one_sku_contains_order_status = True
                            break
                assert has_one_sku_contains_order_status


# 运费范围
def test_freight_search_condition():
    base.wait_element_click(base.find_xpath("其他"))
    base.wait_element_click(base.find_xpath_by_placeholder("运费大于等于")).send_keys(2)
    base.wait_element_click(base.find_xpath_by_placeholder("运费小于")).send_keys(10)
    element = base.wait_element(base.find_xpath("本页共", "加载"))
    text = element.text
    base.wait_element_click(base.find_xpath("组合查询"))
    base.wait_element_refresh(element, text)
    order_num_text = base.wait_element_click(base.find_xpath("已选择", "本页共")).text
    if order_num_text == "本页共0条数据":
        print("没有数据不用看")
    else:
        order_code_list = base.get_column_text("订单编码")
        for i in order_code_list:
            base.wait_element(base.get_cell_xpath(i, "订单编码"))
            time.sleep(1)
            base.wait_element_click(base.get_cell_xpath(i, "订单编码"))
            base.wait_element_click(base.get_cell_xpath(i, "订单编码", "详"))
            base.change_frame("全部订单框架", "订单详情")
            post_fee = base.wait_element(base.find_xpath_by_tag_name("运费:", "input")).get_attribute("value")
            assert 2.00 <= float(post_fee) < 10.00
            base.change_frame("全部订单框架")
            base.wait_element_click(base.find_xpath_by_tag_name("订单详情", "a"))


# 付款时间
def test_pay_time_search_condition():
    base.wait_element_click(base.find_xpath("其他"))
    base.wait_element_click(base.find_xpath_by_placeholder("付款天数大于等于")).send_keys(3)
    base.wait_element_click(base.find_xpath_by_placeholder("付款天数小于")).send_keys(10)
    base.scroll_to(5)
    element = base.wait_element(base.find_xpath("本页共", "加载"))
    text = element.text
    base.wait_element_click(base.find_xpath("组合查询"))
    base.wait_element_refresh(element, text)
    order_num_text = base.wait_element_click(base.find_xpath("已选择", "本页共")).text
    if order_num_text == "本页共0条数据":
        print("没有数据不用看")
    else:
        result = base.get_column_text("付款时间")
        for i in result:
            # i = i.replace("\n", " ")
            i = i[0:i.index("\n")]
            # pay_time = datetime.strptime(i, "%Y-%m-%d %H:%M:%S")
            pay_time = datetime.strptime(i, "%Y-%m-%d")
            print(f"付款时间是{pay_time}")
            # days = (datetime.now()-pay_time).total_seconds()/(60*60)
            days = (datetime.now() - pay_time).days
            print(f"订单的间隔天数：{int(days)}")
            assert 3 <= int(days) < 10


# 相同会员不同地址
def test_same_vip_with_different_address():
    base.wait_element_click(base.find_xpath("其他"))
    base.wait_element_click(base.find_xpath("相同会员不同收货地址", "是"))
    element = base.wait_element(base.find_xpath("本页共", "加载"))
    text = element.text
    base.wait_element_click(base.find_xpath("组合查询"))
    base.wait_element_refresh(element, text)
    order_num_text = base.wait_element_click(base.find_xpath("已选择", "本页共")).text
    if order_num_text == "本页共0条数据":
        print("没有数据不用看")
    else:
        print(f"搜索出来的会员名必然存在多个不同的收货地址")
        vip_name_list = list(set(base.get_column_text("会员名")))
        base.scroll_to(5)
        for i in vip_name_list:
            print(f"本次搜索的会员是：{i}")
            base.fuzzy_search("收货地址", i)
            address_list = list(set(base.get_column_text("收货地址")))
            print(f"搜索出来的地址是{address_list}")
            assert len(address_list) >= 2
    base.scroll_to(0)
    print(f"勾选否的设置下，同会员，地址必然相同")
    base.wait_table_refresh(base.find_xpath("清空"), 1, "会员名")
    base.wait_element_click(base.find_xpath("相同会员不同收货地址", "否"))
    element = base.wait_element(base.find_xpath("本页共", "加载"))
    text = element.text
    base.wait_element_click(base.find_xpath("组合查询"))
    base.wait_element_refresh(element, text)
    order_num_text = base.wait_element_click(base.find_xpath("已选择", "本页共")).text
    if order_num_text == "本页共0条数据":
        print("没有数据不用看")
    else:
        print(f"搜索出来的会员名必然存在只有一个收货地址")
        vip_name_list = list(set(base.get_column_text("会员名")))
        base.scroll_to(5)
        for i in vip_name_list:
            print(f"本次搜索的会员是：{i}")
            base.fuzzy_search("收货地址", i)
            address_list = list(set(base.get_column_text("收货地址")))
            print(f"搜索出来的地址是{address_list}")
            assert len(address_list) == 1


# 相同手机号不同收货地址
def test_same_phone_number_with_different_address():
    base.wait_element_click(base.find_xpath("其他"))
    base.wait_element_click(base.find_xpath("相同手机号不同收货地址", "是"))
    element = base.wait_element(base.find_xpath("本页共", "加载"))
    text = element.text
    base.wait_element_click(base.find_xpath("组合查询"))
    base.wait_element_refresh(element, text)
    order_num_text = base.wait_element_click(base.find_xpath("已选择", "本页共")).text
    if order_num_text == "本页共0条数据":
        print("没有数据不用看")
    else:
        print(f"搜索出来的手机号必然存在多个不同的收货地址")
        base.scroll_to(5)
        phone_num_list = list(set(base.get_column_text("手机号")))
        for i in phone_num_list:
            print(f"本次搜索的手机号是：{i}")
            if i == '15221071395':
                continue
            base.fuzzy_search("收货地址", i)
            address_list = list(set(base.get_column_text("收货地址")))
            print(f"搜索出来的地址是{address_list}")
            assert len(address_list) >= 2
    print(f"勾选否的设置下，同手机号，地址必然相同")
    base.wait_table_refresh(base.find_xpath("清空"), 1, "手机号")
    base.wait_element_click(base.find_xpath("相同手机号不同收货地址", "否"))
    element = base.wait_element(base.find_xpath("本页共", "加载"))
    text = element.text
    base.wait_element_click(base.find_xpath("组合查询"))
    base.wait_element_refresh(element, text)
    order_num_text = base.wait_element_click(base.find_xpath("已选择", "本页共")).text
    if order_num_text == "本页共0条数据":
        print("没有数据不用看")
    else:
        print(f"手机号")
        vip_name_list = list(set(base.get_column_text("手机号")))
        for i in vip_name_list:
            print(f"本次搜索的手机号是：{i}")
            if i == '':
                continue
            base.fuzzy_search("收货地址", i)
            address_list = list(set(base.get_column_text("收货地址")))
            print(f"搜索出来的地址是{address_list}")
            assert len(address_list) == 1


if __name__ == '__main__':
    pytest.main()
