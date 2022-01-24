import generalmethod as gm

'''此模块用于获取数据包结构定义'''


#  获取命令标识定义
def getCommand(key):
    command_dict = {
        '01': '车辆登入',
        '02': '实时信息上报',
        '03': '补发信息上报',
        '04': '车辆登出',
        'A': '平台传输数据占用',
        '07': '心跳',
        '08': '终端校时',
        'B': '上行数据系统预留',
        '80': '查询命令',
        '81': '设置命令',
        '82': '车载终端控制命令',
        'C': '下行数据系统预留',
        'D': '平台交换自定义数据',
    }
    if key in command_dict:
        return command_dict[key]
    else:
        if int('05', 16) <= int(key, 16) <= int('06', 16):
            return command_dict['A']
        elif int('09', 16) <= int(key, 16) <= int('7F', 16):
            return command_dict['B']
        elif int('83', 16) <= int(key, 16) <= int('BF', 16):
            return command_dict['C']
        elif int('C0', 16) <= int(key, 16) <= int('FE', 16):
            return command_dict['D']
        else:
            return '命令标识数据错误'


# 获取命令标识定义
def getMLbs(key):
    bs_dict = {
        '01': '  定义:车辆登入  方向:上行  ',
        '02': '  定义:实时信息上报  方向:上行',
        '03': '  定义:补发信息上报  方向:上行',
        '04': '  定义:车辆登出  方向:上行',
        'A': '  定义:平台传输数据占用  方向:自定义',
        '07': '  定义:心跳  方向:上行',
        '08': '  定义:终端校时  方向:上行',
        'B': '  定义:上行数据系统预留  方向:上行',
        '80': '  定义:查询命令  方向:下行',
        '81': '  定义:设置命令  方向:下行',
        '82': '车载终端控制命令',
        'C': '  定义:下行数据系统预留  方向:下行',
        'D': '  定义:平台交换自定义数据  方向:自定义',
    }
    if key in bs_dict:
        return bs_dict[key]
    else:
        if int('05', 16) <= int(key, 16) <= int('06', 16):
            return bs_dict['A']
        elif int('09', 16) <= int(key, 16) <= int('7F', 16):
            return bs_dict['B']
        elif int('83', 16) <= int(key, 16) <= int('BF', 16):
            return bs_dict['C']
        elif int('C0', 16) <= int(key, 16) <= int('FE', 16):
            return bs_dict['D']
        else:
            return '命令标识数据有误'


# 获取应答标志定义
def getYDbz(key):
    yd_dict = {
        '01': '  定义:成功 说明:接收到的信息正确  ',
        '02': '  定义:错误 说明:设置未成功',
        '03': '  定义:VIN重复 说明:VIN重复错误',
        'FE': '  定义:命令 说明:表示数据包为命令包，而非应答包',
    }
    if key in yd_dict:
        return yd_dict[key]
    else:
        return '应答标志错误'


# 获取数据长度
def get_data_len(data_len):
    data_len = gm.hex_list2dex_int(data_len)
    return f' 长度为{data_len}字节 '


def get_encrypting_method():
    pass
