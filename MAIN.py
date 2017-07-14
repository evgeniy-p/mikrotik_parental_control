import sys
import time
import mainwin
import but1
import logs
import message
import mikr_api
import conf
import sys
import io
import dhcp_hosts
import scirpt
import scheduler
import logging
from contextlib import redirect_stdout
from PyQt5.QtWidgets import QApplication, QMainWindow

policy_can = ['ftp', 'reboot', 'read', 'write', 'policy', 'test', 'password', 'sniff', 'sensitive', 'romon']


class MainWindow:
    def __init__(self):
        self.app = QApplication(sys.argv)
        # Главное окно
        self.Mui = mainwin.Ui_MainWindow()
        self.Mwindow = QMainWindow()
        self.Mwindow.move(300, 300)
        self.Mui.setupUi(self.Mwindow)
        # Окно кнопки 1
        self.uibut1 = but1.Ui_Form()
        self.windowbut1 = QMainWindow()
        self.windowbut1.move(700, 300)
        self.uibut1.setupUi(self.windowbut1)
        # Окно сообщения об ошибке
        self.uimessage = message.Ui_Form()
        self.windowmessage = QMainWindow()
        self.windowmessage.move(500, 500)
        self.uimessage.setupUi(self.windowmessage)
        # Окно кнопки 3
        self.uibut3 = logs.Ui_Form()
        self.windowbut3 = QMainWindow()
        self.windowbut3.move(700, 600)
        self.uibut3.setupUi(self.windowbut3)
        # Соединение с mikrotik
        self.start_connect()
        self.login()
        logging.debug(time.ctime() + ' Запускаем главное окно, передаем список хостов')
        # обращаемся к классу, по которому можно получить список хостов, а также задать статику и т.п
        self.router_hosts = dhcp_hosts.DhcpHosts(self.router)
        self.hosts_dict = self.router_hosts.get_hosts()
        #hosts = router_host.get_hosts()
        #router_host.make_static(.['cent_2'])

        # Обращаемся к классу, по которому можно создать скрипт и получить его id для дальнейшего управления
        #script_id = scirpt.Scripts(router)
        # script_id.choose_policy(policy_can[3], policy_can[2])
        # script_id.make('script', 'test_script32')
        # id1 = script_id.id

        # Обращаемся к классу, по которому можно создать правило расписания и получить его id для дальнейшего управления
        #scheld_id = scheduler.Scheduler(router)
        # scheld_id.choose_policy(policy_can[3], policy_can[2])
        # scheld_id.make('scheduler', 'test_scheld')
        # id2 = scheld_id.id

    def start_connect(self):
        self.s = mikr_api.main(conf.r1_ipaddr)
        if not self.s:
            self.uimessage.label.setText('Нет соединения!!!!')
            self.uimessage.pushButton.clicked.connect(self.windowmessage.close)
            self.windowmessage.show()
            sys.exit(self.app.exec_())
            logging.critical(time.ctime() + ' Соединение с mikrotik не установилась!')
            sys.exit()
        self.router = mikr_api.ApiRos(self.s)
        logging.debug(time.ctime() + ' Соединение по сети прошло успешно')

    def login(self):
        logging.debug(time.ctime() + ' Попытка логина (авторизация)....')
        with io.StringIO() as buf, redirect_stdout(buf):
            try:
                self.router.login(conf.r1_login, conf.r1_passwd1)
            except AttributeError:
                self.uimessage.label.setText('    Не авторизован!')
                self.uimessage.pushButton.clicked.connect(self.windowmessage.close)
                self.windowmessage.show()
                sys.exit(self.app.exec_())
                sys.exit()
            output = buf.getvalue()
            if ">>> =message=cannot log in" in output.split('\n'):
                logging.critical(time.ctime() + ' Логин или пароль не верен!')
                self.uimessage.label.setText('    Не авторизован!')
                self.uimessage.pushButton.clicked.connect(self.windowmessage.close)
                self.windowmessage.show()
                sys.exit(self.app.exec_())
                sys.exit()
            logging.debug(time.ctime() + ' Логин прошел успешно')

    def set_combo_box(self):
        self.Mui.comboBox.addItem('None')
        for host in self.hosts_dict:
            self.Mui.comboBox.addItem(self.hosts_dict[host]['host-name'])

    def run(self):
        self.set_combo_box()
        self.Mui.pushButton.clicked.connect(self.button1)
        self.Mui.pushButton_3.clicked.connect(self.button3)
        self.Mui.pushButton_4.clicked.connect(self.refresh)
        self.Mwindow.show()
        sys.exit(self.app.exec_())

    def button1(self):
        if self.Mui.comboBox.currentText() == 'None':
            if self.windowbut1:
                self.windowbut1.hide()
            self.uibut3.textBrowser.appendPlainText(time.ctime() + ' host- none- warning')
            self.uimessage.label.setText('   ВЫБЕРИТЕ ХОСТ!!!')
            self.uimessage.pushButton.clicked.connect(self.windowmessage.hide)
            self.windowmessage.show()
            return
        if self.windowmessage:
            self.windowmessage.hide()
        self.uibut3.textBrowser.appendPlainText(time.ctime() + ' button1 pressed')
        self.uibut1.hostname = self.Mui.comboBox.currentText()
        self.uibut3.textBrowser.appendPlainText(time.ctime() + ' hostname {}'.format(self.Mui.comboBox.currentText()))
        if self.hosts_dict[self.Mui.comboBox.currentText()]['dynamic'] == 'false':
            self.uibut1.pushButton.setText('already static')
            self.uibut1.pushButton.setDisabled(True)
        else:
            self.uibut1.pushButton_3.setDisabled(True)
        self.uibut1.pushButton_2.clicked.connect(self.pushbuttonbut1_2)
        self.windowbut1.show()

    def button3(self):
        self.uibut3.textBrowser.appendPlainText(time.ctime() + ' button3 pressed')
        if self.windowmessage:
            self.windowmessage.hide()
        if self.windowbut1:
            self.windowbut1.hide()
        self.windowbut3.show()

    def pushbuttonbut1_2(self):
        self.uibut3.textBrowser.appendPlainText(time.ctime() + ' pushbuttonbut1_2 pressed')
        self.uibut1.pushButton_2.setText("inet is off")
        self.windowbut1.hide()
        self.Mui.comboBox.clear()
        self.set_combo_box()

    def refresh(self):
        self.uibut3.textBrowser.appendPlainText(time.ctime() + ' refresh button pressed')
        logging.debug(time.ctime() + ' Restart')
        self.Mui.comboBox.clear()
        self.set_combo_box()
        if self.windowmessage:
            self.windowmessage.hide()
        if self.windowbut1:
            self.windowbut1.hide()
        self.start_connect()
        self.login()
        self.router_hosts = dhcp_hosts.DhcpHosts(self.router)
        self.hosts_dict = self.router_hosts.get_hosts()

if __name__ == '__main__':
    with open('mikrotik.log', 'w') as mfile:
        pass
    logging.basicConfig(filename='mikrotik.log', level=logging.WARNING)
    logging.debug(time.ctime() + ' Start')
    widget = MainWindow()
    widget.run()
