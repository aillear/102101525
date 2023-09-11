from GUI.PanelMgr import *
from Support.EventCenter import EventCenter
from Support.DataKeeper import DataKeeper
from Settings import *
from GUI.Panels.CrawlerPanel import CrawlerPanel
from GUI.Panels.CrawllingPanel import CrawlingPanel
from GUI.Panels.CrawlOverPanel import CrawlOverPanel
from GUI.Panels.WCPanel import WCPanel
from GUI.Panels.WCingPanel import WCingPanel
from GUI.Panels.WCOverPanel import WCOverPanel

# 初始化单例
EC = EventCenter()
DK = DataKeeper()

PM = PanelMgr()
PanelMgr.instance.AddPanel(CrawlerPanel)
PanelMgr.instance.AddPanel(CrawlingPanel)
PanelMgr.instance.AddPanel(CrawlOverPanel)
PanelMgr.instance.AddPanel(WCPanel)
PanelMgr.instance.AddPanel(WCingPanel)
PanelMgr.instance.AddPanel(WCOverPanel)


root = tk.Tk()
root.geometry(f"{WIDTH}x{HEIGHT}")
PanelMgr.instance.SwitchPanel(root, CRAWLER_PANEL_ID)


root.mainloop()
