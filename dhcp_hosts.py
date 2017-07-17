import io
import time
import logging
from contextlib import redirect_stdout
from re import match


class DhcpHosts:
    def __init__(self, router):
        self.hosts = dict()
        self.router = router
        self.get_hosts()

    def talk(self, question):
        logging.debug(' Отправляю запрос {}....'.format(question))
        with io.StringIO() as buf, redirect_stdout(buf):
            self.router.talk(["{}".format(question)])
            answer = buf.getvalue()
        if ">>> =message=no such command" in answer.split('\n') \
                or ">>> =message=no such command prefix" in answer.split('\n'):
            logging.debug(' Получен ответ {}!'.format(answer))
            logging.debug(' Введенный запрос не корректен!')
        else:
            return answer

    def get_hosts(self):
        try:
            hosts_list = self.talk('/ip/dhcp-server/lease/print').split('>>> !re')
            hosts_list.remove('<<< /ip/dhcp-server/lease/print\n<<< \n')
            for host in range(0, len(hosts_list)):
                self.hosts[host] = {}
                for element in hosts_list[host].split('\n'):
                    if element == '>>> ' or element == '':
                        continue
                    elif element == '>>> !done':
                        break
                    self.hosts[host].update({element.split('=')[1]: element.split('=')[2]})
            self.hosts = {nhost['host-name']: nhost for nhost in self.hosts.values()}
            logging.info(' Хосты: {}'.format(self.hosts.keys()))
            logging.debug(':')
            logging.debug(self.hosts)
        except ValueError:
            logging.debug('Совсем нет Lease....')
            self.hosts = {'None': {'host-name': 'None'}}

    def make_static(self, *args):
        for arhost in args:
            if arhost in [kwhost['host-name'] for kwhost in self.hosts.values()]:
                logging.debug(' Задаем статику для {}, ID - {}'.format(arhost, self.hosts[arhost]['.id']))
                with io.StringIO() as buf, redirect_stdout(buf):
                    self.router.talk(['/ip/dhcp-server/lease/make-static', '=.id='+self.hosts[arhost]['.id']])
                    answer = buf.getvalue()
                    logging.debug(answer)

    def remove_static(self, *args):
        for arhost in args:
            if arhost in [kwhost['host-name'] for kwhost in self.hosts.values()]:
                logging.debug(' Удаляем lease для {}, ID - {}'.format(arhost, self.hosts[arhost]['.id']))
                with io.StringIO() as buf, redirect_stdout(buf):
                    self.router.talk(['/ip/dhcp-server/lease/remove', '=.id='+self.hosts[arhost]['.id']])
                    answer = buf.getvalue()
                    logging.debug(answer)

