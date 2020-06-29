import datetime
from selenium import webdriver

driver = webdriver.Chrome()
locations = {
    "全部订单框架": "//iframe[contains(@src,'orders/allOrder/orderbrowserview')]",
}


def get_location(key_name):
    return locations[key_name]


def find_xpath_by_placeholder(keywords):
    xpath = "//*[@placeholder='{}']".format(keywords)
    return xpath


def find_xpath(keywords):
    xpath = "//*[text()='{}']".format(keywords)
    return xpath


def wait_element(xpath):
    start = datetime.datetime.now()
    while (datetime.datetime.now() - start).seconds < 30:
        try:
            element = driver.find_element_by_xpath(xpath)
            if element:
                return element
            else:
                continue
        except Exception:
            continue
    assert 1 == 2, "元素不存在:{}".format(xpath)


def browser_close():
    driver.quit()
