import time

from page.base_page import *


def login():
    driver.maximize_window()
    driver.get("http://erp12345.com")
    wait_element(find_xpath_by_placeholder("公司名")).send_keys("测试专用")
    wait_element(find_xpath_by_placeholder("用户名")).send_keys("测试")
    wait_element(find_xpath_by_placeholder("登录密码")).send_keys("8888")
    time.sleep(1)
    wait_element(find_xpath("登录")).click()
    wait_element(find_xpath("测试专用-测试"))




