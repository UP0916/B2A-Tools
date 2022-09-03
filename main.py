import sys
from src import GUI
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox


class Main(QMainWindow, GUI.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.setWindowIcon(QtGui.QIcon("./images/Logo.ico")) # 设置软件图标
        self.setFixedSize(self.width(), self.height()) # 禁止窗口最大化

        # 信号
        self.pushButton.clicked.connect(self.Conversion)

    def get_text(self):
        if (text := self.plainTextEdit.toPlainText()) != "":
            return text.replace("\r", "").replace("\n", "").replace("\t", "")
        QMessageBox.information(self, "温馨提示", "您输入的内容为空!", QMessageBox.Yes)

    def is_conform(self, bin_str):
        ''' bin_str是否符合，只存在0或者1 '''
        if all(i in ["0", "1"] for i in bin_str):
            return True
        QMessageBox.information(self, "温馨提示", "您输入的内容只能是0或者1!", QMessageBox.Yes)

    def get_checkBox_state(self):
        return self.checkBox.isChecked()

    def bin_str_exchange(self, bin_str):
        ''' bin_str 0和1交换 '''
        return "".join("1" if i == "0" else "0" for i in bin_str)

    def binary_to_ascii(self, bin_str, bit, reverse=False):
        ascii_str = ""
        for i in range(0, len(bin_str), bit):
            bin_ = bin_str[i:i + bit][::-1] if reverse else bin_str[i:i + bit]
            # 如果127 >= num >= 32,那就是可见字符,不可见字符统统转换为`~`(波浪线)
            ascii_str += chr(num) if 127 >= (num := int(bin_, 2)) >= 32 else chr(126)
        return ascii_str

    def Normal_Conversion(self, bin_str):
        return [self.binary_to_ascii(bin_str, 7), self.binary_to_ascii(bin_str, 8)]
    
    def special_Conversion(self, bin_str):
        return [self.binary_to_ascii(bin_str, 7), self.binary_to_ascii(bin_str, 8)]

    def special_Conversion2(self, bin_str):
        return [self.binary_to_ascii(bin_str, 7, True), self.binary_to_ascii(bin_str, 8, True)]

    def Conversion(self):
        # 判断是否输入框是否为空
        if (bin_str := self.get_text()) is not None:
            # 判断输入框类容是否符合要求
            if self.is_conform(bin_str) is not None:
                if self.get_checkBox_state():
                    bin_str = self.bin_str_exchange(bin_str)
                
                # 开始转换
                normal_list = self.Normal_Conversion(bin_str)

                reverse_bin_str = bin_str[::-1]
                special_list = self.special_Conversion(reverse_bin_str)
                special_list2 = self.special_Conversion2(bin_str)

                # 判断是否有flag字段
                ascii_list = normal_list + special_list + special_list2
                self.show_info(ascii_list)

    def set_planTextEdit(self, ascii_str, index):
        if index == 0:
            self.plainTextEdit_2.setPlainText(ascii_str)
        elif index == 1:
            self.plainTextEdit_3.setPlainText(ascii_str)
        elif index == 2:
            self.plainTextEdit_4.setPlainText(ascii_str)
        elif index == 3:
            self.plainTextEdit_5.setPlainText(ascii_str)
        elif index == 4:
            self.plainTextEdit_6.setPlainText(ascii_str)
        elif index == 5:
            self.plainTextEdit_7.setPlainText(ascii_str)

    def show_info(self, ascii_list):
        self.plainTextEdit_8.setPlainText("")
        for index, ascii_str in enumerate(ascii_list):
            if "flag" in ascii_str.lower():
                self.plainTextEdit_8.insertPlainText(f"FLAG可能在右边第{index + 1}输出框\n")
            self.set_planTextEdit(ascii_str, index)


if __name__ == "__main__":
    QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling) # DPI自适应
    app = QApplication(sys.argv)
    ui = Main()
    ui.show()
    sys.exit(app.exec_())