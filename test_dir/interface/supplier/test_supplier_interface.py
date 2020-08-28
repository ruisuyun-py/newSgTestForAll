import sys
from os.path import dirname, abspath
import page.base_page as base
import interface.interface as interface
import interface.supplier.supplier_interface as supplier_interface
import pytest
import requests

sys.path.insert(0, dirname(dirname(dirname(abspath(__file__)))))


def setup_module(browser):
    base.cookies = interface.get_cookie()


def setup_function():
    pass


def teardown_function():
    pass


def teardown_module():
    pass


def test_get_supplier_info():
    result = supplier_interface.get_supplier_info("供应商1", ["供应商ID", "市场"])
    print(result)


if __name__ == '__main__':
    pytest.main()