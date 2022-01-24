import generalmethod as gm
import infohandle as ifo


def chargeableStorageVData(data):
    subSystem_num = data[0]  # 可充电储能子系统个数
    subSystem_num = gm.hex_list2dex_int(subSystem_num)
    startIndex = 1
    index = 10
    endIndex = 10 + gm.hex_list2dex_int(data[index]) * 2 + 1
    data_list = []
    string = ''
    for i in range(subSystem_num):
        data_list.append(data[startIndex:endIndex])
        string += dataAnalyze(data_list[i])
        startIndex = endIndex
        if i < subSystem_num - 1:
            index = startIndex + 9
            endIndex = startIndex + 9 + gm.hex_list2dex_int(data[index]) * 2 + 1
    body = data[endIndex - 1:]
    body_len = len(body)
    if body_len == 1:
        return string
    else:
        flag = ifo.getInfoType(body[1])
        string += f'信息类型标志:{flag}\n'
        body = body[2:]
        string_next = ifo.infoHandle(flag, body)
        return string + string_next


# 分许
def dataAnalyze(data):
    subsystemSn = data[0]
    subsystemSn = getSubSystemSn(subsystemSn)
    chargeableV = data[1:3]
    chargeableV = getChargeableV(chargeableV)
    chargeableI = data[3:5]
    chargeableI = getChargeableI(chargeableI)
    perBatNum = data[5:7]
    perBatNum = getPerBatNum(perBatNum)
    perFrmBatSn = data[7:9]
    perFrmBatSn = getFrmPerBatStartSN(perFrmBatSn)
    perFrmBatNum = data[9]
    perFrmBatNum = getFrmPerBatNum(perFrmBatNum)
    perBatV = data[10:]
    perBatV = getPerBatV(perBatV, int(perFrmBatNum))
    string = f"可充电储能子系统号:{subsystemSn}\n" \
             f"可充电储能装置电压:{chargeableV}\n" \
             f"可充电储能装置电流:{chargeableI}\n" \
             f"单体电池总数:{perBatNum}\n" \
             f"本帧起始电池序号:{perFrmBatSn}\n" \
             f"本帧单体电池总数:{perFrmBatNum}\n" \
             f"单体电池电压:\n{perBatV}\n"
    return string


# 可充电储能子系统号
def getSubSystemSn(data):
    data = gm.hex_list2dex_int(data)
    return f"{data}"


# 可充电储能装置电压
def getChargeableV(data):
    data = gm.hex_list2dex_int(data)
    if data == gm.hex_list2dex_int('FF FE'):
        return '异常'
    elif data == gm.hex_list2dex_int('FF FF'):
        return '无效'
    else:
        data = data * 0.1
        return f"{data}V"


# 可充电储能装置电流
def getChargeableI(data):
    data = gm.hex_list2dex_int(data)
    if data == gm.hex_list2dex_int('FF FE'):
        return '异常'
    elif data == gm.hex_list2dex_int('FF FF'):
        return '无效'
    else:
        data = data * 0.1 - 1000
        return f"{data}A"


#  单体电池总数
def getPerBatNum(data):
    data = gm.hex_list2dex_int(data)
    if data == gm.hex_list2dex_int('FF FE'):
        return '异常'
    elif data == gm.hex_list2dex_int('FF FF'):
        return '无效'
    else:
        return f"{data}"


#  本帧率起始电池序号
def getFrmPerBatStartSN(data):
    data = gm.hex_list2dex_int(data)
    return f"{data}"


#  本帧单体电池总数
def getFrmPerBatNum(data):
    data = gm.hex_list2dex_int(data)
    return f"{data}"


#  单体电池电压
def getPerBatV(data, num):
    startIndex = 0
    endIndex = 2
    string = ''

    def getV(data_l):
        data_l = gm.hex_list2dex_int(data_l) * 0.001
        return f"{data_l}V"

    for i in range(num):
        data_list = data[startIndex:endIndex]
        perV = getV(data_list)
        string += f"第{i + 1}个电池电压为:{perV}\n"
        if i < num - 1:
            startIndex += 2
            endIndex += 2
    return string
