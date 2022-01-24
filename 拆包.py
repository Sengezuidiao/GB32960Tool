import os
import re
from data_struct_def import getMLbs, getYDbz, get_data_len, getCommand
from dataUnitAnalysis import analysis
from generalmethod import getJMfs, lhex2Ascii, hex_list2dex_int


# 从文件中获取原始数据,默认获取第0行
def getFileData(filename='5.txt', line=0):
    if line == 0:
        line = 0
    else:
        line = line - 1
    f = open(filename, encoding='UTF-8')
    text = f.readlines()
    text_data = text[line].strip('\n').strip(' ').replace('0x', '')  # 原始16进制所在行数,并去除两边的换行和空格符号
    text_data = re.findall(".{2}", text_data)
    text_data = " ".join(text_data)
    text_data = text_data.split(' ')  # 以空格分割存入列表
    f.close()
    return text_data


data = getFileData(line=1)

qi_shi_fu = data[0:2]  # 起始符
ming_ling_dy = data[2:4]  # 命令单元
ming_ling_bz = data[2]  # 命令标志
ying_da_bz = data[3]  # 应答标志
wei_yi_bzm = data[4:21]  # 唯一标识码
wei_yi_bzm = " ".join(wei_yi_bzm)
jia_mi_fs = data[21]  # 加密方式
shu_ju_len = data[22:24]  # 数据单元长度
if hex_list2dex_int(shu_ju_len) != 0:
    data_dy = data[24:-1]  # 数据单元
else:
    data_dy = []  # 数据单元为空
jy_ma = data[-1]  # 校验码
if os.path.exists('拆包.text'):
    os.remove('拆包.text')

fOut = open('拆包.text', 'a', encoding="UTF-8")
fOut.write("原始报文:{}\n".format(" ".join(data)))
fOut.write("起始符:" + " ".join(qi_shi_fu) + "\n")
mlbs = getMLbs(ming_ling_bz)
ydbz = getYDbz(ying_da_bz)
fOut.write("命令单元:\n" + "  命令标志: " + "".join(ming_ling_bz) + mlbs +
           "\n" + "  应答标志: " + "".join(ying_da_bz) + ydbz + "\n")
fOut.write("唯一标识码:\n" + wei_yi_bzm + '\n定义:' + lhex2Ascii(wei_yi_bzm) + "\n")
jmfs = getJMfs(jia_mi_fs)
fOut.write("数据单元加密方式:" + "".join(jia_mi_fs) + jmfs + "\n")
data_len = "".join(shu_ju_len)
data_len = get_data_len(data_len)
fOut.write("数据单元长度:" + " ".join(shu_ju_len) + data_len + "\n")
fOut.write("数据单元:" + " ".join(data_dy) + '\n\n')

flag = getCommand(ming_ling_bz)
dataFenxi = analysis(flag, data_dy)
fOut.write(dataFenxi + "\n")
fOut.write("校验码:" + "".join(jy_ma) + "\n")
fOut.close()
