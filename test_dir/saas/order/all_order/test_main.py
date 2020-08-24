import random
import sys
import time
import pytest
from os.path import dirname, abspath
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import test_dir.test_base as test
import page.login_page as login
import page.base_page as base
import page.order.all_order_page as order
import page.interface as interface

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
    with open('file_for_multi_search/vip_list.txt', 'r', encoding='UTF-8') as f:
        vip_list = f.readlines()
    f.close()
    with open('file_for_multi_search/not_found_vip_list.txt', 'r', encoding='UTF-8') as f:
        not_found_vip_list = f.readlines()
    f.close()
    base.wait_element(order.locations["批量搜索下拉按钮"]).click()
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
    with open('file_for_multi_search/express_code.txt', 'r', encoding='UTF-8') as f:
        express_code_list = f.readlines()
    f.close()
    with open('file_for_multi_search/not_found_express_code_list.txt', 'r', encoding='UTF-8') as f:
        not_found_express_code_list = f.readlines()
    f.close()
    base.wait_element(order.locations["批量搜索下拉按钮"]).click()
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
    base.wait_element(base.find_xpath("信息", "确定")).click()
    base.driver.switch_to.default_content()
    base.switch_to_frame(base.locations["全部订单框架"])
    vip_result = base.get_column_text("会员名")
    # 全部订单页面没有物流单号字段只能使用会员名称替代下
    with open('file_for_multi_search/express_code_vip_name_result.txt', 'r', encoding='UTF-8') as f:
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
    with open('file_for_multi_search/platform_order_code.txt', 'r', encoding='UTF-8') as f:
        platform_order_code_list = f.readlines()
    f.close()
    with open('file_for_multi_search/not_found_platform_order_code.txt', 'r', encoding='UTF-8') as f:
        not_found_platform_order_code_list = f.readlines()
    f.close()
    base.wait_element(order.locations["批量搜索下拉按钮"]).click()
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
    with open('file_for_multi_search/address_list.txt', 'r', encoding='UTF-8') as f:
        address_list = f.readlines()
    f.close()
    print(address_list)
    with open('file_for_multi_search/not_found_address_list.txt', 'r', encoding='UTF-8') as f:
        not_found_address_list = f.readlines()
    f.close()
    print(not_found_address_list)
    base.wait_element(order.locations["批量搜索下拉按钮"]).click()
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
        test.test_fuzzy_search(i)
    result = interface.get_delivery_order_column_value("物流单号", "会员名称")
    for i in range(0, 10):
        k = random.choice(list(result.keys()))
        print(f"物流单号:{k}")
        print(f"会员名：{result[k]}")
        base.fuzzy_search("会员名", k)
        vip_name = base.get_column_text("会员名")[0]
        print(f"会员名：{vip_name}")
        assert vip_name == result[k]


# 待审核（无备注）
def test_wait_to_approve_with_out_memo():
    print("验证待审核无备注订单的状态均为待审核，且买家备注和卖家备注均为空或者以#结尾")
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
            assert "待审核" == i
        print("验证订单数必须大于2且必须至少有一个待合并订单状态异常")
        for i in range(1, len(result) + 1):
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


if __name__ == '__main__':
    pytest.main()
