import re
import requests
from bs4 import BeautifulSoup


def BVFinder(_keyword: str, _video_count: int):
    """
    通过关键词获取前n页的相关视频BV号, 返回BV号的字符串列表
    :param _keyword: 关键词
    :param _video_count: 视频数量
    :return: 获取的BV号字符串列表
    """
    result_list = []
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0'}
    # 先get一下bilibili.com获取cookie
    temp = requests.get("https://bilibili.com", headers=header)
    cookie = temp.cookies
    pattern = '"bvid":"(.*?)"'
    print("收集BV号中")
    _page = 1
    while len(result_list) < _video_count:
        url = f"https://api.bilibili.com/x/web-interface/search/all/v2?page={_page}&keyword={_keyword}&tid=0"
        temp = requests.get(url, cookies=cookie, headers=header)
        print(f"请求第{_page}页的数据中")
        temp_bv_list = re.findall(pattern, temp.text)
        result_list += temp_bv_list
        _page += 1
    print("BV号获取完成")
    return result_list


def CidReader(_bv: str):
    """
    读取BV号对应视频的cid
    :param _bv: bv号
    :return: cid字符串
    """
    json_url = f"https://api.bilibili.com/x/player/pagelist?bvid={_bv}&jsonp=jsonp"
    r = requests.get(json_url)
    r.encoding = "utf-8"
    json_str = r.text
    pattern = '"message":"(.*?)"'
    search_result = re.search(pattern, json_str)
    if search_result is None:
        error = Exception("未匹配到状态信息")
        raise error

    elif search_result.group(1) == "请求错误":
        error = Exception("请求错误,请检查BV号是否正确")
        raise error

    pattern = '"cid":(\\d+)'
    search_result = re.search(pattern, json_str)

    cid_value = None
    if search_result is None:
        error = Exception("未匹配到cid信息")
        raise error
    else:
        cid_value = search_result.group(1)
    print(f"BV号:{_bv}\t\t对应cid: {cid_value}")
    return cid_value


def DanmakuReader(_cid: str):
    """
    根据cid读取当前视频弹幕池内弹幕
    :param _cid: cid
    :return: 弹幕列表
    """
    danmaku_url = f"https://comment.bilibili.com/{_cid}.xml"
    danmaku_xml = requests.get(danmaku_url)
    danmaku_xml.encoding = "utf-8"
    # 发现其实用不到这个库
    # soup = BeautifulSoup(danmaku_xml.text, 'xml')
    # print(danmaku_xml.text)
    pattern = '<d p=".*?">(.*?)</d>'
    danmaku_list = re.findall(pattern, danmaku_xml.text)
    return danmaku_list


def DataCollect(_keyword: str, _video_count: int):
    """
    对本模块进行进一步的封装
    :param _keyword: 关键词
    :param _video_count: 视频数
    :return: 弹幕列表
    """
    all_danmaku_list = []
    bv_list = BVFinder(_keyword, _video_count)
    print("开始解析BV号")
    for i in range(_video_count):
        print(f"{i+1}:", end="\t\t")
        cid = CidReader(bv_list[i])
        all_danmaku_list += DanmakuReader(cid)
    print(f"弹幕获取成功,共{len(all_danmaku_list)}条")
    return all_danmaku_list


if __name__ == '__main__':
    keyword = input("输入关键词: \n")
    page = int(input("输入要爬取的视频: \n"))
    res = DataCollect(keyword, page)
