import sys
import time
import pytest
from os.path import dirname, abspath
from appium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

sys.path.insert(0, dirname(dirname(dirname(abspath(__file__)))))


# def setup_module():
#     pass
#
#
# def setup_function():
#     pass
#
#
# def teardown_function():
#     pass
#
#
# def teardown_module():
#     pass


def test_pda_login():

    # appium服务监听地址
    server = 'http://localhost:4723/wd/hub'  # localhost为本机；4723为端口；/wd/hub可以看成是规定的默认地址
    # app启动参数
    desired_caps = {
        "platformName": "Android",  # platformName：使用哪个移动操作系统平台；iOS，Android或FirefoxOS
        "deviceName": "127.0.0.1:62001",  # deviceName：使用的移动设备或模拟器的种类
        "appPackage": "com.pda.cleo",  # appPackage：你想运行的Android应用程序的Java包（仅限Android使用）
        "appActivity": "com.pan.cleo.ac.main.LoginActivity"  # 要从包中启动的Android活动的活动名称。（仅限Android使用）
    }

    # 驱动
    driver = webdriver.Remote(server, desired_caps)
    wait = WebDriverWait(driver, 30)
    # 获取登录按钮
    company_name = wait.until(EC.presence_of_element_located((By.ID, "com.pda.cleo:id/edit_login_companyname")))
    company_name.send_keys(Keys.CONTROL+'a')
    company_name.send_keys("测试专用")
    user_name = wait.until(EC.presence_of_element_located((By.ID, "com.pda.cleo:id/edit_login_username")))
    user_name.send_keys(Keys.CONTROL + 'a')
    user_name.send_keys("测试")
    password = wait.until(EC.presence_of_element_located((By.ID, "com.pda.cleo:id/edit_login_password")))
    password.send_keys(Keys.CONTROL + 'a')
    password.send_keys("8888")
    login_btn = wait.until(EC.presence_of_element_located((By.ID, "com.pda.cleo:id/btn_login_login")))
    # 点击登录按钮
    login_btn.click()
    time.sleep(5)
    # # 获取手机号文本框
    # phone_text = wait.until(EC.presence_of_element_located((By.ID, "com.tencent.mm:id/li")))
    # # 填写手机号文本框
    # phone_text.send_keys("12345678900")


if __name__ == '__main__':
    pytest.main()
