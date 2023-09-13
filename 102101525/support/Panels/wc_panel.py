import tkinter as tk
from .settings import *
import tkinter.ttk
from ..base import EventCenter
from ..UIbase import PanelMgr, DataKeeper, get_file_name, check_for_int
from ..after_crawl import create_word_cloud_image
import jieba
import _thread
from PIL import Image, ImageTk
import os


mask_tk = None


def WCPanel(_root: tk.Tk, _id: int) -> tk.Frame | None:
    if _id != WC_PANEL_ID:
        return None
    wc_panel = tk.Frame(_root)
    '''
    具体布局在这里
    '''
    # 第一行
    tk.Label(wc_panel, text='生成图片名').grid(row=1, column=1)

    temp = DataKeeper.instance.get_data('imageName')
    if temp is None:
        temp = 'WCImage'
    image_name = tk.StringVar(value=temp)
    tk.Entry(wc_panel, textvariable=image_name).grid(row=1, column=2)

    # 第二行
    tk.Label(wc_panel, text='最大词数').grid(row=2, column=1)

    temp = DataKeeper.instance.get_data('maxWordNum')
    if temp is None:
        temp = 100
    max_word_num = tk.IntVar(value=temp)
    tk.Spinbox(wc_panel, from_=50, to=500, increment=1, textvariable=max_word_num).grid(row=2, column=2)

    # 第三行
    tk.Label(wc_panel, text='图片尺寸').grid(row=3, column=1)

    temp = DataKeeper.instance.get_data('imageWidth')
    if temp is None:
        temp = 1000
    image_width = tk.IntVar(value=temp)
    tk.Entry(wc_panel, textvariable=image_width).grid(row=3, column=2)

    tk.Label(wc_panel, text='x').grid(row=3, column=3)

    temp = DataKeeper.instance.get_data('imageHeight')
    if temp is None:
        temp = 1000
    image_height = tk.IntVar(value=temp)
    tk.Entry(wc_panel, textvariable=image_height).grid(row=3, column=4)

    # 第四行
    tk.Label(wc_panel, text='字体').grid(row=4, column=1)

    fonts_name = tkinter.ttk.Combobox(wc_panel, state='readonly')
    fonts_name['value'] = get_file_name('./fonts', ('.ttc', '.ttf'))
    fonts_name.current(0)
    fonts_name.grid(row=4, column=2)

    # 第五行
    tk.Label(wc_panel, text='图片遮罩,启用后上面设置的宽高失效').grid(row=6, column=1)

    mask_name = tkinter.ttk.Combobox(wc_panel, state='readonly')
    mask_name['value'] = get_file_name('./image_masks', ('.png', '.jpg', '.jpeg', '.gif'),
                                       True)
    mask_name.current(0)
    mask_name.grid(row=5, column=2)

    # 第六行
    mask_img = None
    if os.path.exists(f"./image_masks/{mask_name.get()}"):
        mask_img = Image.open(f"./image_masks/{mask_name.get()}")
    else:
        mask_img = Image.new("RGB", (300, 300), (0, 0, 0))

    global mask_tk
    mask_tk = ImageTk.PhotoImage(mask_img)
    mask_label = tk.Label(wc_panel, image=mask_tk)
    mask_label.grid(row=6)

    def ChangeMask(garbage):
        _mask_img = None
        if os.path.exists(f"./image_masks/{mask_name.get()}"):
            _mask_img = Image.open(f"./image_masks/{mask_name.get()}")
            w, h = _mask_img.size
            _mask_img = _mask_img.resize((int(300 * w / h), 300))
        else:
            _mask_img = Image.new("RGB", (300, 300), (0, 0, 0))

        global mask_tk
        mask_tk = ImageTk.PhotoImage(_mask_img)
        mask_label.configure(image=mask_tk)

    mask_name.bind('<<ComboboxSelected>>', ChangeMask)

    # 第七行
    # 按钮绑定函数
    # 1.保存数据 2.新线程生成图片 3.跳转界面
    def Transmit():
        if not check_for_int(max_word_num, '最大词数', 1, 1000):
            return
        if not check_for_int(image_width, '图片宽度', 1, 5000):
            return
        if not check_for_int(image_height, '图片高度', 1, 5000):
            return
        #  保存数据
        DataKeeper.instance.send_data('imageName', image_name.get())
        DataKeeper.instance.send_data('maxWordNum', int(max_word_num.get()))
        DataKeeper.instance.send_data('imageWidth', int(image_width.get()))
        DataKeeper.instance.send_data('imageHeight', int(image_height.get()))
        DataKeeper.instance.send_data('font', fonts_name.get())
        DataKeeper.instance.send_data('maskName', mask_name.get())
        # 开新线程来生成词云
        # 订阅下生成玩事件,不过一般都不久
        EventCenter.instance.add_event_listener('WCOver', AfterWC)
        _thread.start_new_thread(WCHere, ())    # 新线程生成图片
        # 跳转界面
        PanelMgr.instance.switch_panel(_root, WCING_PANEL_ID)

    # 生成图片之后要做的事
    # 1.取消监听 2.跳转界面
    def AfterWC():
        EventCenter.instance.RemoveEventListener('WCOver', AfterWC)
        PanelMgr.instance.switch_panel(_root, WCOVER_PANEL_ID)    # 跳转界面

    tk.Button(wc_panel, text='启动!', command=Transmit).grid(row=7, column=1)

    wc_panel.pack()
    return wc_panel


# 生成词云的逻辑
def WCHere():
    danmaku_list = DataKeeper.instance.get_data('danmakuList')
    image_name = DataKeeper.instance.get_data('imageName')
    image_width = DataKeeper.instance.get_data('imageWidth')
    image_height = DataKeeper.instance.get_data('imageHeight')
    max_word_num = DataKeeper.instance.get_data('maxWordNum')
    font = DataKeeper.instance.get_data('font')
    mask_name = DataKeeper.instance.get_data('maskName')
    if mask_name == 'None':
        mask_name = None
    text = ' '.join((jieba.lcut('\n'.join(danmaku_list))))
    create_word_cloud_image(text, _file_name=image_name, _width=image_width, _mask_name=mask_name,
                            _height=image_height, _font_name=font, _max_words=max_word_num)

    EventCenter.instance.event_trigger('WCOver')
