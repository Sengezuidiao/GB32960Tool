import generalmethod as gm
import infohandle as ifo


def getExtremeData(data):
    maxVSubSystem_n = data[0]
    maxVSubSystem_n = getMaxMinVBatS_n(maxVSubSystem_n)

    maxVBatPerCode = data[1]
    maxVBatPerCode = getBatPerCode(maxVBatPerCode)

    perBatMaxV = data[2:4]
    perBatMaxV = getPerBatVValue(perBatMaxV)

    minVSubSystem_n = data[4]
    minVSubSystem_n = getMaxMinVBatS_n(minVSubSystem_n)

    minVBatPerCode = data[5]
    minVBatPerCode = getBatPerCode(minVBatPerCode)

    perBatMinV = data[6:8]
    perBatMinV = getPerBatVValue(perBatMinV)

    maxTem_subsystem_n = data[8]
    maxTem_subsystem_n = getTemSubsystem_n(maxTem_subsystem_n)

    maxTemProbeSn = data[9]
    maxTemProbeSn = getTemProbeSN(maxTemProbeSn)

    maxTem = data[10]
    maxTem = getTemValue(maxTem)

    minTem_subsystem_n = data[11]
    minTem_subsystem_n = getTemSubsystem_n(minTem_subsystem_n)

    minTemProbeSn = data[12]
    minTemProbeSn = getTemProbeSN(minTemProbeSn)

    minTem = data[13]
    minTem = getTemValue(minTem)

    string = f'最高电压电池子系统号:{maxVSubSystem_n}\n' \
             f'最高电压电池单体代号:{maxVBatPerCode}\n' \
             f'电池单体电压最高值:{perBatMaxV}\n' \
             f'最低电压电池子系统号:{minVSubSystem_n}\n' \
             f'最低电压电池单体代号:{minVBatPerCode}\n' \
             f'电池单体电压最低值:{perBatMinV}\n' \
             f'最高温度子系统号:{maxTem_subsystem_n}\n' \
             f'最高温度探针序号:{maxVBatPerCode}\n' \
             f'最高温度值:{maxTem}\n' \
             f'最低温度子系统号:{minTem_subsystem_n}\n' \
             f'最低温度探针序号:{minTemProbeSn}\n' \
             f'最低温度值:{minTem} \n \n'
    body = data[13:]
    body_len = len(body)
    if body_len == 1:
        return string
    else:
        flag = ifo.getInfoType(body[1])
        string += f'信息类型标志:{flag}\n'
        body = body[2:]
        string_next = ifo.infoHandle(flag, body)
        return string + string_next


#  最高电压电池子系统号
#  最低电压电池子系统号
def getMaxMinVBatS_n(data):
    if data == 'FE':
        return '异常'
    elif data == 'FF':
        return '无效'
    else:
        data = gm.hex_list2dex_int(data)
        return f'{data}'


#  最高电压电池单体代号
#  最低电压电池单体代号
def getBatPerCode(data):
    if data == 'FE':
        return '异常'
    elif data == 'FF':
        return '无效'
    else:
        data = gm.hex_list2dex_int(data)
        return f'{data}'


#  电池单体电压最高值
#  电池单体电压最低值
def getPerBatVValue(data):
    data = gm.hex_list2dex_int(data)
    if data == gm.hex_list2dex_int('FF FE'):
        return '异常'
    elif data == gm.hex_list2dex_int('FF FF'):
        return '无效'
    else:
        data = data * 0.001
        return f"{data}V"


#  最高温度子系统号
#  最低温度子系统号
def getTemSubsystem_n(data):
    if data == 'FE':
        return '异常'
    elif data == 'FF':
        return '无效'
    else:
        data = gm.hex_list2dex_int(data)
        return f'{data}'


#  最高温度探针序号
#  最低温度探针序号
def getTemProbeSN(data):
    if data == 'FE':
        return '异常'
    elif data == 'FF':
        return '无效'
    else:
        data = gm.hex_list2dex_int(data)
        return f'{data}'


#  最高温度值
#  最低温度值
def getTemValue(data):
    if data == 'FE':
        return '异常'
    elif data == 'FF':
        return '无效'
    else:
        data = gm.hex_list2dex_int(data) - 40
        return f'{data}°C'
