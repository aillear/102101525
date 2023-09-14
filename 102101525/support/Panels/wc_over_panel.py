from .settings import *
from ..UIbase import DataKeeper, PanelMgr
from PIL import Image, ImageTk
import tkinter as tk

img_tk = None


def wc_over_panel(_root: tk.Tk, _id: int) -> tk.Frame:
    if _id != WCOVER_PANEL_ID:
        return None
    _wc_over_panel = tk.Frame(_root)
    '''
    具体布局在这里
    '''
    image_name = DataKeeper.instance.get_data('imageName')
    if image_name is None:
        raise TypeError('image_name should not be None!')

    # 第一行
    tk.Label(_wc_over_panel, text=f'生成成功!保存为./word_cloud_image/{image_name}.png').grid(row=1)

    # 第二行
    img = Image.open(f"./word_cloud_image/{image_name}.png")
    w, h = img.size
    img = img.resize((300, int(300*h/w)))
    global img_tk
    img_tk = ImageTk.PhotoImage(img)
    label = tk.Label(_wc_over_panel, image=img_tk)
    label.grid(row=2)

    # 第三行
    tk.Button(_wc_over_panel, text='再来一次',
              command=lambda: PanelMgr.instance.switch_panel(_root, CRAWLER_PANEL_ID)).grid(row=3)

    _wc_over_panel.pack()
    return _wc_over_panel
