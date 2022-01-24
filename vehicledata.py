from generalmethod import hex_list2dex_int
import infohandle


# 整车数据
def vehicleData(body):
    vehicle_state = body[0]  # 车辆状态
    vehicle_state = vehicleState(vehicle_state)
    charge_state = body[1]  # 充电状态
    charge_state = chargeState(charge_state)
    run_way = body[2]  # 运行模式
    run_way = runWay(run_way)
    vehicle_speed = body[3:5]  # 车速
    vehicle_speed = vehicleSpeed(vehicle_speed)
    allmileage = body[5:9]  # 累计里程
    allmileage = allMileage(allmileage)
    voltage = body[9:11]  # 总电压
    voltage = voltageV(voltage)
    current = body[11:13]  # 总电流
    current = currentI(current)
    soc = body[13]  # SOC
    soc = SOC(soc)
    dc = body[14]  # DC-DC 状态
    dcstate = dcdc(dc)
    gear = body[15]  # 挡位
    gear = getGear(gear)
    resistance = body[16:18]  # 绝缘电阻
    resistance = getResistance(resistance)
    acceleratorPedalV = body[18]  # 加速踏板行程值
    acceleratorPedalV = getAcceleratorV(acceleratorPedalV)
    breakPedalS = body[19]
    breakPedalS = getBreakPedalS(breakPedalS)
    string = f'车辆状态:{vehicle_state}\n' \
             f'充电状态:{charge_state}\n' \
             f'运行模式:{run_way}\n' \
             f'车速:{vehicle_speed}\n' \
             f'累计里程:{allmileage}\n' \
             f'总电压:{voltage}\n' \
             f'总电流:{current}\n' \
             f'SOC:{soc}\n' \
             f'DC-DC状态:{dcstate}\n' \
             f'挡位:{gear}\n' \
             f'绝缘电阻:{resistance}\n' \
             f'加速踏板行程值:{acceleratorPedalV}\n' \
             f'制动踏板状态:{breakPedalS}\n\n'
    body = body[19:]
    body_len = len(body)
    if body_len == 1:
        return string
    else:
        flag = infohandle.getInfoType(body[1])
        string += f'信息类型标志:{flag}\n'
        body = body[2:]
        string_next = infohandle.infoHandle(flag, body)
        return string + string_next


# 车辆状态
def vehicleState(data):
    Dict = {
        '01': '启动',
        '02': '熄火',
        '03': '其他状态',
        'FE': '异常',
        'FF': '无效',
    }
    return Dict[data]


# 充电状态
def chargeState(data):
    Dict = {
        '01': '停车充电',
        '02': '行驶充电',
        '03': '未充电状态',
        '04': '充电完成',
        'FE': '异常',
        'FF': '无效',
    }
    return Dict[data]


# 运行模式
def runWay(data):
    Dict = {
        '01': '纯电',
        '02': '混动',
        '03': '燃油',
        '04': '异常',
        '05': '无效',
    }
    return Dict[data]


# 车速
def vehicleSpeed(data):
    speed = hex_list2dex_int(data)
    speed = speed * 0.1
    return f"{speed}km/h"


#  累计里程
def allMileage(data):
    if hex_list2dex_int(data) == hex_list2dex_int('FF FF FF FE'):
        return '异常'
    if hex_list2dex_int(data) == hex_list2dex_int('FF FF FF FF'):
        return '无效'
    data = hex_list2dex_int(data) * 0.1
    return f'{data}km'


# 电压
def voltageV(data):
    if hex_list2dex_int(data) == hex_list2dex_int('FF FE'):
        return '异常'
    if hex_list2dex_int(data) == hex_list2dex_int('FF FF'):
        return '无效'
    data = hex_list2dex_int(data)
    data = data / 10
    return f"{data}V"


# 电流
def currentI(data):
    if hex_list2dex_int(data) == hex_list2dex_int('FF FE'):
        return '异常'
    if hex_list2dex_int(data) == hex_list2dex_int('FF FF'):
        return '无效'
    data = hex_list2dex_int(data) / 10 - 1000
    return f"{data}A"


# SOC
def SOC(data):
    if hex_list2dex_int(data) == hex_list2dex_int('FE'):
        return '异常'
    if hex_list2dex_int(data) == hex_list2dex_int('FF'):
        return '无效'
    data = hex_list2dex_int(data)
    return f"{data}%"


# DC-DC
def dcdc(data):
    Dict = {
        '01': '工作',
        '02': '断开',
        'FE': '异常',
        'FF': '无效',
    }
    return Dict[data]


#  挡位
def getGear(data):
    data = hex_list2dex_int(data)
    data = "{:08b}".format(data)
    if data[2] == '0':
        a = '无驱动力'
    else:
        a = '有驱动力'

    if data[3] == '0':
        b = '无制动力 '
    else:
        b = '有制动力 '
    if data[4:8] == '0000':
        c = '空挡 '
    elif data[4:8] == '1101':
        c = '倒挡 '
    elif data[4:8] == '1110':
        c = '自动D挡 '
    elif data[4:8] == '1111':
        c = '停车P挡 '
    else:
        c = f'{int(data[4:8], 2)}挡 '

    return a + b + c


# 电阻
def getResistance(data):
    return f'{hex_list2dex_int(data)}kΩ'


# 加速踏板行程值
def getAcceleratorV(data):
    data = hex_list2dex_int(data)
    return f'{data}%'


#  获取制动踏板状态
def getBreakPedalS(data):
    if data == '00':
        return '制动关状态'
    elif data == '65':
        return '制动有效状态'
    elif data == 'FE':
        return '异常'
    elif data == 'FF':
        return '无效'
    else:
        data = hex_list2dex_int(data)
        return f'{data}%'
