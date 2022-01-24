import logging
import generalmethod as gm

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# 每个车型自定义数据内容
def get_model_data(data):
    logger.info(data)
    no_vehicle_charge_state = getNoVehicleChargeStage(data[0])
    no_vehicle_charge_power = getNoVehicleChargePower(data[1:3])
    no_vehicle_charge_time = getNoVehicleChargeTime(data[3:5])
    BMS_state_cmd = get_BMS_state_cmd(data[5])
    speed_connect_state = get_speed_connect_state(data[6])
    ac_msg_state = get_ac_msg_state(data[7])
    real_time_low_v = get_real_time_low_v(data[8])
    real_time_low_i = get_real_time_low_i(data[9:11])
    dc_work_state = get_dc_work_state(data[11])
    component_work_state = get_component_work_state(data[12])
    vacuum_degree = get_vacuum_degree(data[13])

    return f"非车载充电机状态:{no_vehicle_charge_state}\n" \
           f"非车载充电机充电电量:{no_vehicle_charge_power}\n" \
           f"非车载充电机充电时间:{no_vehicle_charge_time}\n" \
           f"\nBMS状态指令:\n{BMS_state_cmd}" \
           f"\n动力电池快慢充连接状态:\n{speed_connect_state}\n" \
           f"\n空调报文状态:\n{ac_msg_state}\n" \
           f"低压端实时电压（仪表）:{real_time_low_v}\n" \
           f"低压端实时电流（DCDC）:{real_time_low_i}\n" \
           f"DCDC工作状态:{dc_work_state}\n" \
           f"部件工作状态:\n{component_work_state}\n" \
           f"真空度:{vacuum_degree}\n" \
           f""


# 真空度
def get_vacuum_degree(data):
    data = gm.hex_list2dex_int(data) / 100
    return f"{data}Bar"


# 部件工作这状态
def get_component_work_state(data):
    data = gm.dec2bin_reverse(data)
    if data[0] == '1':
        a = "开启"
    else:
        a = "关闭"
    if data[1] == '1':
        b = "低速风扇开启"
    else:
        b = "关闭"
    if data[2] == '1':
        c = "高速风扇开启"
    else:
        c = "关闭"
    if data[3] == '1':
        d = "开启"
    else:
        d = "关闭"
    if data[4] == '1':
        e = "拉起"
    else:
        e = "放下"
    return f"水泵:{a}\n" \
           f"水箱风扇:{b}\n" \
           f"水箱风扇:{c}\n" \
           f"真空泵:{c}\n" \
           f"手刹:{c}\n"


# DCDC工作状态
def get_dc_work_state(data):
    data = gm.dec2bin_reverse(data)
    data = gm.dec2bin_reverse(data)
    if data[0:4] == '0000':
        return '保留\n'
    if data[0:4] == '0001':
        return '自检\n'
    if data[0:4] == '0010':
        return '待机\n'
    if data[0:4] == '0011':
        return '启动\n'
    if data[0:4] == '0100':
        return '运行\n'
    if data[0:4] == '0101':
        return '正常关机\n'
    if data[0:4] == '0110':
        return '保护关机\n'
    if data[0:4] == '10100':
        return '故障状态\n'


# 低压端实时电流
def get_real_time_low_i(data):
    data = gm.hex_list2dex_int(data) / 10
    return f"{data}A"


# 低压端实时电压
def get_real_time_low_v(data):
    data = gm.hex_list2dex_int(data) / 10
    return f"{data}V\n"


# 空调报文状态
def get_ac_msg_state(data):
    data = gm.dec2bin_reverse(data)
    if data[0] == '1':
        a = "有效"
    else:
        a = "无效"
    if data[1] == '1':
        b = "开始工作"
    else:
        b = "停止工作"
    return f"空调报文状态:{a}\n" \
           f"工作使能命令:{b}\n"


#  非车载充电状态
def getNoVehicleChargeStage(data):
    if data == '01':
        return '充电握手'
    elif data == '02':
        return '充电配置'
    elif data == '03':
        return '充电'
    elif data == '04':
        return '充电结束'
    elif data == 'FE':
        return '异常'
    elif data == 'FF':
        return '无效'


#  非车载充电机充电电里
def getNoVehicleChargePower(data):
    data = gm.hex_list2dex_int(data) * 0.1
    return f'{data} kWh'


#  非车载充电机充电时间
def getNoVehicleChargeTime(data):
    data = gm.hex_list2dex_int(data)
    return f'{data} min'


#  BMS状态指令
def get_BMS_state_cmd(data):
    data = gm.dec2bin_reverse(data)
    if data[0] == '1':
        a = '吸合'
    else:
        a = '断开'
    if data[1] == '1':
        b = '吸合'
    else:
        b = '断开'
    if data[2] == '1':
        c = '吸合'
    else:
        c = '断开'
    if data[3] == '1':
        d = '电池保护，关闭充电机输出'
    else:
        d = '充电机可以开启充电'
    if data[4] == '1':
        e = '加热'
    else:
        e = '非加热'

    return f"总正接触器状态：{a}\n" \
           f"总负接触器状态：{b}\n" \
           f"电池加热继电器器状态：{c}\n" \
           f"使能控制位：{d}\n" \
           f"加热模式状态位：{e}\n"


#  电池最大允许充电电流
def getBatChargeMaxI(data):
    data = (gm.hex_list2dex_int(data) - 5000) / 10
    return f'{data} A'


#  动力电池快慢充连接状态
def get_speed_connect_state(data):
    data = gm.dec2bin_reverse(data)
    if data[0] == '1':
        a = "进入快充状态"
    else:
        a = "未连接"
    if data[1] == '1':
        b = "进入慢充状态"
    else:
        b = "未连接"
    return f"快充连接状态:{a}\n" \
           f"慢充连接状态:{b}\n"


#  电池最大允许放电电流
def getBatDischargeMaxI(data):
    data = (gm.hex_list2dex_int(data) - 5000) / 10
    return f'{data} A'
