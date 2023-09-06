import re
import requests
from bs4 import BeautifulSoup


def BVFinder(_keyword: str, _page_count: int):
    result_list = []
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0'}
    # 先get一下bilibili.com获取cookie
    temp = requests.get("https://bilibili.com", headers=header)
    cookie = temp.cookies
    pattern = '"bvid":"(.*?)"'

    for i in range(1, _page_count + 1):
        url = f"https://api.bilibili.com/x/web-interface/search/all/v2?page={i}&keyword={_keyword}&tid=0"
        temp = requests.get(url, cookies=cookie, headers=header)
        temp_bv_list = re.findall(pattern, temp.text)
        print(len(temp_bv_list))
        result_list += temp_bv_list

    return result_list


def CidReader(_bv: str):
    """
    读取BV号对应视频的cid
    :param _bv: bv号
    :return: cid字符串
    """
    cid_value = None
    json_url = f"https://api.bilibili.com/x/player/pagelist?bvid={bv}&jsonp=jsonp"
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

    if search_result is None:
        error = Exception("未匹配到cid信息")
        raise error
    else:
        cid_value = search_result.group(1)
    print(f"得到的cid: {cid_value}\n")
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


if __name__ == '__main__':
    keyword = input("输入关键词: ")
    page = int(input("输入要爬取的页数"))
    res = BVFinder(keyword, page)
    print(len(res))
