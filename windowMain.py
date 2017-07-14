import sys
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


class MainWindow():
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.ui = mainwin.Ui_MainWindow()
        self.window = QMainWindow()
        self.windowmessage = None
        self.windowbut1 = None
        self.windowbut3 = None
        self.start_connect()
        self.login()
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
            logging.critical('Соединение с mikrotik не установилась!')
            sys.exit()
        self.router = mikr_api.ApiRos(self.s)
        logging.debug('Соединение по сети прошло успешно')


    def login(self):
        logging.debug('Попытка логина (авторизация)....')
        with io.StringIO() as buf, redirect_stdout(buf):
            self.router.login(conf.r1_login, conf.r1_passwd1)
            output = buf.getvalue()
            if ">>> =message=cannot log in" in output.split('\n'):
                logging.critical('Логин или пароль не верен!')
                sys.exit()
            logging.debug('Логин прошел успешно')



    def set_combo_box(self):
        self.ui.comboBox.addItem('None')
        for host in self.hosts_dict:
            self.ui.comboBox.addItem(self.hosts_dict[host]['host-name'])

    def run(self):
        self.window.move(300, 300)
        self.ui.setupUi(self.window)
        self.set_combo_box()
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
        if self.hosts_dict[self.ui.comboBox.currentText()]['dynamic'] == 'false':
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



if __name__ == '__main__':
    with open('mikrotik.log', 'w') as file:
        file.flush()
    logging.basicConfig(filename='mikrotik.log', level=logging.WARNING)
    logging.debug('Start')
    logging.debug('Запускаем главное окно, передаем список хостов')


    widget = MainWindow()
    widget.run()