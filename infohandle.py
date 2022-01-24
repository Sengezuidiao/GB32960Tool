from generalmethod import hex_list2dex_int
from vehicledata import vehicleData
from motordata import motorData
from rechargeEstorageVdata import chargeableStorageVData
from rechargeableEstorageTempData import chargeableStorageTemData
from extremeData import getExtremeData
from vehiclelocationdata import vehicleLocationData
from alarmdata import alarmData
from engineData import engineDataFormat
from customData import getCustomData


#  获取信息类型标志
def getInfoType(key):
    Dict = {
        '01': '整车数据',
        '02': '驱动电机数据',
        '03': '燃料电池数据',
        '04': '发动机数据',
        '05': '车辆位置',
        '06': '极值数据',
        '07': '报警数据',
        '08': '可充电储能装置电压数据',
        '09': '可充电储能装置温度数据',
        'A': '平台交换协议自定义数据',
        'B': '预留',
        '83': '用户自定义'
    }
    if key in Dict:
        return Dict[key]
    elif hex_list2dex_int('0A') <= hex_list2dex_int(key) <= hex_list2dex_int('2F'):
        return Dict['A']
    elif hex_list2dex_int('30') <= hex_list2dex_int(key) <= hex_list2dex_int('7F'):
        return Dict['B']
    elif hex_list2dex_int('80') <= hex_list2dex_int(key) <= hex_list2dex_int('FE'):
        return Dict['C']
    else:
        return "信息体标识错误"


#  信息体处理
def infoHandle(flag, body):
    if flag == '整车数据':
        return vehicleData(body)
    elif flag == '驱动电机数据':
        return motorData(body)
    elif flag == '燃料电池数据':
        return '燃料电池'
    elif flag == '发动机数据':
        return engineDataFormat(body)
    elif flag == '车辆位置':
        return vehicleLocationData(body)
    elif flag == '极值数据':
        return getExtremeData(body)
    elif flag == '报警数据':
        return alarmData(body)
    elif flag == '可充电储能装置电压数据':
        return chargeableStorageVData(body)
    elif flag == '可充电储能装置温度数据':
        return chargeableStorageTemData(body)
    elif flag == '平台交换协议数据':
        return '平台交换协议数据'
    elif flag == '预留':
        return '预留'
    elif flag == '用户自定义':
        return getCustomData(body)
