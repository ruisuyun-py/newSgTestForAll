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
        "记录会员上次交易价：手工单或者门店单保存时，记录会员的商品交易价格": "false",
        "记录会员上次交易价 同款同价：手工单或者门店单保存时，记录会员的商品交易价格 同款同价": "false",
        "只有手工修改售价才会记录预设价格": "true",
    }
    interface.save_order_setting(setting_info)
    # 新建会员
    vip_name = base.get_now_string()
    vip_info = interface.new_vip(vip_name)
    # 查询确认新会员没有任何记录
    base.wait_element(base.find_xpath_by_placeholder("会员")).click()
    base.change_frame("预设会员价明细框架")
    base.switch_to_frame(base.find_frame("选择会员"))
    base.chose_vip(vip_name)
    base.change_frame("预设会员价明细框架")
    base.wait_element(base.find_xpath("本页共0条数据"))
    # 新建商品
    product_code = base.get_now_string()
    print(product_code)
    sku_info = interface.new_product(product_code)
    try:
        base.open_page("订单", "门店收银", "门店收银框架")
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
    finally:
        base.close_page("门店收银")
    # 设置商品的标准售价，第二价格，第三价格，第四价格
    interface.modify_sku_price(sku_info[0], "100", "200", "300", "400")


def test_001():
    setting_info = {
        "记录会员上次交易价：手工单或者门店单保存时，记录会员的商品交易价格": "false",
        "记录会员上次交易价 同款同价：手工单或者门店单保存时，记录会员的商品交易价格 同款同价": "false",
        "只有手工修改售价才会记录预设价格": "true",
    }
    interface.save_order_setting(setting_info)


if __name__ == '__main__':
    pytest.main()
