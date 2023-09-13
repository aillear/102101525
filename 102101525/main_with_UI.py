from support.base import EventCenter
from support.UIbase import DataKeeper, PanelMgr
from support.Panels.crawler_panel import CrawlerPanel
from support.Panels.crawling_panel import CrawlingPanel
from support.Panels.crawl_over_panel import CrawlOverPanel
from support.Panels.wc_panel import WCPanel
from support.Panels.wcing_panel import WCingPanel
from support.Panels.wc_over_panel import WCOverPanel
from support.Panels.settings import *
import tkinter as tk

# 初始化单例
EC = EventCenter()
DK = DataKeeper()

PM = PanelMgr()
PanelMgr.instance.add_panel(CrawlerPanel)
PanelMgr.instance.add_panel(CrawlingPanel)
PanelMgr.instance.add_panel(CrawlOverPanel)
PanelMgr.instance.add_panel(WCPanel)
PanelMgr.instance.add_panel(WCingPanel)
PanelMgr.instance.add_panel(WCOverPanel)


root = tk.Tk()
root.geometry(f"{WIDTH}x{HEIGHT}")
PanelMgr.instance.switch_panel(root, CRAWLER_PANEL_ID)


root.mainloop()
