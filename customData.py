import generalmethod as gm
import logging
from ModelData import G100, V500, s240E

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("__name__")


#  自定义数据
def getCustomData(data):
    data_len = gm.hex_list2dex_int(data[0:2])  # 自定义数据长度
    model_code = get_model_code(data[2])
    protocol_version = data[3]
    model_data = get_model_data(data[4:], model_code)

    return f"自定义数据长度:{data_len}字节\n" \
           f"车型代号:{model_code}\n" \
           f"协议版本号:{protocol_version}\n" \
           f"车型数据:\n{model_data}\n"


#  获取车型代号
def get_model_code(data):
    if data == '01':
        return 'G100'
    elif data == '02':
        return 'V500'
    elif data == '03':
        return 's240e'
    else:
        return '车型代码错误'


#  获取车型数据
def get_model_data(data, model_code):
    if model_code == 'G100':
        model_data = G100.get_model_data(data)
    elif model_code == 'V500':
        model_data = V500.get_model_data(data)
    elif model_code == 's240E':
        model_data = s240E.get_model_data(data)
    else:
        return "车型错误"
    return model_data
