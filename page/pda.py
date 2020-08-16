import page.base_page as base
from appium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


def login():
    # 获取登录按钮
    company_name = base.driver.find_element(By.ID, "com.pda.cleo:id/edit_login_companyname")
    company_name.send_keys("测试专用")
    user_name = base.driver.find_element(By.ID, "com.pda.cleo:id/edit_login_username")
    user_name.send_keys("测试")
    password = base.driver.find_element(By.ID, "com.pda.cleo:id/edit_login_password")
    password.send_keys("8888")
    login_btn = base.driver.find_element(By.ID, "com.pda.cleo:id/btn_login_login")
    # 点击登录按钮
    login_btn.click()


def find_xpath(keywords1, keywords2=''):
    if keywords2 == '':
        xpath = f"//*[@text='{keywords1}']"
    else:
        xpath = f"//*[@text='{keywords1}']/following-sibling::*[@text='{keywords2}']"
    return xpath


def find_xpath_by_tag_name(keywords1, keywords2):
    xpath = f"//*[@text='{keywords1}']/following-sibling::android.widget.{keywords2}"
    return xpath


def get_cell_xpath(row_key, column_index, inner_row_index=''):
    """
    row_id:行号，由于主表的行号是从0计数，这里做了-1处理
    column_name:列名
    return:单元格定位
    """
    column_index -= 1
    if isinstance(row_key, int):
        row_key -= 1
        if inner_row_index == '':
            xpath = f"//android.widget.ListView/*[@index='{row_key}']/*[@index='{column_index}']"
        else:
            inner_row_index -= 1
            xpath = f"//android.widget.ListView/*[@index='{row_key}']/*[@index='{column_index}']/*[@index='{inner_row_index}'] "
    else:
        if inner_row_index == '':
            xpath = f"//*[@text='{row_key}']/../../*[@index='{column_index}']"
        else:
            inner_row_index -= 1
            xpath = f"//*[@text='{row_key}']/../../*[@index='{column_index}']/*[@index='{inner_row_index}']"
    print(xpath)
    return xpath


def send_enter():
    base.driver.keyevent(66)
