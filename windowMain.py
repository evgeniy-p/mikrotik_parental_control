import sys
import mainwin
import but1
import logs
import message
from PyQt5.QtWidgets import QApplication, QMainWindow

class MainWindow():
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.ui = mainwin.Ui_MainWindow()
        self.window = QMainWindow()
        self.windowmessage = None
        self.windowbut1 = None
        self.windowbut3 = None

    def set_params(self, router_host):
        self.r_hosts = router_host
        self.hosts = self.r_hosts.get_hosts()
        self.window.move(300, 300)
        self.ui.setupUi(self.window)
        self.set_combo_box()

    def set_combo_box(self):
        self.ui.comboBox.addItem('None')
        for host in self.hosts:
            self.ui.comboBox.addItem(self.hosts[host]['host-name'])

    def run(self):
        self.ui.pushButton.clicked.connect(self.button1)
        self.ui.pushButton_3.clicked.connect(self.button3)
        self.ui.pushButton_4.clicked.connect(self.refresh)
        self.window.show()
        sys.exit(self.app.exec_())

    def button1(self):
        if self.ui.comboBox.currentText() == 'None':
            self.uimessage= message.Ui_Form()
            self.windowmessage = QMainWindow()
            self.windowmessage.move(500, 500)
            self.uimessage.setupUi(self.windowmessage)
            self.uimessage.label.setText('   ВЫБЕРИТЕ ХОСТ!!!')
            self.uimessage.pushButton.clicked.connect(self.windowmessage.hide)
            self.windowmessage.show()
            return
        if self.windowmessage:
            self.windowmessage.hide()
        self.uibut1 = but1.Ui_Form()
        self.uibut1.hostname = self.ui.comboBox.currentText()
        self.windowbut1 = QMainWindow()
        self.windowbut1.move(700, 300)
        self.uibut1.setupUi(self.windowbut1)
        if self.hosts[self.ui.comboBox.currentText()]['dynamic'] == 'false':
            self.uibut1.pushButton.setText('already static')
            self.uibut1.pushButton.setDisabled(True)
        else:
            self.uibut1.pushButton_3.setDisabled(True)
        self.uibut1.pushButton_2.clicked.connect(self.pushbuttonbut1_2)
        self.windowbut1.show()

    def button3(self):
        if self.windowmessage:
            self.windowmessage.hide()
        if self.windowbut1:
            self.windowbut1.hide()
        self.uibut3 = logs.Ui_Form()
        self.windowbut3 = QMainWindow()
        self.windowbut3.move(700, 600)
        self.uibut3.setupUi(self.windowbut3)
        self.windowbut3.show()
        with open('/home/coreusr/PycharmProjects/study/mikrotik.log', 'r') as file:
            for line in file:
                self.uibut3.textBrowser.appendPlainText(line)

    def pushbuttonbut1_2(self):
        self.uibut1.pushButton_2.setText("inet is off")
        self.windowbut1.hide()
        self.ui.comboBox.clear()
        self.set_combo_box()

    def refresh(self):
        self.ui.comboBox.clear()
        self.set_combo_box()
        if self.windowmessage:
            self.windowmessage.hide()
        if self.windowbut1:
            self.windowbut1.hide()
        if self.windowbut3:
            self.windowbut3.hide()





