import time

import page.base_page as base


# 测试模糊搜索
def fuzzy_search_test(column_name):
    """
    column_name:列名
    简单粗暴，直接获取列的值，然后一个个搜索结果搜索出来的对应列的结果必须和输入值一样
    """
    platform_code_list = base.get_column_text(column_name)
    for i in platform_code_list:
        base.fuzzy_search(column_name, i)
        result = base.get_column_text(column_name)
        for r in result:
            assert r == i


# 测试时间组件的快捷方法
def time_component_test(key_name):
    """
    key_name:place_holder，column_name,目前没发现不一样的，直接使用一个key_name表示
    """
    time_options = ["昨天", "30天内", "上月", "今天", "本周", "今年", "3天内", "上周", "去年", "7天内", "本月"]
    base.wait_element_click(base.find_xpath("时间"))
    for i in time_options:
        base.wait_element_click(base.find_xpath_by_placeholder(key_name))
        base.wait_element_click(base.find_xpath(i))
        base.wait_element_click(base.find_xpath_by_placeholder(key_name))
        start_time = base.wait_element(base.find_xpath_by_placeholder("时间开始")).get_attribute("value")
        end_time = base.wait_element(base.find_xpath_by_placeholder("时间结束")).get_attribute("value")
        base.wait_element_click(base.find_xpath(i))
        base.wait_table_refresh(base.find_xpath("组合查询"), 1, key_name)
        result = base.get_column_text(key_name)
        for j in result:
            time_str = j.replace("\n", " ")
            time_format_str = time.strptime(time_str, "%Y-%m-%d %H:%M:%S")
            start = time.strptime(start_time, "%Y-%m-%d %H:%M:%S")
            end = time.strptime(end_time, "%Y-%m-%d %H:%M:%S")
            print(f"{start_time} < {time_str} < {end_time}")
            assert start < time_format_str < end
