import io
import logging
from contextlib import redirect_stdout
from re import match


class DhcpHosts:
    def __init__(self):
        self.hosts = dict()

    def talk(self, router, question):
        logging.debug('Отправляю запрос {}....'.format(question))
        with io.StringIO() as buf, redirect_stdout(buf):
            router.talk(["{}".format(question)])
            answer = buf.getvalue()
        if ">>> =message=no such command" in answer.split('\n') \
                or ">>> =message=no such command prefix" in answer.split('\n'):
            logging.debug('Получен ответ {}!'.format(answer))
            logging.debug('Введенный запрос не корректен!')
        else:
            logging.debug('Получен ответ {}!'.format(answer))
            return answer

    def get_host(self, router):
        for line in self.talk(router, '/ip/dhcp-server/lease/print').split('\n'):
            list_id = list()
            if match('^.*=.id=.*$', line):
                item = match('^.*=.id=(.*)$', line).group(1)
            if match('^.*=host-name=.*$', line):
                list_id.append(item)
                self.hosts['{}'.format(match('^.*=host-name=(.*)$', line).group(1))] = list_id
        return self.hosts

    def make_static(self, router, hostname):
        for ID in self.hosts[hostname]:
            logging.debug('Задаем статику для {}, ID - {}'.format(hostname,ID))
            with io.StringIO() as buf, redirect_stdout(buf):
                router.writeSentence(['/ip/dhcp-server/lease/make-static', ID])
        return True


def main(router):

    host_dict = DhcpHosts()
    host_dict.get_host(router)

    if len(host_dict.hosts) > 0:
        logging.debug('Построен словарь хостов {}'.format(host_dict.hosts))
    else:
        logging.debug('Хостов нет')
    return  host_dict