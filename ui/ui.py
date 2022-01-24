from PySide2.QtWidgets import QApplication, QMainWindow, QPushButton, QPlainTextEdit, QMessageBox
from PySide2.QtGui import QIcon

app = QApplication([])
window = QMainWindow()
window.resize(1000, 1000)
window.move(300, 300)
window.setWindowTitle('32960解析工具')
window.setWindowIcon(QIcon('icon/tool.png'))
textEdit = QPlainTextEdit(window)

textEdit.resize(900, 200)
textEdit.move(0, 0)
button = QPushButton(window)
button.setText('解析')
button.move(900, 0)


def handle():
    text = textEdit.toPlainText()
    text.strip('\n')
    QMessageBox.about(window, '解析结果', text)


button.clicked.connect(handle)

window.show()
app.exec_()
