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
        print(self.hosts)

        return self.hosts

    def make_static(self, hostname):
        for ID in self.hosts[hostname]:
            logging.debug('Задаем статику для {}, ID - {}'.format(hostname,ID))
            with io.StringIO() as buf, redirect_stdout(buf):
                self.router.writeSentence(['/ip/dhcp-server/lease/make-static', ID])
