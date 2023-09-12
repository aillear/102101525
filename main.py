import jieba
from MainWork import DataCollector, CSVhandler, DataAnalyst, Visualizor

danmaku_list = DataCollector.DataCollect("原神", 1)
if len(danmaku_list) > 0:
    res_list = DataAnalyst.StrStatistics(danmaku_list)
    print("前20的弹幕")
    for i in range(20):
        print(res_list[i])
    CSVhandler.List2Excel(res_list, 'test.xls')
    text = ' '.join(jieba.lcut('\n'.join(danmaku_list)))
    Visualizor.CreateWordCloudImage(text, _file_name='test.png', _width=1000, _height=1000, _mask_name='OIG.jpg')
