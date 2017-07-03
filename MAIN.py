import mikr_api
import conf
import sys
import logging
import logging.handlers
import io
from re import match
from contextlib import redirect_stdout

logging.basicConfig(filename='mikrotik.log', level=logging.DEBUG)


def start_connect():
    s = mikr_api.main(conf.r1_ipaddr)
    if not s:
        logging.critical('Соединение с mikrotik не установилась!')
        sys.exit()
    router = mikr_api.ApiRos(s)
    logging.debug('Соединение по сети прошло успешно')

    logging.debug('Попытка логина (авторизация)....')
    with io.StringIO() as buf, redirect_stdout(buf):
        router.login(conf.r1_login, conf.r1_passwd1)
        output = buf.getvalue()

    if ">>> =message=cannot log in" in output.split('\n'):
        logging.critical('Логин или пароль не верен!')
        sys.exit()

    return router


logging.debug('Start')
router = start_connect()






