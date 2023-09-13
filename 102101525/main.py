import jieba
from MainWork import DataCollector, CSVhandler, DataAnalyst, Visualizor
import cProfile


def main():
    """
    对于非GUI版,仅仅做了简单的参数选择.
    可以自己手动修改参数
    :return:
    """
    keyword = input('输入搜索关键词:\n')
    video_count = None
    try:
        video_count = int(input('输入爬取的视频数量:\n'))
    except ValueError:
        print('输入非法!')
        return

    danmaku_save_name = 'danmaku_list'  # 保存的弹幕文件名
    wordcloud_save_name = 'WCimage'     # 保存的词云图片文件名
    font_name = 'default.ttc'           # 字体文件名, 需要带后缀
    mask_name = None                    # 图片遮罩, 为None则不启用遮罩. 遮罩需要带后缀, 如: default.png
    width = 1000                        # 词云图片宽度, 如果启用 mask_name 则不生效
    height = 1000                       # 词云图片高度, 如果启用 mask_name 则不生效

    # 获取弹幕列表, 检查是否不存在弹幕
    danmaku_list = DataCollector.DataCollect(keyword, video_count)
    if len(danmaku_list) <= 0:
        return

    # 弹幕列表去重统计, 检查是否去重之后不足20条
    res_list = DataAnalyst.StrStatistics(danmaku_list)
    str_len = len(res_list) if len(res_list) < 20 else 20
    print(f"前{str_len}的弹幕")
    for i in range(str_len):
        print(res_list[i])

    # 保存成csv
    CSVhandler.List2CSV(res_list, danmaku_save_name)
    text = ' '.join(jieba.lcut('\n'.join(danmaku_list)))
    # 可视化
    Visualizor.CreateWordCloudImage(text, _file_name=wordcloud_save_name, _width=width, _height=height,
                                    _mask_name=mask_name, _font_name=font_name)


if __name__ == '__main__':
    main()
