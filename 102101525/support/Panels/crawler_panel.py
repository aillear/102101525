from .settings import *
import _thread
import tkinter as tk
from tkinter import messagebox
from ..crawler_func import data_collect
from ..after_crawl import list2csv, str_statistics
from ..base import EventCenter
from ..UIbase import DataKeeper, PanelMgr, check_for_int



def CrawlerPanel(_root: tk.Tk, _id: int) -> tk.Frame:
    if _id != CRAWLER_PANEL_ID:
        return None
    crawler_panel = tk.Frame(_root)
    '''
    具体布局在这里
    '''
    # 第一行
    tk.Label(crawler_panel, text='关键词').grid(row=1, column=1)

    temp = DataKeeper.instance.get_data("keyword")
    if temp is None:
        temp = ''
    keyword = tk.StringVar(value=temp)
    tk.Entry(crawler_panel, textvariable=keyword).grid(row=1, column=2)

    # 第二行
    tk.Label(crawler_panel, text='搜索数').grid(row=2, column=1)

    temp = DataKeeper.instance.get_data("videoCount")
    if temp is None:
        temp = 1
    video_count = tk.IntVar(value=temp)
    tk.Spinbox(crawler_panel, from_=1, to=500, increment=1, textvariable=video_count).grid(row=2, column=2)

    # 第三行
    tk.Label(crawler_panel, text='弹幕文件保存文件名').grid(row=3, column=1)

    temp = DataKeeper.instance.get_data("danmakuSaveName")
    if temp is None:
        temp = 'danmaku_list'
    danmaku_save_name = tk.StringVar(value=temp)
    tk.Entry(crawler_panel, textvariable=danmaku_save_name).grid(row=3, column=2)

    # 第四行
    # 按钮绑定函数,要做的事情1.保存数据 2.开启新线程来爬虫 3.跳转界面
    def Transmit():
        if check_for_int(video_count, '搜索栏', 1, 500) is False:
            return
        if keyword.get() == '':
            messagebox.showerror("ERROR", "请输入关键词!")
            return
        # 保存数据
        DataKeeper.instance.send_data('keyword', keyword.get())
        DataKeeper.instance.send_data('videoCount', int(video_count.get()))
        DataKeeper.instance.send_data('danmakuSaveName', danmaku_save_name.get())
        # 开启新的线程进行爬虫作业
        # 订阅下爬取完毕事件,该事件将在爬虫线程中触发
        EventCenter.instance.add_event_listener('crawlOver', AfterCrawl)
        _thread.start_new_thread(CrawlerHere, ())  # 新线程执行爬虫
        # 跳转界面到爬取中
        PanelMgr.instance.switch_panel(_root, CRAWLING_PANEL_ID)

    # 当副线程结束爬虫之后要做的事
    # 1.取消监听 2.跳转界面
    def AfterCrawl():
        EventCenter.instance.RemoveEventListener('crawlOver', AfterCrawl)
        PanelMgr.instance.switch_panel(_root, CRAWLOVER_PANEL_ID)

    tk.Button(crawler_panel, text="启动!", command=Transmit).grid(row=4, column=1)
    crawler_panel.pack()
    return crawler_panel


# 爬虫主要逻辑
def CrawlerHere():
    # 获取用户输入
    keyword = DataKeeper.instance.get_data("keyword")
    if keyword is None:
        keyword = '不应该啊,怎么会是None呢?'

    video_count = DataKeeper.instance.get_data("videoCount")
    if video_count is None:
        video_count = 1

    danmaku_save_name = DataKeeper.instance.get_data("danmakuSaveName")
    if danmaku_save_name is None:
        danmaku_save_name = 'danmaku_list'

    # 爬虫主要逻辑
    danmaku_list = data_collect(keyword, video_count)
    DataKeeper.instance.send_data("danmakuList", danmaku_list)
    res_list = str_statistics(danmaku_list)
    DataKeeper.instance.send_data("resList", res_list)

    list2csv(res_list, danmaku_save_name)

    # 在这里通知主线程爬取完毕
    EventCenter.instance.event_trigger('crawlOver')

