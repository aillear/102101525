from tkinter import Frame
from ..UIbase import PanelMgr, DataKeeper
from .settings import *
import tkinter as tk


def CrawlOverPanel(_root: tk.Tk, _id: int) -> Frame | None:
    if _id != CRAWLOVER_PANEL_ID:
        return None
    crawl_over_panel = tk.Frame(_root)
    '''
    具体布局在这里
    '''
    res_list = DataKeeper.instance.get_data('resList')
    if res_list is None:
        raise TypeError('res_list is a list of tuples like (str, int), but now is None')
    elif len(res_list) == 0:
        res_list.append(('如果出现此信息, 说明目标视频中没有任何弹幕', -1))
    # 生成前20条弹幕
    str_list = []
    str_list_len = len(res_list) if len(res_list) < 20 else 20
    for i in range(str_list_len):
        str_list.append(f"出现次数:{res_list[i][1]}\n内容:{res_list[i][0]}")

    file_name = (f"爬取结束,已保存为: {DataKeeper.instance.get_data('danmakuSaveName')}.csv\n"
                 f"弹幕一共{len(res_list)}条.\n"
                 f"下面是前{str_list_len}条结果:")
    tk.Label(crawl_over_panel, text=file_name).grid(row=1, column=1)

    page = 0

    text1 = tk.StringVar(value=f"第{page+1}/{str_list_len}页")
    tk.Label(crawl_over_panel, textvariable=text1).grid(row=2, column=1)

    text2 = tk.StringVar(value=str_list[page])
    tk.Label(crawl_over_panel, textvariable=text2, wraplength=200,
             relief=tk.SUNKEN, anchor=tk.NW).grid(row=3, column=1)

    def PrevPage():
        nonlocal page
        if page > 0:
            page -= 1
            text1.set(f"第{page+1}/{str_list_len}页")
            text2.set(str_list[page])

    def NextPage():
        nonlocal page
        if page < str_list_len-1:
            page += 1
            text1.set(f"第{page+1}/{str_list_len}页")
            text2.set(str_list[page])

    # 转移到下一页
    def Transmit():
        PanelMgr.instance.switch_panel(_root, WC_PANEL_ID)

    tk.Button(crawl_over_panel, text='上一条', command=PrevPage).grid(row=4, column=1)
    tk.Button(crawl_over_panel, text='下一条', command=NextPage).grid(row=4, column=2)
    if res_list[0][1] != -1:
        tk.Button(crawl_over_panel, text='去生成词云', command=Transmit).grid(row=5, column=1)

    crawl_over_panel.pack()
    return crawl_over_panel
