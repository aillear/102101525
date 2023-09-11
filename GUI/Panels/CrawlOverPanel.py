from GUI.PanelMgr import *
from Settings import *
from Support.DataKeeper import DataKeeper


def CrawlOverPanel(_root: tk.Tk, _id: int) -> tk.Frame:
    if _id != CRAWLOVER_PANEL_ID:
        return None
    crawl_over_panel = tk.Frame(_root)
    '''
    具体布局在这里
    '''
    res_list = DataKeeper.instance.GetData('resList')
    if res_list is None:
        raise TypeError('res_list is a list of tuples like (str, int), but now is None')
    # 生成前20条弹幕
    str_list = []
    for i in range(20):
        str_list.append(f"出现次数:{res_list[i][1]}\n内容:{res_list[i][0]}")

    file_name = f"爬取结束,已保存为: {DataKeeper.instance.GetData('danmakuSaveName')}.csv\n下面是前20条结果:"
    tk.Label(crawl_over_panel, text=file_name).grid(row=1, column=1)

    page = 0

    text1 = tk.StringVar(value=f"第{page+1}/20页")
    tk.Label(crawl_over_panel, textvariable=text1).grid(row=2, column=1)

    text2 = tk.StringVar(value=str_list[page])
    tk.Label(crawl_over_panel, textvariable=text2, wraplength=200,
             relief=tk.SUNKEN, anchor=tk.NW).grid(row=3, column=1)

    def PrevPage():
        nonlocal page
        if page > 0:
            page -= 1
            text1.set(f"第{page+1}/20页")
            text2.set(str_list[page])

    def NextPage():
        nonlocal page
        if page < 19:
            page += 1
            text1.set(f"第{page+1}/20页")
            text2.set(str_list[page])

    # 转移到下一页
    def Transmit():
        PanelMgr.instance.SwitchPanel(_root, WC_PANEL_ID)

    tk.Button(crawl_over_panel, text='上一条', command=PrevPage).grid(row=4, column=1)
    tk.Button(crawl_over_panel, text='下一条', command=NextPage).grid(row=4, column=2)
    tk.Button(crawl_over_panel, text='去生成词云', command=Transmit).grid(row=5, column=1)

    crawl_over_panel.pack()
    return crawl_over_panel
