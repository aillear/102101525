import csv
import codecs


def List2CSV(_list: list[tuple[str, int]], _file_name: str):
    """
    把列表保存到CSV里
    :param _list: 列表
    :param _file_name: 保存的文件名
    :return: None
    """
    with codecs.open(f"DanmakuData/{_file_name}", 'w', encoding='utf-8-sig') as file:
        writer = csv.writer(file)
        for info in _list:
            writer.writerow(info)
    print(f"保存为{_file_name}.")
