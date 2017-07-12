import sys
import mainwin
import but1
import logs
from PyQt5.QtWidgets import QApplication, QMainWindow

class MainWindow():
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.ui = mainwin.Ui_MainWindow()
        self.window = QMainWindow()

    def set_params(self, hosts):
        self.window.move(300, 300)
        self.ui.setupUi(self.window)
        self.fill_combo(hosts)
        self.ui.pushButton.clicked.connect(self.button1)
        self.ui.pushButton_3.clicked.connect(self.button3)

    def run(self):
        self.window.show()
        sys.exit(self.app.exec_())

    def fill_combo(self, hosts=None):
        if not hosts:
            self.ui.comboBox.addItem('None')
        else:
            for host in hosts:
                self.ui.comboBox.addItem(host)

    def button1(self):
        if not self.ui.comboBox.currentText():
            return
        self.uibut1 = but1.Ui_Form()
        self.uibut1.hostname = self.ui.comboBox.currentText()
        self.windowbut1 = QMainWindow()
        self.windowbut1.move(700, 300)
        self.uibut1.setupUi(self.windowbut1)
        self.windowbut1.show()

    def button3(self):
        self.uibut2 = logs.Ui_Form()
        self.windowbut3 = QMainWindow()
        self.windowbut3.move(700, 600)
        self.uibut2.setupUi(self.windowbut3)
        self.windowbut3.show()


