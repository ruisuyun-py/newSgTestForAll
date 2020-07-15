import sys
import time
import pytest
from os.path import dirname, abspath
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

import page.login_page as login
import page.base_page as base

sys.path.insert(0, dirname(dirname(dirname(abspath(__file__)))))


def setup_module(module):
    login.login()


def setup_function(function):
    base.driver.switch_to.default_content()
    base.wait_element(base.find_xpath("订单")).click()
    time.sleep(1)
    base.wait_element(base.find_xpath("全部订单")).click()
    time.sleep(1)
    base.driver.switch_to.default_content()
    frame = base.get_location("全部订单框架")
    base.driver.switch_to.frame(base.driver.find_element_by_xpath(base.get_location("全部订单框架")))


def teardown_function(function):
    base.driver.switch_to.default_content()
    ActionChains(base.driver).double_click(base.wait_element("//span[text()='全部订单']")).perform()


def teardown_module(module):
    base.browser_close()


def test_multi_search():
    """
    base.wait_element(base.locations["批量搜索下拉按钮"]).click()
    base.wait_element(base.find_xpath("搜索类型", "买家账号")).click()
    base.wait_element(base.find_xpath_by_tag_name("搜索类型", "textarea")).send_keys("200623201454")
    base.wait_element(base.find_xpath("确定")).click()
    time.sleep(2)

    base.wait_element(base.find_xpath_by_placeholder("模糊搜索")).click()
    """
    time.sleep(2)


if __name__ == '__main__':
    pytest.main()
