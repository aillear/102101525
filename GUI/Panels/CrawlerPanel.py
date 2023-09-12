from GUI.PanelMgr import *
from Settings import *
from Support.DataKeeper import DataKeeper
from Support.EventCenter import EventCenter
import _thread
from MainWork import DataAnalyst, DataCollector, CSVhandler


def CrawlerPanel(_root: tk.Tk, _id: int) -> tk.Frame:
    if _id != CRAWLER_PANEL_ID:
        return None
    crawler_panel = tk.Frame(_root)
    '''
    具体布局在这里
    '''
    # 第一行
    tk.Label(crawler_panel, text='关键词').grid(row=1, column=1)

    temp = DataKeeper.instance.GetData("keyword")
    if temp is None:
        temp = ''
    keyword = tk.StringVar(value=temp)
    tk.Entry(crawler_panel, textvariable=keyword).grid(row=1, column=2)

    # 第二行
    tk.Label(crawler_panel, text='搜索数').grid(row=2, column=1)

    temp = DataKeeper.instance.GetData("videoCount")
    if temp is None:
        temp = 1
    video_count = tk.IntVar(value=temp)
    tk.Spinbox(crawler_panel, from_=1, to=500, increment=1, textvariable=video_count).grid(row=2, column=2)

    # 第三行
    tk.Label(crawler_panel, text='弹幕文件保存文件名').grid(row=3, column=1)

    temp = DataKeeper.instance.GetData("danmakuSaveName")
    if temp is None:
        temp = 'default'
    danmaku_save_name = tk.StringVar(value=temp)
    tk.Entry(crawler_panel, textvariable=danmaku_save_name).grid(row=3, column=2)

    # 第四行
    # 按钮绑定函数,要做的事情1.保存数据 2.开启新线程来爬虫 3.跳转界面
    def Transmit():
        # 保存数据
        DataKeeper.instance.SendData('keyword', keyword.get())
        DataKeeper.instance.SendData('videoCount', video_count.get())
        DataKeeper.instance.SendData('danmakuSaveName', danmaku_save_name.get())
        # 开启新的线程进行爬虫作业
        # 订阅下爬取完毕事件,该事件将在爬虫线程中触发
        EventCenter.instance.AddEventListener('crawlOver', AfterCrawl)
        _thread.start_new_thread(CrawlerHere, ())   # 新线程执行爬虫
        # 跳转界面到爬取中
        PanelMgr.instance.SwitchPanel(_root, CRAWLING_PANEL_ID)

    # 当副线程结束爬虫之后要做的事
    # 1.取消监听 2.跳转界面
    def AfterCrawl():
        EventCenter.instance.RemoveEventListener('crawlOver', AfterCrawl)
        PanelMgr.instance.SwitchPanel(_root, CRAWLOVER_PANEL_ID)

    tk.Button(crawler_panel, text="启动!", command=Transmit).grid(row=4, column=1)
    crawler_panel.pack()
    return crawler_panel


# 爬虫主要逻辑
def CrawlerHere():
    # 获取用户输入
    keyword = DataKeeper.instance.GetData("keyword")
    if keyword is None:
        keyword = 'default'

    video_count = DataKeeper.instance.GetData("videoCount")
    if video_count is None:
        video_count = 1

    danmaku_save_name = DataKeeper.instance.GetData("danmakuSaveName")
    if danmaku_save_name is None:
        danmaku_save_name = 'default'

    danmaku_save_name += '.xls'
    # 爬虫主要逻辑
    danmaku_list = DataCollector.DataCollect(keyword, video_count)
    DataKeeper.instance.SendData("danmakuList", danmaku_list)
    res_list = DataAnalyst.StrStatistics(danmaku_list)
    DataKeeper.instance.SendData("resList", res_list)

    CSVhandler.List2Excel(res_list, danmaku_save_name)

    # 在这里通知主线程爬取完毕
    EventCenter.instance.EventTrigger('crawlOver')

