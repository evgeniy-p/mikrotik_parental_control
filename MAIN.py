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
import scheduler
import sched_but
import logging
from contextlib import redirect_stdout
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtCore

policy_can = ['ftp', 'reboot', 'read', 'write', 'policy', 'test', 'password', 'sniff', 'sensitive', 'romon']


class MainWindow:
    def __init__(self):
        self.app = QApplication(sys.argv)
        # Окно кнопки 3 (logger)
        self.uibut3 = logs.Ui_Form()
        self.windowbut3 = QMainWindow()
        self.windowbut3.move(700, 600)
        self.uibut3.setupUi(self.windowbut3)
        # logger conf
        self.logger = logging.getLogger(__name__)
        self.gui = logging.StreamHandler(Writer(self.uibut3))
        self.logfile = logging.FileHandler('mikrotik.log')
        self.logger.addHandler(self.gui)
        self.logger.addHandler(self.logfile)
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
        # Обращаемся к классу, по работе с скриптами
        self.wwscript = scirpt.Scripts(self.router)
        # Обращаемся к классу по работе с расписанием
        self.scheduler = scheduler.Scheduler(self.router)
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
        # Окно кнопки 2(1-4) (расписание)
        self.uibut2 = but1.Ui_Form()
        self.windowbut2 = QMainWindow()
        self.uibut2.setupUi(self.windowbut2)
        self.uibut2.pushButton.clicked.connect(self.pushbuttonbut2_1)
        self.uibut2.pushButton_2.clicked.connect(self.pushbuttonbut2_2)
        self.uibut2.pushButton_3.clicked.connect(self.pushbuttonbut2_3)
        self.uibut2.pushButton_4.clicked.connect(self.pushbuttonbut2_4)
        self.uibut2.pushButton_2.setDisabled(True)
        self.uibut2.pushButton_3.setDisabled(True)
        self.uibut2.pushButton_4.setDisabled(True)
        # Окно сообщения об ошибке
        self.uimessage = message.Ui_Form()
        self.windowmessage = QMainWindow()
        self.windowmessage.move(500, 500)
        self.uimessage.setupUi(self.windowmessage)
        # Окно кнопки sched_but
        self.uished_but = sched_but.Ui_Form()
        self.windowshed_but = QMainWindow()
        self.windowshed_but.move(1000, 300)
        self.uished_but.setupUi(self.windowshed_but)
        self.uished_but.dateTimeEdit_2.setDisabled(True)
        self.uished_but.dateTimeEdit_4.setDisabled(True)
        self.uished_but.label_2.setDisabled(True)
        self.uished_but.label_5.setDisabled(True)
        self.uished_but.label_6.setDisabled(True)
        self.uished_but.radioButton_4.checkStateSet()
        self.uished_but.radioButton_4.setDisabled(True)
        self.uished_but.radioButton_5.setDisabled(True)
        self.uished_but.radioButton_6.setDisabled(True)
        self.uished_but.radioButton.setChecked(True)
        self.uished_but.radioButton_6.setChecked(True)
        self.time_disabeled_2 = True
        self.uished_but.pushButton_2.clicked.connect(self.set_en_2)
        self.date_en = False
        self.interval_en = False
        self.date_dis = False
        self.date_en2 = False
        self.date_dis2 = False
        self.interval_en2 = False

    def set_en_2(self):
        if self.time_disabeled_2:
            self.uished_but.label_2.setDisabled(False)
            self.uished_but.label_5.setDisabled(False)
            self.uished_but.label_6.setDisabled(False)
            self.uished_but.radioButton_4.setDisabled(False)
            self.uished_but.radioButton_5.setDisabled(False)
            self.uished_but.radioButton_6.setDisabled(False)
            self.uished_but.pushButton_2.setText('-')
            self.uished_but.dateTimeEdit_2.setDisabled(False)
            self.uished_but.dateTimeEdit_4.setDisabled(False)
            self.time_disabeled_2 = False
        else:
            self.uished_but.label_2.setDisabled(True)
            self.uished_but.label_5.setDisabled(True)
            self.uished_but.label_6.setDisabled(True)
            self.uished_but.radioButton_4.setDisabled(True)
            self.uished_but.radioButton_5.setDisabled(True)
            self.uished_but.radioButton_6.setDisabled(True)
            self.uished_but.pushButton_2.setText('+')
            self.uished_but.dateTimeEdit_2.setDisabled(True)
            self.uished_but.dateTimeEdit_4.setDisabled(True)
            self.time_disabeled_2= True

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
        self.Mui.comboBox.close()
        self.Mui.label.setText('Выбран хост:')
        self.Mui.label_2.setText(self.Mui.comboBox.currentText())
        if self.Mui.comboBox.currentText() == 'None':
            if self.windowbut1:
                self.windowbut1.hide()
            self.logger.debug(' host- none- warning')
            self.uimessage.label.setText('   ВЫБЕРИТЕ ХОСТ!!!\nЕсли хостов нет -\nпопробуйте\n'
                                         'переподключить\nустройство к сети!')
            self.uimessage.pushButton.clicked.connect(self.windowmessage.hide)
            self.windowmessage.show()
            return
        self.windowbut1.move(700, 300)
        self.windowbut2.close()
        if self.router_filter.isblocked(self.Mui.comboBox.currentText(), 'block'):
            self.dynamic()
            self.uibut1.pushButton_2.setText("unblock inet")
            self.uibut1.pushButton_3.setDisabled(True)
            self.uibut1.pushButton_4.setDisabled(True)
        elif self.router_filter.isblocked(self.Mui.comboBox.currentText(), 'sched'):
            self.uibut1.pushButton.setDisabled(True)
            self.uibut1.pushButton_2.setDisabled(True)
            self.uibut1.pushButton_3.setDisabled(True)
            self.uibut1.pushButton_4.setDisabled(False)
        else:
            self.uibut1.pushButton_2.setText("block inet")
            self.uibut1.pushButton_3.setDisabled(False)
            self.uibut1.pushButton_4.setDisabled(False)
            self.dynamic()
        if self.windowmessage:
            self.windowmessage.hide()
        self.logger.debug('modify "' + self.Mui.comboBox.currentText() + '" host')
        self.windowbut1.setWindowTitle(self.Mui.comboBox.currentText())
        self.uibut1.hostname = self.Mui.comboBox.currentText()
        self.windowbut1.show()

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
        self.logger.debug('make static "' + self.Mui.comboBox.currentText() + '" host')
        self.router_hosts.make_static(self.Mui.comboBox.currentText())
        self.start_connect()
        self.login()
        self.router_hosts = dhcp_hosts.DhcpHosts(self.router)
        self.hosts_dict = self.router_hosts.hosts
        self.dynamic()

    def pushbuttonbut1_2(self):
        self.windowbut1.close()
        self.windowshed_but.close()
        self.router_filter = filter.Filter(self.router)
        if self.router_filter.isblocked(self.Mui.comboBox.currentText(), 'sched'):
            self.uibut1.pushButton_2.setDisabled(True)
            self.uibut1.pushButton_3.setDisabled(True)
        else:
            self.buttonbut1_2()

    def buttonbut1_2(self):
        if self.router_filter.isblocked(self.Mui.comboBox.currentText(), 'block'):
            self.logger.debug('turn on internet "' + self.Mui.comboBox.currentText() + '" enable host in firewall')
            self.router_filter.delete_rule(self.Mui.comboBox.currentText(), 'block')
            self.uibut1.pushButton_2.setText("block inet")
            self.uibut1.pushButton_3.setDisabled(False)
            self.uibut1.pushButton_4.setDisabled(False)
        else:
            self.logger.debug('turn off internet "' + self.Mui.comboBox.currentText() + '" disable host in firewall')
            self.router_filter.forwardblock(self.Mui.comboBox.currentText(), 'block')
            self.uibut1.pushButton_2.setText("unblock inet")
            self.uibut1.pushButton_3.setDisabled(True)
            self.uibut1.pushButton_4.setDisabled(True)

    def pushbuttonbut1_3(self):
        self.windowbut1.hide()
        self.logger.debug('remove static lease host "' + self.Mui.comboBox.currentText() + '"')
        self.router_hosts.remove_static(self.Mui.comboBox.currentText())
        self.refresh()
        self.uimessage.label.setText('Удалено!\nНужно будет\nпереподключить\nустройства к сети'
                                     '\nдля дальнейшей\nработы!')
        self.uimessage.pushButton.clicked.connect(self.windowmessage.hide)
        self.windowmessage.show()

    def pushbuttonbut1_4(self):
        self.windowbut2.move(800, 300)
        self.windowbut2.setWindowTitle('Расписание')
        self.uibut2.pushButton.setText('Настроить')
        if self.router_filter.isblocked(self.Mui.comboBox.currentText(), 'sched'):
            self.logger.debug('Правила в firewall уже созданы')
            self.uibut2.pushButton_2.setDisabled(False)
            self.uibut2.pushButton_3.setDisabled(True)
            self.uibut2.pushButton_4.setDisabled(False)
        self.uibut2.pushButton_2.setText("Включить")
        self.uibut2.pushButton_3.setText("Выключить")
        self.uibut2.pushButton_4.setText('Удалить')
        self.windowbut1.close()
        self.windowbut2.show()

    def pushbuttonbut2_1(self):
        self.uished_but.pushButton.clicked.connect(self.set_time)
        self.date_en, self.date_dis, self.interval_en = self.show_current_sched_rules('Enable_1', 'Disable_1')
        self.date_en2, self.date_dis2, self.interval_en2 = self.show_current_sched_rules('Enable_2', 'Disable_2')
        if self.date_en:
            self.get_time(self.date_en, self.date_dis, self.uished_but.dateTimeEdit, self.uished_but.dateTimeEdit_3)
        if self.date_en2:
            self.get_time(self.date_en2, self.date_dis2, self.uished_but.dateTimeEdit_2, self.uished_but.dateTimeEdit_4)
        self.set_rbut(self.uished_but.radioButton, self.uished_but.radioButton_2, self.uished_but.radioButton_3,
                      self.interval_en)
        self.set_rbut(self.uished_but.radioButton_6, self.uished_but.radioButton_5, self.uished_but.radioButton_4,
                      self.interval_en2)
        self.windowshed_but.show()

    def show_current_sched_rules(self, first, second):
        date_en, interval = self.scheduler.show_shed(self.Mui.comboBox.currentText(), first)
        date_dis, interval = self.scheduler.show_shed(self.Mui.comboBox.currentText(), second)
        return date_en, date_dis, interval

    def get_time(self, de, dd, qdt1, qdt2):
        date_enable = QtCore.QDateTime(QtCore.QDate(de[2], de[1], de[0]), QtCore.QTime(de[3], de[4], de[5]))
        date_disable = QtCore.QDateTime(QtCore.QDate(dd[2], dd[1], dd[0]), QtCore.QTime(dd[3], dd[4], dd[5]))
        qdt1.setDateTime(date_enable)
        qdt2.setDateTime(date_disable)

    def set_rbut(self, but1, but2, but3, interval):
        if interval == '1d':
            but1.setChecked(True)
        elif interval == '1w':
            but2.setChecked(True)
        else:
            but3.setChecked(True)

    def set_time(self):
        self.Mui.pushButton.setText('wait...')
        self.Mui.pushButton.setDisabled(True)
        self.windowbut2.close()
        self.windowshed_but.close()
        QtCore.QTimer.singleShot(4000, self.unhide)
        if not self.router_filter.isblocked(self.Mui.comboBox.currentText(), 'sched'):
            self.router_filter.forwardblock(self.Mui.comboBox.currentText(), 'sched')
            self.router_filter.disable_rule(self.Mui.comboBox.currentText(), 'sched')
        self.uibut2.pushButton.setDisabled(True)
        self.uibut2.pushButton_2.setDisabled(False)
        self.uibut2.pushButton_3.setDisabled(True)
        self.uibut2.pushButton_4.setDisabled(False)
        if self.date_en:
            self.delete_old_rules('Enable_1', 'Disable_1')
        if self.date_en2:
            self.delete_old_rules('Enable_2', 'Disable_2')
        self.init_script('Enable_1', 'Disable_1')
        self.date_en = self.uished_but.dateTimeEdit.dateTime().toString(format('MM*dd/yyyy*hh:mm:ss'))
        self.date_dis = self.uished_but.dateTimeEdit_3.dateTime().toString(format('MM*dd/yyyy*hh:mm:ss'))
        self.interval_en = self.check_button(self.uished_but.radioButton, self.uished_but.radioButton_2)
        self.scheduler.make_sched(self.Mui.comboBox.currentText(), self.date_en, self.interval_en, 'Enable_1')
        self.scheduler.make_sched(self.Mui.comboBox.currentText(), self.date_dis, self.interval_en, 'Disable_1')
        if not self.time_disabeled_2:
            self.init_script('Enable_2', 'Disable_2')
            self.date_en2 = self.uished_but.dateTimeEdit_2.dateTime().toString(format('MM*dd/yyyy*hh:mm:ss'))
            self.date_dis2 = self.uished_but.dateTimeEdit_4.dateTime().toString(format('MM*dd/yyyy*hh:mm:ss'))
            self.interval_en2 = self.check_button(self.uished_but.radioButton_6, self.uished_but.radioButton_5)
            self.scheduler.make_sched(self.Mui.comboBox.currentText(), self.date_en2, self.interval_en2, 'Enable_2')
            self.scheduler.make_sched(self.Mui.comboBox.currentText(), self.date_dis2, self.interval_en2, 'Disable_2')

    def unhide(self):
        self.Mui.pushButton.setText('Изменить')
        self.Mui.pushButton.setDisabled(False)
        self.uibut2.pushButton.setText('Настроить')
        self.uibut2.pushButton.setDisabled(False)

    def init_script(self, first, second):
        if not self.wwscript.script_is_here(self.Mui.comboBox.currentText(), first):
            self.wwscript.make_script(self.Mui.comboBox.currentText(),
                                      self.hosts_dict[self.Mui.comboBox.currentText()]['address'], first, 'no')
            self.wwscript.make_script(self.Mui.comboBox.currentText(),
                                      self.hosts_dict[self.Mui.comboBox.currentText()]['address'], second, 'yes')

    def delete_old_rules(self, first, second):
        self.scheduler.remove_shed(self.Mui.comboBox.currentText(), first)
        self.scheduler.remove_shed(self.Mui.comboBox.currentText(), second)
        self.wwscript.remove_script(self.Mui.comboBox.currentText(), first)
        self.wwscript.remove_script(self.Mui.comboBox.currentText(), second)

    def check_button(self, rbut1, rbut2):
        if rbut1.isChecked():
            interval = '1d 00:00:00'
        elif rbut2.isChecked():
            interval = '7d 00:00:00'
        else:
            interval = '365d 00:00:00'
        return interval

    def pushbuttonbut2_2(self):
        self.change_stat('no')
        self.uibut2.pushButton_2.setDisabled(True)
        self.uibut2.pushButton_3.setDisabled(False)

    def change_stat(self, disable='yes'):
        self.scheduler.modify_shed(self.Mui.comboBox.currentText(), 'Enable_1', disable)
        self.scheduler.modify_shed(self.Mui.comboBox.currentText(), 'Disable_1', disable)
        self.scheduler.modify_shed(self.Mui.comboBox.currentText(), 'Enable_2', disable)
        self.scheduler.modify_shed(self.Mui.comboBox.currentText(), 'Disable_2', disable)

    def pushbuttonbut2_3(self):
        self.change_stat()
        self.uibut2.pushButton_2.setDisabled(False)
        self.uibut2.pushButton_3.setDisabled(True)

    def pushbuttonbut2_4(self):
        self.uibut2.pushButton.setText('wait...')
        self.uibut2.pushButton.setDisabled(True)
        self.Mui.pushButton.setText('wait...')
        self.Mui.pushButton.setDisabled(True)
        QtCore.QTimer.singleShot(4000, self.unhide)
        self.delete_old_rules('Enable_1', 'Disable_1')
        self.delete_old_rules('Enable_2', 'Disable_2')
        self.router_filter.delete_rule(self.Mui.comboBox.currentText(), 'sched')
        self.uibut2.pushButton_2.setDisabled(True)
        self.uibut2.pushButton_3.setDisabled(True)
        self.uibut2.pushButton_4.setDisabled(True)

    def refresh(self):
        self.logger.debug(' refresh button pressed')
        self.logger.debug(' Restart')
        self.Mui.comboBox.clear()
        self.Mui.label_2.setText('')
        self.Mui.label.setText('Выберите хост:')
        self.Mui.comboBox.show()
        self.start_connect()
        self.login()
        self.router_hosts = dhcp_hosts.DhcpHosts(self.router)
        self.hosts_dict = self.router_hosts.hosts
        self.set_combo_box()
        self.windowbut1.close()
        self.windowbut2.close()
        self.windowbut3.close()
        self.windowshed_but.close()

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
