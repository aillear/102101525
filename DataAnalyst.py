
def StrStatistics(_str_list: list[str]):
    """
    字符串列表去重，统计同一字符串的数量，返回元组(str, int)的列表
    :param _str_list: 待处理的字符串列表
    :return: 处理后的元组列表
    """
    dic = {}
    for _str in _str_list:
        if _str in dic:
            dic[_str] += 1
        else:
            dic[_str] = 1
    # 直接在这里排个序
    res_list = sorted(dic.items(), key=lambda x: x[1], reverse=True)
    return res_list


if __name__ == "__main__":
    str_list = ['aaa', 'bbb', 'ccc', 'ddd', 'eee', 'aaa', 'aaa', 'bbb']
    res = StrStatistics(str_list)
    print(res)
