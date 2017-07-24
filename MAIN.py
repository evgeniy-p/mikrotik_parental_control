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
import filter
import scirpt
import sched_but
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
        self.Mui.pushButton.clicked.connect(self.button1)
        self.Mui.pushButton_3.clicked.connect(self.button3)
        self.Mui.pushButton_4.clicked.connect(self.refresh)
        # Окно кнопки 1
        self.uibut1 = but1.Ui_Form()
        self.windowbut1 = QMainWindow()
        self.uibut1.setupUi(self.windowbut1)
        self.uibut1.pushButton.clicked.connect(self.pushbuttonbut1_1)
        self.uibut1.pushButton_2.clicked.connect(self.pushbuttonbut1_2)
        self.uibut1.pushButton_3.clicked.connect(self.pushbuttonbut1_3)
        self.uibut1.pushButton_4.clicked.connect(self.pushbuttonbut1_4)
        # Окно кнопки 1-4 (расписание)
        self.uibut2 = but1.Ui_Form()
        self.windowbut2 = QMainWindow()
        self.uibut2.setupUi(self.windowbut2)
        self.uibut2.pushButton.clicked.connect(self.pushbuttonbut2_4)
        self.uibut2.pushButton_2.clicked.connect(self.pushbuttonbut2_4)
        self.uibut2.pushButton_3.clicked.connect(self.pushbuttonbut2_4)
        self.uibut2.pushButton_4.clicked.connect(self.pushbuttonbut2_4)
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
        self.logger = logging.getLogger(__name__)
        self.gui = logging.StreamHandler(Writer(self.uibut3))
        self.logfile = logging.FileHandler('mikrotik.log')
        self.logger.addHandler(self.gui)
        self.logger.addHandler(self.logfile)
        # Окно кнопки sched_but
        self.date_time = None
        self.uished_but = sched_but.Ui_Form()
        self.windowshed_but = QMainWindow()
        self.windowshed_but.move(700, 600)
        self.uished_but.setupUi(self.windowshed_but)
        self.uished_but.dateTimeEdit_3.setDisabled(True)
        self.uished_but.dateTimeEdit_4.setDisabled(True)
        self.uished_but.dateTimeEdit_5.setDisabled(True)
        self.uished_but.dateTimeEdit_6.setDisabled(True)
        self.time_disabeled_3_4 = True
        self.time_disabeled_5_6 = True
        self.uished_but.pushButton_2.clicked.connect(self.set_en_3_4)
        self.uished_but.pushButton_3.clicked.connect(self.set_en_5_6)
        # Соединение с mikrotik
        self.s = None
        self.router = None
        self.start_connect()
        self.login()
        self.logger.debug(' Запускаем главное окно, передаем список хостов')
        # обращаемся к классу, по которому можно получить список хостов, а также задать статику и т.п
        self.router_hosts = dhcp_hosts.DhcpHosts(self.router)
        self.hosts_dict = self.router_hosts.hosts
        # обращаемся к классу, по которому можно создать\удалить правило в firewall
        self.router_filter = filter.Filter(self.router)
        # Обращаемся к классу, по которому можно создать скрипт и получить его id
        self.wwscript = scirpt.Scripts(self.router)
        # script_id.choose_policy(policy_can[3], policy_can[2])
        # script_id.make('script', 'test_script32')
        # id1 = script_id.id

        # Обращаемся к классу, по которому можно создать правило расписания и получить его id для дальнейшего управления

    def set_en_3_4(self):
        if self.time_disabeled_3_4:
            self.uished_but.pushButton_2.setText('-')
            self.uished_but.dateTimeEdit_3.setDisabled(False)
            self.uished_but.dateTimeEdit_4.setDisabled(False)
            self.time_disabeled_3_4 = False
        else:
            self.uished_but.pushButton_2.setText('+')
            self.uished_but.dateTimeEdit_3.setDisabled(True)
            self.uished_but.dateTimeEdit_4.setDisabled(True)
            self.time_disabeled_3_4 = True

    def set_en_5_6(self):
        if self.time_disabeled_5_6:
            self.uished_but.pushButton_3.setText('-')
            self.uished_but.dateTimeEdit_5.setDisabled(False)
            self.uished_but.dateTimeEdit_6.setDisabled(False)
            self.time_disabeled_5_6 = False
        else:
            self.uished_but.pushButton_3.setText('+')
            self.uished_but.dateTimeEdit_5.setDisabled(True)
            self.uished_but.dateTimeEdit_6.setDisabled(True)
            self.time_disabeled_5_6 = True

    def start_connect(self):
        self.s = mikr_api.main(conf.r1_ipaddr)
        if not self.s:
            self.uimessage.label.setText('Нет соединения!!!!')
            self.uimessage.pushButton.clicked.connect(self.windowmessage.close)
            self.windowmessage.show()
            self.logger.critical(' Соединение с mikrotik не установилась!')
            sys.exit(self.app.exec_())
        self.router = mikr_api.ApiRos(self.s)
        self.logger.debug(' Соединение по сети прошло успешно')

    def login(self):
        self.logger.debug(' Попытка логина (авторизация)....')
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
                self.logger.critical(' Логин или пароль не верен!')
                self.uimessage.label.setText('    Не авторизован!')
                self.uimessage.pushButton.clicked.connect(self.windowmessage.close)
                self.windowmessage.show()
                sys.exit(self.app.exec_())
                sys.exit()
            self.logger.debug(' Логин прошел успешно')

    def set_combo_box(self):
        self.Mui.comboBox.clear()
        self.Mui.comboBox.addItem('None')
        for host in self.hosts_dict:
            self.Mui.comboBox.addItem(self.hosts_dict[host]['host-name'])

    def run(self):
        self.set_combo_box()
        self.logger.debug('заполняем выпадающий список')
        self.Mwindow.show()
        sys.exit(self.app.exec_())

    def button1(self):
        self.windowbut1.move(700, 300)
        self.windowbut2.close()
        self.logger.debug('"Изменить"')

        if self.Mui.comboBox.currentText() == 'None':
            if self.windowbut1:
                self.windowbut1.hide()
            self.logger.debug(' host- none- warning')
            self.uimessage.label.setText('   ВЫБЕРИТЕ ХОСТ!!!\nЕсли хостов нет -\nпопробуйте\n'
                                         'переподключить\nустройство к сети!')
            self.uimessage.pushButton.clicked.connect(self.windowmessage.hide)
            self.windowmessage.show()
            return
        if self.windowmessage:
            self.windowmessage.hide()
        self.logger.debug(' button1 pressed')
        self.windowbut1.setWindowTitle(self.Mui.comboBox.currentText())
        self.uibut1.hostname = self.Mui.comboBox.currentText()
        self.logger.debug(' hostname {}'.format(self.Mui.comboBox.currentText()))
        self.windowbut1.show()
        if self.router_filter.isblocked(self.Mui.comboBox.currentText()):
            self.uibut1.pushButton_2.setText("unblock inet")
            self.uibut1.pushButton_4.setDisabled(False)
        else:
            self.uibut1.pushButton_2.setText("block inet")
            self.uibut1.pushButton_4.setDisabled(True)
        self.dynamic()

    def dynamic(self):
        try:
            if self.hosts_dict[self.Mui.comboBox.currentText()]['dynamic'] == 'false':
                self.uibut1.pushButton.setText('already static')
                self.uibut1.pushButton.setDisabled(True)
                self.uibut1.pushButton_3.setDisabled(False)
                self.uibut1.pushButton_2.setDisabled(False)
                self.uibut1.pushButton_4.setDisabled(False)
            else:
                self.uibut1.pushButton_4.setDisabled(True)
                self.uibut1.pushButton.setText('make static')
                self.uibut1.pushButton_2.setDisabled(True)
                self.uibut1.pushButton.setDisabled(False)
                self.uibut1.pushButton_3.setDisabled(True)
        except KeyError:
            self.no_shuch_host()

    def button3(self):
        self.logger.debug('"Логи"')
        if self.windowmessage:
            self.windowmessage.hide()
        if self.windowbut1:
            self.windowbut1.hide()
        self.windowbut3.show()

    def pushbuttonbut1_1(self):
        self.logger.debug(' pushbuttonbut1_1 pressed')
        self.router_hosts.make_static(self.Mui.comboBox.currentText())
        self.start_connect()
        self.login()
        self.router_hosts = dhcp_hosts.DhcpHosts(self.router)
        self.hosts_dict = self.router_hosts.hosts
        self.dynamic()

    def pushbuttonbut1_2(self):
        self.windowshed_but.close()
        self.router_filter = filter.Filter(self.router)
        self.logger.debug(' pushbuttonbut1_2 pressed')
        if self.router_filter.isblocked(self.Mui.comboBox.currentText()):
            self.router_filter.delete_rule(self.Mui.comboBox.currentText())
            self.uibut1.pushButton_2.setText("block inet")
            self.uibut1.pushButton_3.setDisabled(False)
            self.uibut1.pushButton_4.setDisabled(False)
        else:
            self.router_filter.forwardblock(self.Mui.comboBox.currentText())
            self.uibut1.pushButton_2.setText("unblock inet")
            self.uibut1.pushButton_3.setDisabled(True)
            self.uibut1.pushButton_4.setDisabled(True)

    def pushbuttonbut1_3(self):
        self.windowbut1.hide()
        self.logger.debug(' pushbuttonbut1_3 pressed')
        self.router_hosts.remove_static(self.Mui.comboBox.currentText())
        self.refresh()
        self.logger.debug(' lease remove- warning')
        self.uimessage.label.setText('Удалено!\nНужно будет\nпереподключить\nустройства к сети'
                                     '\nдля дальнейшей\nработы!')
        self.uimessage.pushButton.clicked.connect(self.windowmessage.hide)
        self.windowmessage.show()

# self.wwscript.make_script(self.Mui.comboBox.currentText(),
#                                  self.hosts_dict[self.Mui.comboBox.currentText()]['address'])
    def pushbuttonbut1_4(self):
        self.windowbut2.move(800, 300)
        self.windowbut2.setWindowTitle('Расписание')
        self.uibut2.pushButton.setText('Настроить')

        self.uibut2.pushButton_2.setText("Включить")
        self.uibut2.pushButton_3.setText("Выключить")
        self.uibut2.pushButton_4.setText('Удалить')

        self.windowbut1.close()
        self.windowbut2.show()

    def pushbuttonbut2_4(self):
        self.date_time = list()
        self.uished_but.pushButton.clicked.connect(self.get_time)
        self.windowshed_but.show()

    def get_time(self):
        self.uished_but.dateTimeEdit.dateTime()
        print(self.uished_but.dateTimeEdit.dateTime())
        print(self.uished_but.dateTimeEdit.dateTime().toString(format('dd.MM.yyyy')))

    def refresh(self):
        self.logger.debug(' refresh button pressed')
        self.logger.debug(' Restart')
        self.Mui.comboBox.clear()
        self.start_connect()
        self.login()
        self.router_hosts = dhcp_hosts.DhcpHosts(self.router)
        self.hosts_dict = self.router_hosts.hosts
        self.set_combo_box()
        if self.windowbut1:
            self.windowbut1.hide()

    def no_shuch_host(self):
        self.uimessage.label.setText('Нажмите "Обновить"')
        self.uimessage.pushButton.clicked.connect(self.windowmessage.close)
        self.windowmessage.show()


class Writer:
    def __init__(self, widget):
        self.widget = widget
    def write(self, text):
        self.widget.textBrowser.appendPlainText(text)


if __name__ == '__main__':
    logging.basicConfig(filename='mikrotik.log', filemode='w', level=logging.DEBUG, format='%(asctime)s %(message)s')
    logging.debug(' Start')
    widget = MainWindow()
    widget.run()
