from .settings import *
from ..UIbase import DataKeeper
import tkinter as tk


def CrawlingPanel(_root: tk.Tk, _id: int) -> tk.Frame:
    if _id != CRAWLING_PANEL_ID:
        return None
    crawling_panel = tk.Frame(_root)
    '''
    具体布局在这里
    '''
    keyword = DataKeeper.instance.get_data('keyword')
    video_count = DataKeeper.instance.get_data('videoCount')
    tk.Label(crawling_panel, text=f"关键词: {keyword}\n爬取视频数{video_count}").grid(row=1, column=1)
    tk.Label(crawling_panel, text='正在爬取中,此过程耗时较久...\n为了防止你觉得卡了,我弄了一个计时器').grid(row=2, column=1)

    time_count = tk.IntVar(value=0)

    def timer():
        time_count.set(time_count.get()+1)
        label_timer.after(1000, timer)

    label_timer = tk.Label(crawling_panel, textvariable=time_count)
    label_timer.grid(row=3, column=1)
    timer()

    crawling_panel.pack()
    return crawling_panel

