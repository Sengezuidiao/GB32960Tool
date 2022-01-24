import infohandle as ifo
import generalmethod as gm


def motorData(body):
    motor_num = body[0]  # 驱动电机个数
    motor_num = gm.hex_list2dex_int(motor_num)
    total_len = 12 * motor_num
    data_list = []
    startIndex = 1
    endIndex = 13
    string = ''
    for i in range(motor_num):
        data_list.append(body[startIndex:endIndex])
        startIndex += 12
        endIndex += 12
        string += dataAnalyze(data_list[i])
    string = string + '\n'
    body = body[total_len:]
    body_len = len(body)
    if body_len == 1:
        return string
    else:
        flag = ifo.getInfoType(body[1])
        string += f'信息类型标志:{flag}\n'
        body = body[2:]
        string_next = ifo.infoHandle(flag, body)
        return string + string_next


def dataAnalyze(data):
    motorSN = data[0]
    motorSN = getMotorSN(motorSN)
    motorCtrS = data[1]
    motorCtrS = getMotorCtrState(motorCtrS)
    motorCtrTem = data[2]
    motorCtrTem = getMotorCtrTem(motorCtrTem)
    motorSpeed = data[3:5]
    motorSpeed = getMotorSpeed(motorSpeed)
    motorTorque = data[5:7]
    motorTorque = getMotorTorque(motorTorque)
    motorTem = data[7]
    motorTem = getMotorTem(motorTem)
    motorCtrV = data[8:10]
    motorCtrV = getMotorCtrV(motorCtrV)
    motorCtrI = data[10:12]
    motorCtrI = getMotorCtrI(motorCtrI)
    return f"驱动电机序号:{motorSN}\n" \
           f"驱动电机状态:{motorCtrS}\n" \
           f"驱动电机控制温度:{motorCtrTem}\n" \
           f"驱动电机转速:{motorSpeed}\n" \
           f"驱动电机转矩:{motorTorque}\n" \
           f"驱动电机温度:{motorTem}\n" \
           f"电机控制器输入电压:{motorCtrV}\n" \
           f"电机控制器直流母线电流:{motorCtrI}\n"


def getMotorSN(data):
    data = gm.hex_list2dex_int(data)
    return data


def getMotorCtrState(data):
    if data == 'FE':
        return '异常'
    elif data == 'FF':
        return '无效'
    elif data == '01':
        return '耗电'
    elif data == '02':
        return '发电'
    elif data == '03':
        return '关闭状态'
    elif data == '04':
        return '准备状态'


def getMotorCtrTem(data):
    if data == 'FE':
        return '异常'
    elif data == 'FF':
        return '无效'
    data = gm.hex_list2dex_int(data) - 40
    return f"{data}°C"


def getMotorSpeed(data):
    if data == gm.hex_list2dex_int('FF FE'):
        return '异常'
    elif data == gm.hex_list2dex_int('FF FF'):
        return '无效'
    else:
        data = gm.hex_list2dex_int(data) - 20000
        return f'{data}r/min'


# 驱动电机转矩
def getMotorTorque(data):
    if data == gm.hex_list2dex_int('FF FE'):
        return '异常'
    elif data == gm.hex_list2dex_int('FF FF'):
        return '无效'
    else:
        data = gm.hex_list2dex_int(data) - 20000
        data = data * 0.1
        return f"{data}N*m"


# 驱动电机温度
def getMotorTem(data):
    if data == 'FE':
        return '异常'
    elif data == 'FF':
        return '无效'
    else:
        data = gm.hex_list2dex_int(data) - 40
        return f"{data}°C"


# 电机控制器输入电压
def getMotorCtrV(data):
    if data == gm.hex_list2dex_int('FF FE'):
        return '异常'
    elif data == gm.hex_list2dex_int('FF FF'):
        return '无效'
    else:
        data = gm.hex_list2dex_int(data) * 0.1
        return f"{data}V"


def getMotorCtrI(data):
    if data == gm.hex_list2dex_int('FF FE'):
        return '异常'
    elif data == gm.hex_list2dex_int('FF FF'):
        return '无效'
    else:
        data = gm.hex_list2dex_int(data) * 0.1
        data -= 1000
        return f"{data}A"
