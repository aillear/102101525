import os


# 定义一个函数，用于获取目录下的所有文件名，并返回一个元组
def GetFileName(dir_path, extensions=('ALL_FILE_EXTENSION',), _add_default=False):
    """
    得到某个路径下指定后缀的所有文件名(带后缀), 以元组返回
    :param dir_path: 指定路径
    :param extensions: 后缀元组, 需要为全小写且带., 如.txt
    :param _add_default: 是否添加默认元素 'None'
    :return: 字符串元组
    """
    # 定义一个空列表，用于存储文件名
    _names = []
    if _add_default:
        _names.append('None')
    # 获取指定目录下的所有文件和目录的列表
    for path in os.listdir(dir_path):
        # 判断当前元素是否是文件
        if os.path.isfile(os.path.join(dir_path, path)):
            # 获取后缀,只返回匹配后缀的文件名集合
            filename, file_extension = os.path.splitext(os.path.join(dir_path, path))
            # 都转化为小写进行匹配
            file_extension = file_extension.lower()
            # 如果不指定后缀,那么匹配任何文件
            if 'ALL_FILE_EXTENSION' in extensions or file_extension in extensions:
                # 将文件名添加到列表中
                _names.append(path)
    # 将列表转换为元组，并返回
    return tuple(_names)


if __name__ == '__main__':
    # 调用函数，传入一个目录路径
    file_names = GetFileName('../Fonts')
    # 打印结果
    print(file_names)
