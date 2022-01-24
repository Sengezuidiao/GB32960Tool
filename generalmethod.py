import binascii


# 十六进制列表转字符串
def list2str(data):
    data = " ".join(data)
    return data


# 十六进制转ascii字符
def lhex2Ascii(hex_data):
    hex_data = "".join(hex_data)
    hex_data = hex_data.replace(" ", "")

    ascii_out = binascii.a2b_hex(hex_data)
    ascii_out = str(ascii_out, encoding='utf-8')
    return ascii_out


# 十六进制列表转10进制返回整型
def hex_list2dex_int(hex_data):
    hex_data = "".join(hex_data)
    hex_data = hex_data.replace(" ", "")
    d = int(hex_data, 16)
    return d


# 十六进制列表转10进制返回字符串
def listH2StrD(hex_data):
    hex_data = "".join(hex_data)
    hex_data = hex_data.replace(" ", "")
    d = int(hex_data, 16)
    d = str(d)
    return d


# 16进制时间格式化输出
def listTime2Dec(data_collect_time):
    clt_time = f"{int(data_collect_time[0], 16)}年{int(data_collect_time[1], 16)}月{int(data_collect_time[2], 16)}日" \
               f"{int(data_collect_time[3], 16)}时{int(data_collect_time[4], 16)}分{int(data_collect_time[5], 16)}秒"
    return clt_time


# 获取加密方式
def getJMfs(key):
    jiami_dict = {
        '01': ' 描述:数据不加密 ',
        '02': ' 描述:数据经过RSA算法加密 ',
        '03': ' 描述:数据经过AES128位算法加密 ',
        'FE': ' 描述:异常 ',
        'FF': ' 描述:无效 ',
    }
    if key in jiami_dict:
        return jiami_dict[key]
    else:
        return ' 描述: 预留'


# 十进制转八位二进制，并倒置
def dec2bin_reverse(data):
    data = str(data)
    data = int(data, base=16)
    data = "{:08b}".format(data)
    list1 = []
    for i in data:
        list1.append(i)
    list1.reverse()
    data = "".join(list1)
    return data


#  十六进制转换成解析数据
def get_value_from_original(
        original_data: list = None,
        unit: str = '',
        extre_num=None,
        accuracy=1.0,
        spacial_value_dict: dict = None,
        return_type='value',
        offset=0.0,
):
    """
    返回值类型:
    value 算出具体值
    ASCII 返回字符串
    time 返回时间
    比特序列
    :type offset: float
    :type extre_num: tuple
    :type return_type: str
    :type accuracy: float
    :type spacial_value_dict: float
    :type original_data: list
    :type unit: str
    """

    if not isinstance(original_data, list):
        raise TypeError
    if spacial_value_dict is not None:
        data = list2str(original_data)
        for key, value in spacial_value_dict.items():
            if isinstance(key, str):
                if data == key:
                    return value
            elif isinstance(key, tuple):
                if int(key[0], 16) <= int(data, 16) <= int(key[1], 16):
                    return value
    if return_type == 'value':
        data = hex_list2dex_int(original_data)
        if extre_num is not None:
            if len(extre_num) == 2:
                if extre_num[0] <= data <= extre_num[1]:
                    print(offset)
                    data = data * accuracy - offset
        else:
            data = data + offset
        return f"{data} {unit}"
    if return_type == 'time':
        return


confdict = {('10', '90'): "hello"}
a = get_value_from_original(['80'], accuracy=0.1, unit="V", offset=-20.0)
print(a)
