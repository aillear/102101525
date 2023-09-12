import os


# 定义一个函数，用于获取目录下的所有文件名，并返回一个元组
def GetFileName(dir_path, _add_default=False):
    # 定义一个空列表，用于存储文件名
    _names = []
    if _add_default:
        _names.append('None')
    # 获取指定目录下的所有文件和目录的列表
    for path in os.listdir(dir_path):
        # 判断当前元素是否是文件

        if os.path.isfile(os.path.join(dir_path, path)):
            # 将文件名添加到列表中
            _names.append(path)
    # 将列表转换为元组，并返回
    return tuple(_names)


if __name__ == '__main__':
    # 调用函数，传入一个目录路径
    file_names = GetFileName('../Fonts')
    # 打印结果
    print(file_names)
