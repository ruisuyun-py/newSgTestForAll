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
    sku_code = interface.get_sku_code("",product_code)[0]
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
    barcode_list = interface.get_sku_bar_code('', product_code)
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


def test_001():
    pass


if __name__ == '__main__':
    pytest.main()
