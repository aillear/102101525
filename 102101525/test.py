from MainWork import DataCollector, CSVhandler, Visualizor
import cProfile

danmaku_list = DataCollector.data_collect("原神", 1)
if len(danmaku_list) > 0:
    res_list = None
    text = None
    # 对DataAnalyst.str_statistics(danmaku_list)函数进行性能分析
    cProfile.run('res_list = DataAnalyst.str_statistics(danmaku_list)')
    str_len = len(res_list) if len(res_list) < 20 else 20
    print(f"前{str_len}的弹幕")
    for i in range(str_len):
        print(res_list[i])
    CSVhandler.list2csv(res_list, 'test')
    # 对text = ' '.join(jieba.lcut('\n'.join(danmaku_list)))语句进行性能分析
    cProfile.run('text = \' \'.join(jieba.lcut(\'\\n\'.join(danmaku_list)))')
    Visualizor.create_word_cloud_image(text, _file_name='test.png', _width=1000, _height=1000, _mask_name='OIG.jpg')
