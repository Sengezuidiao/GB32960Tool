import os

import PySide2
from PySide2.QtWidgets import QApplication
from PySide2.QtUiTools import QUiLoader
from PySide2.QtGui import QIcon
from PySide2 import QtCore
import re
import guiunpack
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class Tool:
    def __init__(self):
        self.ui = QUiLoader().load('toolwindow.ui')
        self.ui.setWindowIcon(QIcon('icon/tool.png'))
        self.ui.button.clicked.connect(self.buttonClick)

    def buttonClick(self):
        data = self.ui.textEdit.toPlainText()
        logger.info(data)
        data = data.strip('\n').strip(' ').upper().replace('0X', '').replace(" ","")
        logger.info(data)
        data_list = re.findall(".{2}", data)
        data = " ".join(data_list)
        data = data.split(' ')
        logger.info(data)
        # try:
        #     outText = guiunpack.dataUnpack(data)
        #     self.ui.textBrowser.setText(outText)
        # except Exception as e:
        #     # error_str = '输入的报文信息有误，请检查重新输入\n错误信息:\n' + str(e)
        #     # self.ui.textBrowser.setText('输入的报文信息有误，请检查重新输入')
        #     self.ui.textBrowser.setText(str(e))
        outText = guiunpack.dataUnpack(data)
        self.ui.textBrowser.setText(outText)


if __name__ == '__main__':
    dirname = os.path.dirname(PySide2.__file__)
    plugin_path = os.path.join(dirname, 'plugins', 'platforms')
    os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.ApplicationAttribute.AA_EnableHighDpiScaling)  # 允许高分辨率缩放
    app = QApplication([])
    tool = Tool()
    tool.ui.show()
    app.exec_()
