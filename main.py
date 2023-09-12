import jieba
from MainWork import DataCollector, CSVhandler, DataAnalyst, Visualizor


def main():
    keyword = input('输入搜索关键词:\n')
    video_count = None
    try:
        video_count = int(input('输入爬取的视频数量:\n'))
    except ValueError:
        print('输入非法!')
        return

    danmaku_list = DataCollector.DataCollect(keyword, video_count)
    if len(danmaku_list) <= 0:
        return

    res_list = DataAnalyst.StrStatistics(danmaku_list)
    str_len = len(res_list) if len(res_list) < 20 else 20
    print(f"前{str_len}的弹幕")
    for i in range(str_len):
        print(res_list[i])
    CSVhandler.List2CSV(res_list, 'test')
    text = ' '.join(jieba.lcut('\n'.join(danmaku_list)))
    Visualizor.CreateWordCloudImage(text, _file_name='test.png', _width=1000, _height=1000, _mask_name='OIG.jpg')


if __name__ == '__main__':
    main()
