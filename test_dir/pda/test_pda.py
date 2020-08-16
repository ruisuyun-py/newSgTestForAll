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
    base.wait_element_click(pda.find_xpath("门店开单"))
    base.wait_element_click(pda.find_xpath("我要开单"))
    barcode_input = base.wait_element_click(pda.find_xpath_by_tag_name("条码", "EditText"))
    product_code = base.get_now_string()
    interface.new_product(product_code)
    print(f"新建商品,款号：{product_code}")
    sku_id_list = interface.get_sku_id('', product_code)
    print("sku_id列表：")
    for i in sku_id_list:
        print(i)
    interface.new_create_sku_bar_code(sku_id_list)
    barcode_list = interface.get_sku_bar_code('', product_code)
    print("barcode_list列表：")
    for i in barcode_list:
        print(i)
    j = 2
    print("barcode_list[1:3]")
    for i in barcode_list[0:3]:
        print(i)
    for barcode in barcode_list:
        for i in range(1, j):
            print(f"第{i}次录入{barcode}")
            barcode_input.send_keys(barcode)
            pda.send_enter()
        j = j+1
    for barcode in barcode_list:
        # 条码必须等于barcode
        result = base.wait_element(pda.get_cell_xpath(barcode, 1, 2)).text
        assert result == barcode
        # result = base.wait_element(pda.get_cell_xpath(barcode, 2)).text
        # assert result == '1'


def test_001():
    pass


if __name__ == '__main__':
    pytest.main()
