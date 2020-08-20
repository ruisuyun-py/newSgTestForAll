import sys
import time
import pytest
from os.path import dirname, abspath
from appium import webdriver
import page.pda as pda
import page.base_page as base
import page.interface as interface
import page.login_page as login
sys.path.insert(0, dirname(dirname(dirname(abspath(__file__)))))


def setup_module():
    base.cookies = interface.get_cookie()
    # appium服务监听地址
    server = 'http://localhost:4723/wd/hub'  # localhost为本机；4723为端口；/wd/hub可以看成是规定的默认地址
    # app启动参数
    desired_caps = {
        "platformName": "Android",  # platformName：使用哪个移动操作系统平台；iOS，Android或FirefoxOS
        "deviceName": "127.0.0.1:62001",  # deviceName：使用的移动设备或模拟器的种类
        "appPackage": "com.pda.cleo",  # appPackage：你想运行的Android应用程序的Java包（仅限Android使用）
        "appActivity": "com.pan.cleo.ac.main.LoginActivity",  # 要从包中启动的Android活动的活动名称。（仅限Android使用）
        "unicodeKeyboard": True,  # 允许Unicode编码格式的输入
        "resetKeyboard": True  # 初始化键盘状态，和unicodeKeyboard配合使用时生效，以实现Unicode测试
    }
    # 驱动
    base.driver = webdriver.Remote(server, desired_caps)
    pda.login()


def setup_function():
    pass


def teardown_function():
    pass


def teardown_module():
    base.browser_close()


def test_pos_order():
    setting_info = {
        "记录会员上次交易价：手工单或者门店单保存时，记录会员的商品交易价格": "true",
        "记录会员上次交易价 同款同价：手工单或者门店单保存时，记录会员的商品交易价格 同款同价": "true",
        "只有手工修改售价才会记录预设价格": "true",
    }
    interface.save_order_setting(setting_info)
    print("这就为了换个行")
    print("非同款同价模式+修改才记录会员价设置完成，修改设置之后等5秒，让设置生效")
    setting_info = {
        "启用条码唯一码": "true",
    }
    interface.save_base_setting(setting_info)
    print("启用唯一码设置完成，等待5秒保证设置生效")
    time.sleep(5)
    base.wait_element_click(pda.find_xpath("门店开单"))
    base.wait_element_click(pda.find_xpath("我要开单"))
    barcode_input = base.wait_element_click(pda.find_xpath_by_tag_name("条码", "EditText"))
    product_code = base.get_now_string()
    interface.new_product(product_code)
    print(f"新建商品,款号：{product_code}")
    sku_code = interface.get_sku_code(product_code)[0]
    price = 50.0
    interface.modify_sku_price(sku_code, price)
    print(f"获取一个sku_code:{sku_code},并修改价格为{price}")
    sku_id_list = interface.get_sku_id('', product_code)
    print("获取所有商品的sku_id列表，用来创建商品条码：商品id列表：")
    for i in sku_id_list:
        print(i)
    print("新建所有商品的商品条码")
    interface.new_create_sku_bar_code(sku_id_list)
    print("用barcode_list保存商品的商家编码")
    barcode_list = interface.get_sku_bar_code('', product_code)[0:3]
    print("barcode_list列表：")
    num = 0
    input_barcode_info = {}
    for i in barcode_list:
        print("barcode:"+i)
        num += 1
        input_barcode_info[i] = num
    print("使用input_barcode_info记录要输入的商家编码和数量{'barcode':num ,'barcode':num}")
    print("使用input_barcode_info录入商品条码")
    for k, v in input_barcode_info.items():
        print(f"输入条码：{k}共计：{v}次")
        for i in range(0, v):
            barcode_input.set_text(k)
            pda.send_enter()
    print(f"验证条码输入的结果和input_barcode_info中记录的数据完全一致")
    for k, v in input_barcode_info.items():
        # 条码必须等于barcode
        result = base.wait_element(pda.get_cell_xpath(k, 1, 2)).text
        assert result == k
        num = base.wait_element(pda.get_cell_xpath(k, 2)).text
        assert num == str(v)
        unit_price = base.wait_element(pda.get_cell_xpath(k, 3)).text
        assert unit_price == str(price)
        amount = base.wait_element(pda.get_cell_xpath(k, 4)).text
        assert amount == str(float(num)*float(unit_price))
        print(f"条码{result}输入了{num}个，每个单价{unit_price},总价{amount}")
    print(f"点击第一行的第一列，调出修改界面")
    base.wait_element_click(pda.get_cell_xpath(1, 1))
    base.wait_element(pda.find_xpath_by_tag_name("价格", "EditText")).clear()
    modify_price = "100"
    base.wait_element(pda.find_xpath_by_tag_name("价格", "EditText")).set_text(modify_price)
    base.wait_element_click(pda.find_xpath("保存"))
    unit_price = pda.get_column_text(2)
    for i in unit_price:
        assert float(i) == float(modify_price)
    print("通过sku_code获取唯一码")
    nuique_sku_code = interface.get_sku_unique_bar_code(sku_code, 3)
    print(f"输入nuique_sku_code中的唯一码")
    for i in nuique_sku_code:
        barcode_input.set_text(i)
        pda.send_enter()
    print("验证每个唯一码的商家编码必须是sku_code,数量必须是1，价格是price,金额是1*price")
    for k in nuique_sku_code:
        print(f"扫描的唯一码是{k}")
        # 商家编码必须是sku_code
        unique_sku_code = base.wait_element(pda.get_cell_xpath(k, 1, 1)).text
        assert unique_sku_code == sku_code
        # 条码必须等于barcode
        result = base.wait_element(pda.get_cell_xpath(k, 1, 2)).text
        assert result == k
        num = base.wait_element(pda.get_cell_xpath(k, 2)).text
        assert num == "1"
        unit_price = base.wait_element(pda.get_cell_xpath(k, 3)).text
        assert unit_price == str(price)
        amount = base.wait_element(pda.get_cell_xpath(k, 4)).text
        assert amount == str(float(num)*float(unit_price))
        print(f"{k}输入了1次，商家编码是{unique_sku_code},价格是{price},金额是{amount}")
    print(f"点击第一行的第一列，调出修改界面，将价格修改为200")
    base.wait_element_click(pda.get_cell_xpath(1, 1))
    base.wait_element(pda.find_xpath_by_tag_name("价格", "EditText")).clear()
    modify_price = "200"
    base.wait_element(pda.find_xpath_by_tag_name("价格", "EditText")).set_text(modify_price)
    base.wait_element_click(pda.find_xpath("保存"))
    unit_price = pda.get_column_text(2)
    for i in unit_price:
        assert float(i) == float(modify_price)
    print(f"确定修改之后价格全部为200")


def test_001():
    pass


if __name__ == '__main__':
    pytest.main()
