import csv
import codecs
import xlwt


def List2CSV(_list: list[tuple[str, int]], _file_name: str):
    """
    把列表保存到CSV里,
    :param _list: 列表
    :param _file_name: 保存的文件名
    :return: None
    """
    _file_name += '.csv'
    with codecs.open(f"DanmakuData/{_file_name}", 'w', encoding='utf-8-sig') as file:
        writer = csv.writer(file)
        for info in _list:
            writer.writerow(info)
    print(f"保存为./DanmakuData/{_file_name}")


def List2Excel(_list: list[tuple[str, int]], _file_name: str):
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

    workbook.save(f"DanmakuData/{_file_name}")
    print(f"保存为./DanmakuData/{_file_name}.")
