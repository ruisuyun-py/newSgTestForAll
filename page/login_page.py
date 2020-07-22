from selenium.webdriver.common.keys import Keys
import page.base_page as base


def login():
    base.driver.maximize_window()
    base.driver.get("http://erp12345.com")
    base.wait_element(base.find_xpath_by_placeholder("公司名")).send_keys(Keys.CONTROL+'a')
    base.wait_element(base.find_xpath_by_placeholder("公司名")).send_keys("测试专用")
    base.wait_element(base.find_xpath_by_placeholder("用户名")).send_keys(Keys.CONTROL+'a')
    base.wait_element(base.find_xpath_by_placeholder("用户名")).send_keys("测试")
    base.wait_element(base.find_xpath_by_placeholder("登录密码")).send_keys(Keys.CONTROL+'a')
    base.wait_element(base.find_xpath_by_placeholder("登录密码")).send_keys("8888")
    base.wait_element(base.find_xpath("登录")).click()
    base.wait_element(base.find_xpath("测试专用-测试"))
    coo = base.driver.get_cookies()
    cookie_str = 'TOKEN='
    for c in coo:
        if c['name'] == 'TOKEN':
            cookie_str += c['value']
            cookie_str += ';'
        elif c['name'] == 'TENANTID':
            cookie_str += 'TENANTID='
            cookie_str += c['value']

    return cookie_str


