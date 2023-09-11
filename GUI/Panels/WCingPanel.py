from GUI.PanelMgr import *
from Settings import *


def WCingPanel(_root: tk.Tk, _id: int) -> tk.Frame:
    if _id != WCING_PANEL_ID:
        return None
    wcing_panel = tk.Frame(_root)
    '''
    具体布局在这里
    '''
    tk.Label(wcing_panel, text='生成词云中,这个过程不会太久').grid(row=1, column=1)

    wcing_panel.pack()
    return wcing_panel
