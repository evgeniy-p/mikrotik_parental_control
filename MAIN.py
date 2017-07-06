import mikr_api
import dhcp_hosts
#import scirpt
import conf
import sys
import logging
import logging.handlers
import io
from re import match
from contextlib import redirect_stdout

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
router_host = dhcp_hosts.main(router)
#router_host.make_static(router, 'cent_2')

#choosed_policy =


