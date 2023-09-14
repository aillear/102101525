import csv
import codecs
import xlwt
import numpy as np
import wordcloud
from PIL import Image


def str_statistics(_str_list: list[str]):
    """
    字符串列表去重，统计同一字符串的数量，返回元组(str, int)的列表
    :param _str_list: 待处理的字符串列表
    :return: 处理后的元组列表
    """
    dic = {}
    for _str in _str_list:
        if _str in dic:
            dic[_str] += 1
        else:
            dic[_str] = 1
    # 直接在这里排个序
    res_list = sorted(dic.items(), key=lambda x: x[1], reverse=True)
    return res_list


def list2csv(_list: list[tuple[str, int]], _file_name: str):
    """
    把列表保存到CSV里,
    :param _list: 列表
    :param _file_name: 保存的文件名
    :return: None
    """
    _file_name += '.csv'
    with codecs.open(f"danmaku_data/{_file_name}", 'w', encoding='utf-8-sig') as file:
        writer = csv.writer(file)
        for info in _list:
            writer.writerow(info)
    print(f"保存为./DanmakuData/{_file_name}")


def list2excel(_list: list[tuple[str, int]], _file_name: str):
    """
    把列表保存到Excel里,保存条数有限不使用
    :param _list:
    :param _file_name:
    :return:
    """
    workbook = xlwt.Workbook()
    worksheet = workbook.add_sheet("Danmaku List")
    _file_name += '.xls'
    for i in range(len(_list)):
        worksheet.write(i, 1, _list[i][0])
        worksheet.write(i, 0, _list[i][1])

    workbook.save(f"danmaku_data/{_file_name}")
    print(f"保存为./danmaku_data/{_file_name}.")


def transform_mask(image):
    # 把图片转换成灰度模式
    image = image.convert("L")
    # 获取图片的像素值
    pixels = image.load()
    # 创建一个空的二维数组，大小和图片一样
    mask = np.zeros((image.size[1], image.size[0]), dtype=np.uint8)
    # 遍历图片的每个像素点
    for i in range(image.size[1]):
        for j in range(image.size[0]):
            # 如果像素值小于200（表示是黑色或深色），就把对应的数组元素设为0
            if pixels[j, i] < 200:
                mask[i, j] = 0
            else:
                mask[i, j] = 255
    # 返回二维数组
    return mask


def create_word_cloud_image(_content: str, _file_name: str, _max_words=100, _width=1000, _height=1000,
                            _mask_name=None, _font_name='default.ttc'):
    """
    生成词云图
    :param _content: 内容
    :param _file_name: 生成的图片名
    :param _max_words: 显示的最大词
    :param _width: 宽
    :param _height: 高
    :param _mask_name: 遮罩名（请放在ImageMask里。），默认为空
    :param _font_name: 字体名，默认为雅黑
    :return: None
    """
    # 不需要的介词等等。
    garbage_words = ['的', '了', '是', '咯', '呀', '在', '你', '我', '他', '她', '也', '就', '这', '都', '吗', '那', '哪']

    if _mask_name is None:
        image_mask = None
    else:
        image = Image.open(f"image_masks/{_mask_name}")
        image_mask = transform_mask(image)

    wc = wordcloud.WordCloud(font_path=f"fonts/{_font_name}",
                             mask=image_mask,
                             max_words=_max_words,
                             width=_width,
                             height=_height,
                             stopwords=garbage_words,
                             background_color='white',
                             collocations=False).generate(_content)
    wc.to_file(f"word_cloud_image/{_file_name}.png")
    print(f"图片保存为./word_cloud_image/{_file_name}.png")
