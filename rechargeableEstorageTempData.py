import generalmethod as gm
import infohandle as ifo


def chargeableStorageTemData(data):
    print(data)
    subsystem_num = data[0]
    subsystem_num = gm.hex_list2dex_int(subsystem_num)
    startIndex = 1
    index = 2
    endIndex = 3 + gm.hex_list2dex_int(data[index:index + 2]) + 1
    data_list = []
    string = ''
    for i in range(subsystem_num):
        data_list.append(data[startIndex:endIndex])
        string += dataAnalyze(data_list[i])
        startIndex = endIndex
        if i < subsystem_num - 1:
            index = startIndex + 1
            endIndex = startIndex + 9 + gm.hex_list2dex_int(data[index:index + 1]) * 2 + 1
    body = data[endIndex - 1:]
    body_len = len(body)
    if body_len == 1:
        return string + '\n'
    else:
        flag = ifo.getInfoType(body[1])
        string += f'信息类型标志:{flag}\n'
        body = body[2:]
        string_next = ifo.infoHandle(flag, body)
        return string + string_next


def dataAnalyze(data):
    subsystem_sn = data[0]
    subsystem_sn = getSubSystemSn(subsystem_sn)
    chargeTemProbe_num = data[1:3]
    chargeTemProbe_num = getChargeTemProbeNum(chargeTemProbe_num)
    perProbeTem = data[3:]
    perProbeTem = getPerProbeTem(perProbeTem, int(chargeTemProbe_num))
    string = f"可充电储能子系统号:{subsystem_sn}\n" \
             f"可充电储能温度探针个数:{chargeTemProbe_num}\n" \
             f"可充电储能子系统各温度探针检测到的温度值:\n{perProbeTem}\n"
    return string


# 可充电储能子系统号
def getSubSystemSn(data):
    data = gm.hex_list2dex_int(data)
    return f"{data}"


def getChargeTemProbeNum(data):
    data = gm.hex_list2dex_int(data)
    return f"{data}"


def getPerProbeTem(data, num):
    string = ''

    def getTem(per_data):
        tem = gm.hex_list2dex_int(per_data) - 40
        return f"{tem}°C"

    for i in range(num):
        string += f"第{i + 1}个温度探针的温度为{getTem(data[i])}\n"

    return string
