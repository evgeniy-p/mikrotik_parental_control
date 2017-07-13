import sys
import mainwin
import but1
import dhcp_hosts
import logs

from PyQt5.QtWidgets import QApplication, QMainWindow

class MainWindow():
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.ui = mainwin.Ui_MainWindow()
        self.window = QMainWindow()

    def set_params(self, hosts, router):
        self.hosts = hosts
        self.router = router
        self.window.move(300, 300)
        self.ui.setupUi(self.window)
        for host in hosts:
            self.ui.comboBox.addItem(self.hosts[host]['host-name'])


    def run(self):
        self.ui.pushButton.clicked.connect(self.button1)
        self.ui.pushButton_3.clicked.connect(self.button3)
        self.window.show()
        sys.exit(self.app.exec_())

    def button1(self):
        #if dhcp_hosts.is_static_host(self.hosts[self.ui.comboBox.currentText()]):

        self.uibut1 = but1.Ui_Form()
        self.uibut1.hostname = self.ui.comboBox.currentText()
        self.windowbut1 = QMainWindow()
        self.windowbut1.move(700, 300)
        self.uibut1.setupUi(self.windowbut1)
        self.uibut1.pushButton_2.clicked.connect(self.pushbuttonbut1_2)
        self.windowbut1.show()

    def button3(self):
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

