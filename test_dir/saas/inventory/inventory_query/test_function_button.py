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


def setup_function():
    base.open_page("库存", "库存查询", "库存查询框架")
    element = ''
    try:
        element = base.wait_element(base.find_xpath("刷新报表缓存", "天数"), 3)
    except AssertionError as ae:
        print(ae)
    if element != '':
        time.sleep(1)
        base.wait_element_click(base.find_xpath("刷新报表缓存", "确定"))


def teardown_function():
    base.close_page("库存查询")


def teardown_module():
    base.browser_close()


def test_export_button():
    """
    点击下即可
    """
    base.wait_element_click(base.find_xpath("导出"))


# 盘点选中库位
def test_check_inventory():
    base.wait_element(base.find_xpath("显示0库存", "是"))
    time.sleep(1)
    base.wait_element_click(base.find_xpath("显示0库存", "是"))
    base.wait_table_refresh(base.find_xpath("组合查询"), 1, "货号")
    sku_code = base.wait_element(base.get_cell_xpath(1, "商家编码")).text
    base.wait_element_click(base.get_cell_xpath(1, "商家编码"))
    base.click_space()
    base.wait_element_click(base.find_xpath("盘点选中商品库存"))
    base.change_frame("库存查询框架", "新增盘点单")
    base.wait_element(base.get_old_cell_input_xpath(1, "实际数量")).send_keys(Keys.CONTROL+'a')
    base.wait_element(base.get_old_cell_input_xpath(1, "实际数量")).send_keys(100)
    base.change_frame("库存查询框架")
    base.wait_element_click(base.find_xpath("新增盘点单", "提交并盘点"))
    base.wait_element(base.find_xpath("显示0库存", "全部"))
    time.sleep(1)
    base.wait_element_click(base.find_xpath("显示0库存", "全部"))
    base.wait_element(base.find_xpath_by_placeholder("商家编码")).send_keys(Keys.CONTROL+'a')
    base.wait_element(base.find_xpath_by_placeholder("商家编码")).send_keys(sku_code)
    base.wait_table_refresh(base.find_xpath("组合查询"), 1, "货号")
    inventory = base.wait_element(base.get_cell_xpath(sku_code, ["库存预警值", "库存数"])).text
    assert inventory == '100'


# 批量修改固定库位
def test_multi_modify_bin():
    bin_name = setting_interface.get_random_bin("主仓库")["库位"]
    print(bin_name)
    base.wait_element_click(base.find_xpath("显示0库存", "是"))
    base.wait_table_refresh(base.find_xpath("组合查询"), 1, "货号")
    sku_code = base.wait_element(base.get_cell_xpath(1, "商家编码")).text
    base.wait_element_click(base.get_cell_xpath(1, "商家编码"))
    base.click_space()
    element = base.wait_element(base.get_cell_xpath(1, "固定库位"))
    text = element.text
    base.wait_element_click(base.find_xpath("批量修改固定库位"))
    base.wait_element(base.find_xpath_by_placeholder("请输入完整库位编码")).send_keys(Keys.CONTROL + 'a')
    base.wait_element(base.find_xpath_by_placeholder("请输入完整库位编码")).send_keys(bin_name)
    base.wait_element_click(base.find_xpath("空值不修改", "确认"))
    base.wait_element_refresh(element, text)
    result = base.wait_element(base.get_cell_xpath(sku_code, "固定库位")).text
    bin_name_list = list(bin_name)
    bin_name_list.pop(bin_name.index("-"))
    result_bin_name = '' .join(bin_name_list)
    print(result_bin_name)
    assert result_bin_name in result


# 修改固定库位
def test_modify_bin():
    bin_name = setting_interface.get_random_bin("主仓库")["库位"]
    print(bin_name)
    time.sleep(1)
    base.wait_element_click(base.find_xpath("显示0库存", "是"))
    base.wait_table_refresh(base.find_xpath("组合查询"), 1, "货号")
    sku_code = base.wait_element(base.get_cell_xpath(1, "商家编码")).text
    element = base.wait_element(base.get_cell_xpath(1, "固定库位"))
    text = element.text
    base.wait_element_click(base.get_cell_xpath(sku_code, "固定库位"))
    base.wait_element_click(base.get_cell_xpath(sku_code, "固定库位", "改"))
    base.wait_element(base.find_xpath_by_placeholder("请输入完整库位编码")).send_keys(Keys.CONTROL+'a')
    base.wait_element(base.find_xpath_by_placeholder("请输入完整库位编码")).send_keys(bin_name)
    base.wait_element_click(base.find_xpath("空值不修改", "确认"))
    base.wait_element_refresh(element, text)
    time.sleep(1)
    result = base.wait_element(base.get_cell_xpath(sku_code, "固定库位")).text
    bin_name_list = list(bin_name)
    bin_name_list.pop(bin_name.index("-"))
    result_bin_name = ''.join(bin_name_list)
    print(result_bin_name)
    assert result_bin_name in result


# 库存预警值
def test_warning_inventory():
    base.wait_element(base.find_xpath("显示0库存", "是"))
    time.sleep(1)
    base.wait_element_click(base.find_xpath("显示0库存", "是"))
    base.wait_table_refresh(base.find_xpath("组合查询"), 1, "货号")
    sku_code = base.wait_element(base.get_cell_xpath(1, "商家编码")).text
    base.wait_element_click(base.get_cell_xpath(1, "商家编码"))
    base.click_space()
    base.wait_element_click(base.find_xpath("盘点选中商品库存"))
    base.change_frame("库存查询框架", "新增盘点单")
    base.wait_element(base.get_old_cell_input_xpath(1, "实际数量")).send_keys(Keys.CONTROL + 'a')
    base.wait_element(base.get_old_cell_input_xpath(1, "实际数量")).send_keys(100)
    base.change_frame("库存查询框架")
    base.wait_element_click(base.find_xpath("新增盘点单", "提交并盘点"))
    base.wait_element(base.find_xpath("显示0库存", "全部"))
    time.sleep(1)
    base.wait_element_click(base.find_xpath("显示0库存", "全部"))
    base.wait_element(base.find_xpath_by_placeholder("商家编码")).send_keys(Keys.CONTROL + 'a')
    base.wait_element(base.find_xpath_by_placeholder("商家编码")).send_keys(sku_code)
    base.wait_table_refresh(base.find_xpath("组合查询"), 1, "货号")
    base.wait_element_click(base.get_cell_xpath(sku_code, "库存预警值")).send_keys(200)
    base.wait_element_click(base.find_xpath("库存告警", "是"))
    time.sleep(1)
    base.wait_table_refresh(base.find_xpath("组合查询"), 1, "货号")
    result_num = base.wait_element(base.find_xpath("已选择", "本页共")).text
    assert result_num == "本页共1条数据"
    base.wait_element_click(base.find_xpath("库存告警", "否"))
    base.wait_table_refresh(base.find_xpath("组合查询"), 1, "货号")
    result_num = base.wait_element(base.find_xpath("已选择", "本页共")).text
    assert result_num == "本页共0条数据"


def test_detail_button():
    """
    能显示字段即可，不管功能
    """
    sku_code = "测试商品1-红色 XS"
    base.scroll_to(4)
    time.sleep(1)
    base.wait_element(base.find_xpath_by_placeholder("商家编码")).send_keys(Keys.CONTROL+'a')
    base.wait_element(base.find_xpath_by_placeholder("商家编码")).send_keys(sku_code)
    base.wait_table_refresh(base.find_xpath("组合查询"), 1, "余额")
    base.wait_element_click(base.get_cell_xpath(1, ["库存预警值", "库存数"]))
    base.wait_element_click(base.get_cell_xpath(1, ["库存预警值", "库存数"], "详"))
    base.change_frame("库存查询框架", "出入库记录页面")
    base.wait_element(base.find_xpath("调整金额"))
    base.change_frame("库存查询框架")
    time.sleep(1)
    base.wait_element_click(base.find_xpath_by_tag_name("出入库记录页面", "a"))
    base.wait_element_click(base.get_cell_xpath(1, ["余额", "占用数"]))
    base.wait_element_click(base.get_cell_xpath(1, ["余额", "占用数"], "详"))
    base.change_frame("库存查询框架", "占用记录页面")
    base.wait_element(base.find_xpath("订单单号"))
    base.change_frame("库存查询框架")
    time.sleep(1)
    base.wait_element_click(base.find_xpath_by_tag_name("占用记录页面", "a"))
    base.wait_element_click(base.get_cell_xpath(1, "采购在途数"))
    base.wait_element_click(base.get_cell_xpath(1, "采购在途数", "详"))
    base.change_frame("库存查询框架", "在途采购单明细页面")
    base.wait_element(base.find_xpath("采购单编码"))
    base.change_frame("库存查询框架")
    time.sleep(1)
    base.wait_element_click(base.find_xpath_by_tag_name("在途采购单明细页面", "a"))
    base.wait_element_click(base.get_cell_xpath(1, "操作", "销售链接"))
    base.change_frame("库存查询框架", "销售链接明细")
    base.wait_element(base.find_xpath("店铺"))
    base.change_frame("库存查询框架")
    time.sleep(1)
    base.wait_element_click(base.find_xpath_by_tag_name("销售链接明细", "a"))
    base.wait_element_click(base.get_cell_xpath(1, "操作", "销售订单"))
    base.change_frame("库存查询框架", "销售订单明细")
    base.wait_element(base.find_xpath("平台单号"))


if __name__ == '__main__':
    pytest.main()