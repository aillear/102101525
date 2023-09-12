import numpy as np
import wordcloud
from PIL import Image


# 定义一个函数，把图片转换成二维数组，表示图片的形状
def transformMask(image):
    # 把图片转换成灰度模式
    image = image.convert("L")
    # 获取图片的像素值
    pixels = image.load()
    # 创建一个空的二维数组，大小和图片一样
    mask = np.zeros((image.size[1], image.size[0]), dtype=np.uint8)
    # 遍历图片的每个像素点
    for i in range(image.size[1]):
        for j in range(image.size[0]):
            # 如果像素值小于200（表示是黑色或深色），就把对应的数组元素设为255（表示是白色）
            if pixels[j, i] < 200:
                mask[i, j] = 0
            else:
                mask[i, j] = 255
    # 返回二维数组
    return mask


def CreateWordCloudImage(_content: str, _file_name: str, _max_words=100, _width=1000, _height=1000,
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
        image = Image.open(f"ImageMasks/{_mask_name}")
        image_mask = transformMask(image)

    wc = wordcloud.WordCloud(font_path=f"Fonts/{_font_name}",
                             mask=image_mask,
                             max_words=_max_words,
                             width=_width,
                             height=_height,
                             stopwords=garbage_words,
                             background_color='white',
                             collocations=False).generate(_content)
    wc.to_file(f"WordCloudImage/{_file_name}")
    print(f"图片保存为./WordCloudImage/{_file_name}")
