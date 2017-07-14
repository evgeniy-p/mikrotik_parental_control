import io
import time
import logging
from contextlib import redirect_stdout
from re import match


class DhcpHosts:
    def __init__(self, router):
        self.hosts = dict()
        self.router = router

    def talk(self, question):
        logging.debug(time.ctime() + ' Отправляю запрос {}....'.format(question))
        with io.StringIO() as buf, redirect_stdout(buf):
            self.router.talk(["{}".format(question)])
            answer = buf.getvalue()
        if ">>> =message=no such command" in answer.split('\n') \
                or ">>> =message=no such command prefix" in answer.split('\n'):
            logging.debug(time.ctime() + ' Получен ответ {}!'.format(answer))
            logging.debug(time.ctime() + ' Введенный запрос не корректен!')
        else:
            return answer

    def get_hosts(self):
        hosts_list = self.talk('/ip/dhcp-server/lease/print').split('>>> !re')
        hosts_list.remove('<<< /ip/dhcp-server/lease/print\n<<< \n')
        for host in range(0, len(hosts_list)):
            self.hosts[host] = {}
            for element in hosts_list[host].split('\n'):
                if element == '>>> ' or element == '':
                    continue
                elif element == '>>> !done':
                    break
                self.hosts[host].update({element.split('=')[1]:element.split('=')[2]})

        for host in range(0, len(self.hosts)):
            self.hosts[self.hosts[host]['host-name']] = self.hosts[host]
            self.hosts.pop(host)
        logging.info(time.ctime() + ' Хосты: {}'.format(self.hosts.keys()))
        logging.debug(time.ctime() + ':')
        logging.debug(self.hosts)
        return self.hosts

    def make_static(self, **kwargs):
        if 'host-name' in kwargs:
            logging.debug(time.ctime() + ' Задаем статику для {}, ID - {}'.format(kwargs['host-name'], kwargs['.id']))
            with io.StringIO() as buf, redirect_stdout(buf):
                self.router.writeSentence(['/ip/dhcp-server/lease/make-static', kwargs['.id']])

    def remove_static(self, hostname):
        pass