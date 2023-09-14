import tkinter as tk
from tkinter import messagebox
from .base import Delegate
import os


class PanelMgr:
    """
    界面管理模块,用于管理界面
    """
    instance = None

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self):
        self.panel_delegate = Delegate()

    @staticmethod
    def clean_window(_root: tk.Tk):
        # 获取窗口中的所有子控件
        widgets = _root.winfo_children()
        # 遍历所有子控件，并销毁它们
        for widget in widgets:
            widget.destroy()

    def add_panel(self, _panel_func):
        self.panel_delegate += _panel_func

    def switch_panel(self, _root: tk.Tk, _id: int):
        self.clean_window(_root)
        # 确保生成的frame对象唯一,直接这样调用了
        res = self.panel_delegate(_root, _id)[0]
        return res


class DataKeeper:
    """
    数据暂存模块,用于暂存数据
    """
    instance = None

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self):
        self.info_dic = {}

    def send_data(self, name: str, data):
        self.info_dic[name] = data

    def get_data(self, name: str):
        # 反正None就返回None了呗
        return self.info_dic.get(name)


def check_for_int(int_var: tk.IntVar, name: str, from_num: int, to_num: int) -> bool:
    """
    检查输入书否符合数据类型
    """
    temp = None
    try:
        temp = int_var.get()
    except tk.TclError:
        messagebox.showerror("ERROR", f"请在{name}处输入数字!")
        return False

    if temp < from_num or temp > to_num:
        messagebox.showerror("ERROR", f"请确保在{name}输入的数字\n在{from_num}~{to_num}之间!")
        return False

    return True


def get_file_name(dir_path, extensions=('ALL_FILE_EXTENSION',), _add_default=False):
    """
    得到某个路径下指定后缀的所有文件名(带后缀), 以元组返回
    :param dir_path: 指定路径
    :param extensions: 后缀元组, 需要为全小写且带., 如.txt
    :param _add_default: 是否添加默认元素 'None'
    :return: 字符串元组
    """
    # 定义一个空列表，用于存储文件名
    _names = []
    if _add_default:
        _names.append('None')
    # 获取指定目录下的所有文件和目录的列表
    for path in os.listdir(dir_path):
        # 判断当前元素是否是文件
        if os.path.isfile(os.path.join(dir_path, path)):
            # 获取后缀,只返回匹配后缀的文件名集合
            filename, file_extension = os.path.splitext(os.path.join(dir_path, path))
            # 都转化为小写进行匹配
            file_extension = file_extension.lower()
            # 如果不指定后缀,那么匹配任何文件
            if 'ALL_FILE_EXTENSION' in extensions or file_extension in extensions:
                # 将文件名添加到列表中
                _names.append(path)
    # 将列表转换为元组，并返回
    return tuple(_names)
