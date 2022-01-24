import infohandle as ifo
import generalmethod as gm


# 燃料电池数据格式
def fuelBatDataFormat(data):
    fuelBatV = data[0:2]  # 燃料电池电压
    fuelBatV = getFuelBatV(fuelBatV)  # 获取燃料电池电压

    fuelBatI = data[2:4]  # 燃料电池电流
    fuelBatI = getFuelBatI(fuelBatI)  # 获取燃料电池电流

    fuelConsumeRate = data[4:6]  # 燃料消耗率
    fuelConsumeRate = getFuelConsumeRate(fuelConsumeRate)  # 获取燃料消耗率

    fuelBatTempProbe_n = data[6:8]  # 燃料电池温度探针总数
    fuelBatTempProbe_n = getFuelBatTemProbe_num(fuelBatTempProbe_n)  # 获取燃料电池温度探针总数

    startIndex = 8  # 起始索引
    endIndex = 8 + 1 + fuelBatTempProbe_n  # 终止索引
    if fuelBatTempProbe_n != 0:
        probeTemList = data[startIndex, endIndex]  # 温度探针列表
        perProbeTempInfo = getPerProbeTem(probeTemList, fuelBatTempProbe_n)
    else:
        probeTemList = []
        perProbeTempInfo = '温度探针值为空'

    startIndex = endIndex
    endIndex += 2

    H_systemMaxTemp = data[startIndex:endIndex]
    H_systemMaxTemp = getHSystemMaxTem(H_systemMaxTemp)

    H_systemMaxTempProbe_num = data[endIndex]
    H_systemMaxTempProbe_num = getHSystemMaxTemNum(H_systemMaxTempProbe_num)

    startIndex = endIndex + 1
    endIndex = startIndex + 2

    H_systemMax_CONC = data[startIndex, endIndex]
    H_systemMax_CONC = getHSystemMaxCONC(H_systemMax_CONC)

    H_systemMax_CONC_sensor_n = data[endIndex]
    H_systemMax_CONC_sensor_n = getHSystemMaxCONCSensor_n(H_systemMax_CONC_sensor_n)

    startIndex = endIndex + 1
    endIndex = startIndex + 2

    H_MaxPressure = data[startIndex, endIndex]
    H_MaxPressure = getHSystemMaxPressure(H_MaxPressure)

    H_MaxPressure_sensor_n = data[endIndex]
    H_MaxPressure_sensor_n = getHSystemMaxPressureSensor_n(H_MaxPressure_sensor_n)

    endIndex += 1
    HPressure_dcState = data[endIndex]
    HPressure_dcState = getDcState(HPressure_dcState)

    string = f'\n燃料电池电压:{fuelBatV}\n' \
             f'燃料电池电流:{fuelBatI}\n' \
             f'燃料消耗率:{fuelConsumeRate}\n' \
             f'燃料电池温度探针总数{fuelBatTempProbe_n}\n' \
             f'探针温度值:{perProbeTempInfo}\n' \
             f'氢系统中最高温度:{H_systemMaxTemp}\n' \
             f'氢系统中最高温度探针代号:{H_systemMaxTempProbe_num}\n' \
             f'氢系统最高浓度:{H_systemMax_CONC}\n' \
             f'氢气最高浓度传感器代号:{H_systemMax_CONC_sensor_n}\n' \
             f'氢气最高压力:{H_MaxPressure}\n' \
             f'氢气最高压力传感器代号:{H_MaxPressure_sensor_n}\n' \
             f'高压DC/DC状态:{HPressure_dcState}\n'

    body = data[endIndex:]
    body_len = len(body)
    if body_len == 1:
        return string
    else:
        flag = ifo.getInfoType(body[1])
        body = body[2:]
        string_next = ifo.infoHandle(flag, body)
        return string + string_next


def getFuelBatV(data):
    data = gm.hex_list2dex_int(data)
    if data == gm.hex_list2dex_int('FF FE'):
        return '异常'
    if data == gm.hex_list2dex_int('FF FF'):
        return '无效'
    else:
        data = data * 0.1
        return f'{data} V'


def getFuelBatI(data):
    data = gm.hex_list2dex_int(data)
    if data == gm.hex_list2dex_int('FF FE'):
        return '异常'
    if data == gm.hex_list2dex_int('FF FF'):
        return '无效'
    else:
        data = data * 0.1
        return f'{data} A'


def getFuelConsumeRate(data):
    data = gm.hex_list2dex_int(data)
    if data == gm.hex_list2dex_int('FF FE'):
        return '异常'
    if data == gm.hex_list2dex_int('FF FF'):
        return '无效'
    else:
        data = data * 0.01
        return f'{data} kg/100km'


def getFuelBatTemProbe_num(data):
    data = gm.hex_list2dex_int(data)
    if data == gm.hex_list2dex_int('FF FE'):
        return '异常'
    if data == gm.hex_list2dex_int('FF FF'):
        return '无效'
    else:
        return f'{data}'


#  获取每个探针的温度值
def getPerProbeTem(data, num):
    string = ''

    def getTem(data_l):
        temperature = gm.hex_list2dex_int(data_l) - 40
        return f"{temperature}°C"

    for i in num:
        temp = getTem(data[i])
        string += f'第{i + 1}个温度探针温度:{temp}\n'

    return string


#  氢系统中最高温度
def getHSystemMaxTem(data):
    data = gm.hex_list2dex_int(data)
    if data == gm.hex_list2dex_int('FF FE'):
        return '异常'
    if data == gm.hex_list2dex_int('FF FF'):
        return '无效'
    else:
        data = data * 0.1 - 40
        return f'{data}°C'


#  氢系统的最高温度探针代号
def getHSystemMaxTemNum(data):
    data = gm.hex_list2dex_int(data)
    if data == gm.hex_list2dex_int('FE'):
        return '异常'
    if data == gm.hex_list2dex_int('FF'):
        return '无效'
    else:
        return f'{data}'


#  氢气最高浓度
def getHSystemMaxCONC(data):
    data = gm.hex_list2dex_int(data)
    if data == gm.hex_list2dex_int('FF FE'):
        return '异常'
    if data == gm.hex_list2dex_int('FF FF'):
        return '无效'
    else:
        return f'{data} mg/kg'


#  氢系统中最高浓度传感器代号
def getHSystemMaxCONCSensor_n(data):
    data = gm.hex_list2dex_int(data)
    if data == gm.hex_list2dex_int('FE'):
        return '异常'
    if data == gm.hex_list2dex_int('FF'):
        return '无效'
    else:
        return f'{data}'


#  氢气最高压力
def getHSystemMaxPressure(data):
    data = gm.hex_list2dex_int(data) * 0.1
    return f'{data} MPa'


#  氢气最高压力传感器代号
def getHSystemMaxPressureSensor_n(data):
    data = gm.hex_list2dex_int(data)
    if data == gm.hex_list2dex_int('FE'):
        return '异常'
    if data == gm.hex_list2dex_int('FF'):
        return '无效'
    else:
        return f'{data}'


#  高压 DC/DC 状态
def getDcState(data):
    if data == '01':
        return '工作'
    elif data == '02':
        return '断开'
    elif data == 'FE':
        return '异常'
    elif data == 'FF':
        return '无效'
    else:
        return '数据异常'
