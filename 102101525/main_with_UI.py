from support.base import EventCenter
from support.UIbase import DataKeeper, PanelMgr
from support.Panels.crawler_panel import crawler_panel
from support.Panels.crawling_panel import crawling_panel
from support.Panels.crawl_over_panel import crawl_over_panel
from support.Panels.wc_panel import wc_panel
from support.Panels.wcing_panel import wcing_panel
from support.Panels.wc_over_panel import wc_over_panel
from support.Panels.settings import *
import tkinter as tk

# 初始化单例
EC = EventCenter()
DK = DataKeeper()

PM = PanelMgr()
PanelMgr.instance.add_panel(crawler_panel)
PanelMgr.instance.add_panel(crawling_panel)
PanelMgr.instance.add_panel(crawl_over_panel)
PanelMgr.instance.add_panel(wc_panel)
PanelMgr.instance.add_panel(wcing_panel)
PanelMgr.instance.add_panel(wc_over_panel)


root = tk.Tk()
root.geometry(f"{WIDTH}x{HEIGHT}")
PanelMgr.instance.switch_panel(root, CRAWLER_PANEL_ID)


root.mainloop()
