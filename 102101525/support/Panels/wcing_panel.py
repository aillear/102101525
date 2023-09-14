from .settings import *
import tkinter as tk


def wcing_panel(_root: tk.Tk, _id: int) -> tk.Frame | None:
    if _id != WCING_PANEL_ID:
        return None
    _wcing_panel = tk.Frame(_root)
    '''
    具体布局在这里
    '''
    tk.Label(_wcing_panel, text='生成词云中,这个过程不会太久').grid(row=1, column=1)

    _wcing_panel.pack()
    return _wcing_panel
