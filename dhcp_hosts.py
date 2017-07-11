import io
import logging
from contextlib import redirect_stdout
from re import match


class DhcpHosts:
    def __init__(self, router):
        self.hosts = dict()
        self.router = router

    def talk(self, question):
        logging.debug('Отправляю запрос {}....'.format(question))
        with io.StringIO() as buf, redirect_stdout(buf):
            self.router.talk(["{}".format(question)])
            answer = buf.getvalue()
        if ">>> =message=no such command" in answer.split('\n') \
                or ">>> =message=no such command prefix" in answer.split('\n'):
            logging.debug('Получен ответ {}!'.format(answer))
            logging.debug('Введенный запрос не корректен!')
        else:
            logging.debug('Получен ответ {}!'.format(answer))
            return answer

    def get_host(self):
        for line in self.talk('/ip/dhcp-server/lease/print').split('\n'):
            list_id = list()
            if match('^.*=.id=.*$', line):
                item = match('^.*=.id=(.*)$', line).group(1)
            if match('^.*=host-name=.*$', line):
                list_id.append(item)
                self.hosts['{}'.format(match('^.*=host-name=(.*)$', line).group(1))] = list_id
        return self.hosts

    def make_static(self, hostname):
        for ID in self.hosts[hostname]:
            logging.debug('Задаем статику для {}, ID - {}'.format(hostname,ID))
            with io.StringIO() as buf, redirect_stdout(buf):
                self.router.writeSentence(['/ip/dhcp-server/lease/make-static', ID])
