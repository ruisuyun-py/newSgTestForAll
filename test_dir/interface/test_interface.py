import sys
import time
from os.path import dirname, abspath
import page.base_page as base
import interface.interface as interface
import interface.order.delivery_order_interface as delivery_interface
import interface.product.product_interface as product_interface
import interface.supplier.supplier_interface as supplier_interface
import interface.vip.vip_interface as vip_interface
import interface.inventory.inventory_interface as inventory_interface
import interface.purchase.purchase_interface as purchase_interface
import interface.finance.finance_interface as finance_interface
import interface.order.order_interface as order_interface
import interface.pda.pda_interface as pda_interface
import interface.setting.setting_interface as setting_interface
import pytest
import requests

sys.path.insert(0, dirname(dirname(dirname(abspath(__file__)))))


def setup_module():
    base.cookies = interface.get_cookie()
    pda_interface.cookies = pda_interface.login()


def setup_function():
    pass


def teardown_function():
    pass


def teardown_module():
    pass


def test_login_for_module():
    url = "http://gw.erp12345.com/api/Orders/AllOrder/QueryPage?ModelTypeName=ErpWeb.Domain.ViewModels.Orders" \
          ".AllOrderVmv&page=1&pagesize=20 "
    headers = {
        'Cookie': base.cookies
    }
    response = requests.get(url, headers=headers)
    print()
    print("查询结果1：", end=' ')
    print(response.text.encode('utf8'))
    url = 'http://gw.erp12345.com/api/Orders/AllOrder/QueryPage?OrderStatus=1&ModelTypeName=ErpWeb.Domain.ViewModels' \
          '.Orders.AllOrderVmv&page=1&pagesize=20 '
    response = requests.get(url, headers=headers)
    print()
    print("查询结果2：", end=' ')
    print(response.text)


def test_add_vip():
    vip_name = base.get_now_string()
    name = interface.new_vip(vip_name)
    print(name)


def test_get_vip_id():
    vip_id = interface.get_vip_info("测试会员1")
    print(vip_id)


def test_get_vip_level_info():
    vip_level_info = interface.get_vip_level_info("8折")
    print(vip_level_info)


def test_modify_vip():
    interface.modify_vip("测试会员1", "8折")
    interface.modify_vip("测试会员1", "固定减5-1")


def test_new_order():
    name = base.get_now_string()
    print(name)
    interface.new_vip(name)
    sku_info = [{'商家编码': '测试商品1-红色 XS', '数量': '2'}, ]
    order_info = order_interface.new_order(name, sku_info)
    print(order_info)
    order_id = order_info["ID"]
    order_code = order_info["Code"]
    print(f"创建订单单号:{order_code}")
    result = order_interface.approve_order(order_id)
    print(result)
    time.sleep(1)
    delivery_order_id = delivery_interface.get_delivery_order_info({"模糊搜索": order_code}, ["ID"])[0]["ID"]
    print(f"发货单ID是{delivery_order_id}")
    delivery_interface.send_delivery(delivery_order_id)
    delivery_order_id = delivery_interface.get_delivered_order_info({"模糊搜索": name}, ["ID"])
    print(f"发货单ID是{delivery_order_id}")


def test_new_order2():
    vip_name = "会员" + base.get_now_string()
    vip_interface.new_vip(vip_name)
    print(f"{vip_name}")
    product_code = base.get_now_string()
    product_interface.new_product(product_code)
    sku_code = product_interface.get_sku_code(product_code)[0]
    product_interface.modify_sku_price(sku_code, "100")
    sku_info = [{'商家编码': sku_code, '数量': '2'}, ]
    order_code = order_interface.new_order(vip_name, sku_info, "测试仓", "买家自提", "巨淘气", {"卖家备注": "111"})["Code"]
    print(order_code)

def test_get_product_info_by_id():
    result = interface.get_sku_price_by_vip_id("20200803195546", "20200803195549-红色 3XL")
    print(result)


def test_new_pos_order():
    sku_info = [
        {'SkuCode': '测试商品1-红色 XS', 'Qty': 2, 'Price': "80"},
        {'SkuCode': '测试商品1-红色 S', 'Qty': 2, 'Price': "90"},
        {'SkuCode': '测试商品1-红色 M', 'Qty': 2, 'Price': "100"},
    ]
    result = interface.new_pos_oder("芮苏云", sku_info)
    print(result)


def test_new_product():
    product_code = base.get_now_string()
    result = product_interface.new_product(product_code)
    print(result)


def test_get_sku_info():
    sku_code = "测试商品1-红色 XS"
    sku_id = product_interface.get_sku_info(sku_code)
    print(sku_id)
    product_info = product_interface.get_sku_info('', "测试商品1")
    print(product_info)


def test_modify_sku_price():
    result = interface.modify_sku_price("07080932-黑 XS XS", "7", )


def test_new_create_sku_bar_code():
    product_code = base.get_now_string()
    interface.new_product(product_code)
    print(f"新建商品,款号：{product_code}")
    sku_id_list = interface.get_sku_id('', product_code)
    print("sku_id列表：")
    print(sku_id_list)
    for i in sku_id_list:
        print(i)
    interface.new_create_sku_bar_code(sku_id_list)
    barcode_list = interface.get_sku_bar_code('', product_code)
    print("barcode_list列表：")
    for i in barcode_list:
        print(i)


def test_get_sku_unique_bar_code():
    result = interface.get_sku_unique_bar_code("测试商品1-红色 XL", 2)
    for i in result:
        print(i)


def test_old_get_delivery_order_info():
    result = interface.get_delivery_order_info()
    print(result)


def test_get_order_info_by_fuzzy():
    result = interface.get_order_info_by_fuzzy("1146084768821949721", ["ID"])
    print(result)


def test_get_order_product_detail():
    result = interface.get_order_product_detail("7495072077142033625", ["供应商ID"])
    print(result)


def test_get_delivery_order_info():
    query_params = {"模糊搜索": "TD200903025"}
    return_info = ["物流单号", "会员名称", ]
    result = delivery_interface.get_delivery_order_info(query_params, return_info)
    print(result)


def test_multi_modify_sku_info():
    sku_id_list = product_interface.get_sku_id("", "20200831095731")
    print(sku_id_list)
    modify_info_dict = {"优先出库仓": "主仓库"}
    product_interface.multi_modify_sku_info(sku_id_list, modify_info_dict)


# 获取仓库信息接口
def test_get_inventory_info():
    result = inventory_interface.get_inventory_info()
    print(result)


def test_new_purchase_order():
    sku_info_list = [{"商家编码": "测试商品1-红色 S", "单价": "20", "数量": "10"}]
    result = purchase_interface.new_purchase_order("主仓库", "供应商1", sku_info_list)
    print(result)
    purchase_order_id = result["ID"]
    result = purchase_interface.approve_and_stock_in_purchase_order(purchase_order_id)
    print(result)


# 获取最新进价成本单价
def test_get_warehouse_cost_price_info():
    query_info_list = {"仓库": "主仓库", "商家编码": "测试商品1-红色 XS"}
    return_info_list = ["最新进价", "成本单价"]
    result = finance_interface.get_warehouse_cost_price_info(query_info_list, return_info_list)
    print(result)


def test_new_stock_in_order():
    sku_info_list = [{"商家编码": "测试商品1-红色 S", "数量": "10"}]
    result = inventory_interface.new_stock_in_order("主仓库", "供应商1", sku_info_list)
    print(result)
    stock_in_order_id = result["ID"]
    result = inventory_interface.stock_in_stock_in_order(stock_in_order_id)
    print(result)


def test_new_stock_out_order():
    sku_info_list = [{"商家编码": "测试商品1-红色 S", "数量": "10"}]
    result = inventory_interface.new_stock_out_order("主仓库", "供应商1", sku_info_list)
    print(result)
    stock_out_order_id = result["ID"]
    result = inventory_interface.stock_out_stock_out_order(stock_out_order_id)
    print(result)


def test_new_refund_out_order():
    sku_info_list = [{"商家编码": "测试商品1-红色 S", "数量": "10"}]
    result = inventory_interface.new_refund_out_order("主仓库", "供应商1", sku_info_list)
    print(result)
    refund_out_order_id = result["ID"]
    result = inventory_interface.stock_out_stock_out_order(refund_out_order_id)
    print(result)


def test_pda_login():
    cookie_str = pda_interface.login()
    print(f"{cookie_str}")


def test_quick_put_away():
    # print(f"pda_cookies:{pda_interface.cookies}")
    bin = "T-1-1-3"
    # bin = "A-1-5-63"
    pda_interface.cookies = pda_interface.change_warehouse("测试仓")["data"]["LoginToken"]
    print(pda_interface.cookies)
    result = pda_interface.quick_put_away(bin, "1907150011407", 5)
    print(result)


def test_quick_sold_out():
    # print(f"pda_cookies:{pda_interface.cookies}")
    bin = "A-1-5-62"
    result = pda_interface.quick_sold_out(bin, "1907150011407", 2)
    print(result)


def test_get_bin_info():
    result = setting_interface.get_bin_info("主仓库")
    result = setting_interface.get_random_bin("主仓库")
    print(f"{result}")


def test_save_auto_merge_setting():
    setting_info = {"开启": "true", "会员相同": "true"}
    setting_interface.save_auto_merge_setting(setting_info)
    time.sleep(5)
    print(f"修改设置之后等待5秒")


def test_get_shop_id():
    shop_id = setting_interface.get_shop_id("巨淘气")
    print(f"{shop_id}")


if __name__ == '__main__':
    pytest.main()
