import page.base_page as base


# 测试模糊搜索
def test_fuzzy_search(column_name):
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
