import generalmethod as gm
import infohandle as ifo


def alarmData(data):
    highestAlarmLv = data[0]  # 最高报警等级
    highestAlarmLv = getHighestAlarmLv(highestAlarmLv)

    gnrAlarmFlag = data[1:5]  # 通用报警标志
    print(f"通用报警标志{gnrAlarmFlag}")
    gnrAlarmFlag = getGnrAlarmFlag(gnrAlarmFlag)
    print(gnrAlarmFlag)

    CDeviceFault_num = data[5]  # 可充电储能装置故障总数N1
    CDeviceFault_num = gm.hex_list2dex_int(CDeviceFault_num)
    endIndex = 6
    if CDeviceFault_num != 0:
        endIndex = 6 + CDeviceFault_num + 1
        CDeviceFault_list = data[6:endIndex]
    else:
        CDeviceFault_list = []

    motorFault_num = data[endIndex]  # 驱动电机故障总数
    motorFault_num = gm.hex_list2dex_int(motorFault_num)
    startIndex = endIndex + 1

    if motorFault_num != 0:
        endIndex += (motorFault_num + 1)
        motorFault_list = data[startIndex:endIndex]
    else:
        motorFault_list = []
        endIndex += 1

    engineFault_num = data[endIndex]  # 发动机故障总数
    engineFault_num = gm.hex_list2dex_int(engineFault_num)

    startIndex = endIndex + 1

    if engineFault_num != 0:
        endIndex += (engineFault_num + 1)
        engineFault_list = data[startIndex, endIndex]

    else:
        engineFault_list = []
        endIndex += 1
    print(endIndex)
    otherFault_num = data[endIndex]  # 其他故障总数
    otherFault_num = gm.hex_list2dex_int(otherFault_num)

    startIndex = endIndex + 1

    if otherFault_num != 0:
        endIndex = (otherFault_num + 1)
        otherFault_list = data[startIndex, endIndex]
    else:
        otherFault_list = []

    string = f'最高报警等级:{highestAlarmLv}\n' \
             f'通用报警标志:\n{gnrAlarmFlag}' \
             f'可充电储能装置故障总数:{CDeviceFault_num}\n' \
             f'可充电储能装置故障代码列表:{CDeviceFault_list}\n' \
             f'驱动电机故障总数:{motorFault_num}\n' \
             f'驱动电机故障代码列表:{motorFault_list}\n' \
             f'发动机故障总数:{engineFault_num}\n' \
             f'发动机故障列表:{engineFault_list}\n' \
             f'其他故障总数:{otherFault_num}\n' \
             f'其他故障代码列表:{otherFault_list}\n\n'

    body = data[endIndex:]
    body_len = len(body)
    if body_len == 1:
        return string
    else:
        flag = ifo.getInfoType(body[1])
        string += f'信息类型标志:{flag}\n'
        body = body[2:]
        string_next = ifo.infoHandle(flag, body)
        return string + string_next


# 最高报警等级
def getHighestAlarmLv(data):
    data = gm.hex_list2dex_int(data)
    if data == 'FE':
        return '异常'
    elif data == 'FF':
        return '无效'
    elif data == 0:
        return '无故障'
    elif data == 1:
        return '1级故障 不影响车辆正常行驶'
    elif data == 2:
        return '2级故障 影响车辆性能，需驾驶员限制行驶'
    elif data == 3:
        return '3级故障 驾驶员应立即停车处理或请求救援'


# 通用报警标志
def getGnrAlarmFlag(data):
    data0 = gm.hex_list2dex_int(data[0])
    data0 = "{:08b}".format(data0)
    data1 = gm.hex_list2dex_int(data[1])
    data1 = "{:08b}".format(data1)
    data2 = gm.hex_list2dex_int(data[2])
    data2 = "{:08b}".format(data2)
    data3 = gm.hex_list2dex_int(data[3])
    data3 = "{:08b}".format(data3)
    data = data0 + data1 + data2 + data3

    if data[-1] == '0':
        a = '(温度差异)正常不报警\n'
    else:
        a = '温度差异报警\n'

    if data[-2] == '0':
        b = '(电池高温)正常不报警\n'
    else:
        b = '电池高温报警'

    if data[-3] == '0':
        c = '(车载储能装置类型过压)正常不报警\n'
    else:
        c = '车载储能装置类型过压报警\n'

    if data[-4] == '0':
        d = '(车载储能装置类型欠压)正常不报警\n'
    else:
        d = '车载储能装置类型欠压报警\n'

    if data[-5] == '0':
        e = '(SOC低)正常不报警\n'
    else:
        e = 'SOC低报警\n'

    if data[-6] == '0':
        f = '(单体电池过压)正常不报警\n'
    else:
        f = '单体电池过压报警\n'

    if data[-7] == '0':
        g = '(单体电池欠压)正常不报警\n'
    else:
        g = '单体电池欠压报警\n'

    if data[-8] == '0':
        h = '(SOC过高)正常不报警\n'
    else:
        h = 'SOC过高报警\n'

    if data[-9] == '0':
        i = '(SOC跳变)正常不报警\n'
    else:
        i = 'SOC跳变报警\n'

    if data[-10] == '0':
        j = '(可充电储能系统不匹配)正常不报警\n'
    else:
        j = '可充电储能系统不匹配报警\n'

    if data[-11] == '0':
        k = '(电池单体一致性差)正常不报警\n'
    else:
        k = '(电池单体一致性差)报警\n'

    if data[-12] == '0':
        l = '(绝缘)正常不报警\n'
    else:
        l = '绝缘报警\n'

    if data[-13] == '0':
        m = '(DC-DC温度)正常不报警\n'
    else:
        m = 'DC-DC温度报警\n'

    if data[-14] == '0':
        n = '(制动系统)正常不报警\n'
    else:
        n = '制动系统报警\n'

    if data[-15] == '0':
        o = '(DC-DC状态）正常不报警\n'
    else:
        o = 'DC-DC状态报警\n'

    if data[-16] == '0':
        p = '(驱动电机控制器温度)正常不报警\n'
    else:
        p = '驱动电机控制器温度报警\n'

    if data[-17] == '0':
        q = '(高压互锁状态)正常不报警\n'
    else:
        q = '高压互锁状态报警\n'

    if data[-18] == '0':
        r = '(驱动电机温度)正常不报警\n'
    else:
        r = '驱动电机温度报警\n'

    if data[-19] == '0':
        s = '(车载储能装置类型过充)正常不报警\n'
    else:
        s = '车载储能装置类型过充\n'

    return a + b + c + d + e + f + g + h + i + j + k + l + m + n + o + p + q + r + s
