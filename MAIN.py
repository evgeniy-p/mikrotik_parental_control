import mikr_api
import dhcp_hosts
import scirpt
import scheduler
import conf
import sys
import logging
import io
import widget
from contextlib import redirect_stdout
from PyQt5.QtWidgets import QApplication, QMainWindow


logging.basicConfig(filename='mikrotik.log', level=logging.WARNING)


def start_connect():
    s = mikr_api.main(conf.r1_ipaddr)
    if not s:
        logging.critical('Соединение с mikrotik не установилась!')
        sys.exit()
    router = mikr_api.ApiRos(s)
    logging.debug('Соединение по сети прошло успешно')

    return router


def login(mikrot):
    logging.debug('Попытка логина (авторизация)....')
    with io.StringIO() as buf, redirect_stdout(buf):
        mikrot.login(conf.r1_login, conf.r1_passwd1)
        output = buf.getvalue()

    if ">>> =message=cannot log in" in output.split('\n'):
        logging.critical('Логин или пароль не верен!')
        sys.exit()
    logging.debug('Логин прошел успешно')

policy_can = ['ftp', 'reboot', 'read', 'write', 'policy', 'test', 'password', 'sniff', 'sensitive', 'romon']


logging.debug('Start')
router = start_connect()
login(router)

# обращаемся к классу, по которому можно получить список хостов, а также задать статику и т.п
router_host = dhcp_hosts.DhcpHosts(router)
"""
hosts = router_host.get_host()
if len(hosts) > 0:
    logging.debug('Построен словарь хостов {}'.format(hosts))
else:
    logging.debug('Хостов нет')
router_host.make_static(router, 'cent_2')
"""
# Обращаемся к классу, по которому можно создать скрипт и получить его id для дальнейшего управления
script_id = scirpt.Scripts(router)
#script_id.choose_policy(policy_can[3], policy_can[2])
#script_id.make('script', 'test_script32')
#id1 = script_id.id

# Обращаемся к классу, по которому можно создать правило расписания и получить его id для дальнейшего управления
scheld_id = scheduler.Scheduler(router)
#scheld_id.choose_policy(policy_can[3], policy_can[2])
#scheld_id.make('scheduler', 'test_scheld')
#id2 = scheld_id.id

app = QApplication(sys.argv)
window = QMainWindow()
ui = widget.Ui_MainWindow()
ui.setupUi(window)

window.show()
sys.exit(app.exec_())