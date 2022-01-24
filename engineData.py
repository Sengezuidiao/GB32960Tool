import infohandle as ifo
import generalmethod as gm


def engineDataFormat(data):
    engineState = data[0]
    engineState = getEngineState(engineState)

    crankshaftSpeed = data[1:3]
    crankshaftSpeed = getShaftSpeed(crankshaftSpeed)

    fuelConsumeRate = data[3:5]
    fuelConsumeRate = getFuelConsumeRate(fuelConsumeRate)

    string = f'\n发动机状态:{engineState}\n' \
             f'曲轴转速:{crankshaftSpeed}\n' \
             f'燃料消耗率:{fuelConsumeRate}\n'
    body = data[4:]
    body_len = len(body)
    if body_len == 1:
        return string
    else:
        flag = ifo.getInfoType(body[1])
        body = body[2:]
        string_next = ifo.infoHandle(flag, body)
        return string + string_next


def getEngineState(data):
    if data == '01':
        return '  启动状态'
    elif data == '02':
        return '  关闭状态'
    elif data == 'FE':
        return '  异常'
    elif data == 'FF':
        return '  无效'


def getShaftSpeed(data):
    data = gm.hex_list2dex_int(data)
    if data == gm.hex_list2dex_int('FF FE'):
        return '异常'
    if data == gm.hex_list2dex_int('FF FF'):
        return '无效'
    else:
        return f'{data} r/min'


def getFuelConsumeRate(data):
    data = gm.hex_list2dex_int(data)
    if data == gm.hex_list2dex_int('FF FE'):
        return '异常'
    if data == gm.hex_list2dex_int('FF FF'):
        return '无效'
    else:
        data = data * 0.01
        return f"{data} L/km"
