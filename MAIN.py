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


def talk(router, question):
    logging.debug('Отправляю запрос {}....'.format(question))
    with io.StringIO() as buf, redirect_stdout(buf):
        router.talk(["{}".format(question)])
        answer = buf.getvalue()
    if ">>> =message=no such command" in answer.split('\n') \
            or ">>> =message=no such command prefix" in answer.split('\n'):
        logging.debug('Получен ответ {}!'.format(answer))
        logging.debug('Введенный запрос не корректен!')
    else:
        #logging.debug('Получен ответ {}!'.format(answer))
        logging.debug('Получен ответ....')
        return answer


def add_item(router, question):
    logging.debug('Отправляю запрос {}....'.format(question))
    with io.StringIO() as buf, redirect_stdout(buf):
        router.writeSentence(question)
        router.readSentence()
        answer = buf.getvalue()
    if '>>> =message=failure: item with such name already exists' in answer.split('\n'):
        logging.warning('Указанный item уже существует!!!')
        return
    for line in answer.split('\n'):
        if match('^.*=ret=.*$', line):
            ID_ITEM = match('^.*=ret=(.*)$', line).group(1)
            return ID_ITEM


policy_can = ['ftp', 'reboot', 'read', 'write', 'policy', 'test', 'password', 'sniff', 'sensitive', 'romon']



logging.debug('Start')
router = start_connect()
login(router)
hosts = dict()
for line in talk(router, '/ip/dhcp-server/lease/print').split('\n'):
    list_item = []
    if match('^.*=.id=.*$', line):
        item = match('^.*=.id=(.*)$', line).group(1)
    if match('^.*=host-name=.*$', line):
        list_item.append(item)
        hosts['{}'.format(match('^.*=host-name=(.*)$', line).group(1))] = list_item

if len(hosts) > 0:
    logging.debug('Построен словарь хостов {}'.format(hosts))
else:
    logging.debug('Хостов нет')


"""
key = input("Какой hostname?")

for item in hosts[key]:
    router.writeSentence(['/ip/dhcp-server/lease/make-static', item])
"""



name_script = 'test234'

choosed_policy = policy_can[2] + ',' + policy_can[3]
id_script1 = add_item(router, ['/system/script/add', '=name={}'.format(name_script), '=policy={}'.format(choosed_policy)])
if not id_script1:
    logging.warning('ID item не был возвращен!!!')
else:
    logging.debug('Получен ID item {}....'.format(id_script1))






