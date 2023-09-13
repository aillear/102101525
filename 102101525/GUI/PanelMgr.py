from Support.Delegate import Delegate
import tkinter as tk


class PanelMgr:
    instance = None

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self):
        self.panel_delegate = Delegate()

    @staticmethod
    def CleanWindow(_root: tk.Tk):
        # 获取窗口中的所有子控件
        widgets = _root.winfo_children()
        # 遍历所有子控件，并销毁它们
        for widget in widgets:
            widget.destroy()

    def AddPanel(self, _panel_func):
        self.panel_delegate += _panel_func

    def SwitchPanel(self, _root: tk.Tk, _id: int):
        self.CleanWindow(_root)
        # 确保生成的frame对象唯一,直接这样调用了
        res = self.panel_delegate(_root, _id)[0]
        return res

