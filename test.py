import jieba
import DataAnalyst
import DataCollector
import Visualizor
import CSVhandler

danmaku_list = DataCollector.DataCollect("日本核污染水排海", 1)
res_list = DataAnalyst.StrStatistics(danmaku_list)
print("前20的弹幕")
for i in range(20):
    print(res_list[i])
CSVhandler.List2CSV(res_list, 'test.csv')
text = ' '.join(jieba.lcut('\n'.join(danmaku_list)))
Visualizor.CreateWordCloudImage(text, _file_name='test.png', _width=1000, _height=1000)
