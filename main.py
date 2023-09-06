import re

import requests
from bs4 import BeautifulSoup

keyword = "日本核污染水排海"
page = 1
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0'
}
# 先get一下bilibili.com获取cookie
temp = requests.get("https://bilibili.com", headers=header)
cookie = temp.cookies

url = f"https://api.bilibili.com/x/web-interface/search/all/v2?page={page}&keyword={keyword}&tid=0"
temp = requests.get(url, cookies=cookie, headers=header)

pattern = '"bvid":"(.*?)"'
bv_list = re.findall(pattern, temp.text)

for bv in bv_list:
    print(bv)
