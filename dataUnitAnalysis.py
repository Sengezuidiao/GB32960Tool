
from generalmethod import getJMfs,listTime2Dec, lhex2Ascii, hex_list2dex_int
from infohandle import getInfoType, infoHandle

#  车辆登入分析
def vehicleLogin(data_dy):
    data_collect_time = data_dy[0:6]
    login_SN = data_dy[6:8]  # 登入流水号
    login_SN = hex_list2dex_int(login_SN)
    ICCID = data_dy[8:28]
    subSystemNum = data_dy[28]
    systemCodeLen = data_dy[29]
    endIndex =30 + int(subSystemNum,16) * int(systemCodeLen,16)
    systemCode = " ".join(data_dy[30:endIndex])
    clt_time = listTime2Dec(data_collect_time)
    string = f"数据采集时间:{clt_time}\n" \
             f"登入流水号:{login_SN}\n" \
             f"ICCID:{lhex2Ascii(ICCID)}\n" \
             f"可充电储能子系统数:{subSystemNum}\n" \
             f"可充电储能系统编码长度:{systemCodeLen}字节\n" \
             f"可充电储能系统编码:{lhex2Ascii(systemCode)}"
    return string

#  实时信息上报
def realTimeInfoUp(data_dy):
    data_collect_time = data_dy[0:6]
    clt_time = listTime2Dec(data_collect_time)
    infoTypeFlag = data_dy[6]
    infoBody = data_dy[7:]
    infoTypeFlag = getInfoType(infoTypeFlag)
    info = infoHandle(infoTypeFlag,infoBody)
    string = f'数据采集时间:{clt_time}\n' \
             f'信息类型标志:{infoTypeFlag}\n' \
             f'{info}'
    return string
#  补发信息上报
def reissueInfoUp(data_dy):
    return realTimeInfoUp(data_dy)

#  车辆登出
def vehicleLogout(data_dy):
    data_collect_time = data_dy[0:6]
    clt_time = listTime2Dec(data_collect_time)
    logout_SN = data_dy[6:8]
    string = f"登出时间:{clt_time}\n登出流水号:{logout_SN}"
    return string









# 根据命令单元进行索引分析
def analysis(flag, data_dy):
    if flag == '车辆登入':
        return  vehicleLogin(data_dy)
    elif flag == '实时信息上报':
        return  realTimeInfoUp(data_dy)
    elif flag == '补发信息上报':
        return reissueInfoUp(data_dy)
    elif flag == '车辆登出':
        return vehicleLogout(data_dy)
    elif flag == '平台传输数据占用':
        return  platformLogin(data_dy)
    elif flag == '心跳':
        return '数据单元为空'
    elif flag == '终端校时':
        return '数据单元为空'
    elif flag == '上行数据系统预留':
        return platformLogout(data_dy)
    elif flag == '查询命令':
        return platformLogout(data_dy)
    elif flag == '设置命令':
        return platformLogout(data_dy)
    elif flag == '车载终端控制命令':
        return platformLogout(data_dy)
    elif flag == '下行数据系统预留':
        return platformLogout(data_dy)
    elif flag == '平台交换自定义数据':
        return platformLogout(data_dy)
    else:
        print("命令标识程序未完成\n")
        return None