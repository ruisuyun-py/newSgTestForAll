import os
import sys
import time
from datetime import datetime
import pytest
from os.path import dirname, abspath
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import test_dir.test_base as test
import page.login_page as login
import page.base_page as base
import page.order.all_order_page as order
import interface.interface as interface
import interface.order.delivery_order_interface as delivery_interface
import interface.supplier.supplier_interface as supplier_interface

sys.path.insert(0, dirname(dirname(dirname(abspath(__file__)))))


def setup_module():
    base.driver = webdriver.Chrome()
    base.cookies = login.login()


def setup_function():
    base.open_page("库存", "库存查询", "库存查询框架")


def teardown_function():
    base.close_page("库存查询")


def teardown_module():
    base.browser_close()


# 验证库存查询页面数据准确性
def test_data_correctness():
    pass
