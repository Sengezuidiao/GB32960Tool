import generalmethod as gm
import infohandle as ifo


def vehicleLocationData(data):
    locationState = data[0]
    locationState = getLocationState(locationState)
    state = locationState[0]
    longitudeState = locationState[2]
    latitudeState = locationState[1]
    longitude = data[1:5]
    longitude = getLongitudeInfo(longitude)

    latitude = data[5:9]
    latitude = getLatitude(latitude)

    string = f"定位状态:{state}\n" \
             f"{longitudeState}:{longitude}\n" \
             f"{latitudeState}:{latitude}\n\n"
    body = data[8:]
    body_len = len(body)
    if body_len == 1:
        return string + "\n"
    else:
        flag = ifo.getInfoType(body[1])
        string += f'信息类型标志:{flag}\n'
        print(body)
        body = body[2:]
        string_next = ifo.infoHandle(flag, body)
        return string + string_next


def getLocationState(data):
    data = gm.hex_list2dex_int(data)
    data = "{:08b}".format(data)
    if data[0] == '0':
        a = '有效定位'
    else:
        a = '无效定位'

    if data[1] == '0':
        b = '北纬 '
    else:
        b = '南纬 '
    if data[2] == '0':
        c = '东经 '
    else:
        c = '西经 '

    return a, b, c


def getLongitudeInfo(data):
    data = gm.hex_list2dex_int(data)
    data /= 1000000
    return f'{data}°'


def getLatitude(data):
    data = gm.hex_list2dex_int(data)
    data /= 1000000
    return f'{data}°'
