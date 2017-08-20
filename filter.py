import io
import dhcp_hosts
import logging
from contextlib import redirect_stdout
from re import match


class Filter:
    def __init__(self, router):
        self.router = router
        self.ids = dict()
        self.answer = None
        self.hosts_dict = dhcp_hosts.DhcpHosts.hosts

    def forwardblock(self, host, method):
        self.hosts_dict = dhcp_hosts.DhcpHosts.hosts
        with io.StringIO() as buf, redirect_stdout(buf):
            self.router.talk(['/ip/firewall/filter/add', '=chain=forward', '=action=reject',
                              '=reject-with=icmp-admin-prohibited',
                              '=comment=' + method + '_' + self.hosts_dict[host]['address'], '=place-before=0',
                              '=src-address=' + self.hosts_dict[host]['address']])
            answer = buf.getvalue()
            logging.debug(answer)

    def isblocked(self, host, method):
        self.hosts_dict = dhcp_hosts.DhcpHosts.hosts
        with io.StringIO() as buf, redirect_stdout(buf):
            self.router.talk(['/ip/firewall/filter/print', '?comment=' + method + '_'
                              + self.hosts_dict[host]['address']])
            self.answer = buf.getvalue()
            logging.debug(self.answer)
        if ">>> !re" in self.answer.split('\n'):
            for line in self.answer.split('\n'):
                if match('^.*\.id.*', line):
                    self.ids[host] = match('^.*\.id=(.*)', line).group(1)
            return True
        else:
            return False

    def disable_rule(self, host, method):
        self.hosts_dict = dhcp_hosts.DhcpHosts.hosts
        with io.StringIO() as buf, redirect_stdout(buf):
            self.router.talk(['/ip/firewall/filter/print', '?comment=' + method + '_'
                              + self.hosts_dict[host]['address']])
            self.answer = buf.getvalue()
            logging.debug(self.answer)
        if ">>> !re" in self.answer.split('\n'):
            for line in self.answer.split('\n'):
                if match('^.*\.id.*', line):
                    with io.StringIO() as buf, redirect_stdout(buf):
                        self.router.talk(['/ip/firewall/filter/set', '=.id=' + match('^.*\.id=(.*)', line).group(1),
                                          '=disabled=yes'])
                        disabled = buf.getvalue()
                        logging.debug(disabled)

    def delete_rule(self, host, method):
        self.hosts_dict = dhcp_hosts.DhcpHosts.hosts
        with io.StringIO() as buf, redirect_stdout(buf):
            self.router.talk(['/ip/firewall/filter/print', '?comment=' + method + '_'
                              + self.hosts_dict[host]['address']])
            self.answer = buf.getvalue()
            logging.debug(self.answer)
        if ">>> !re" in self.answer.split('\n'):
            for line in self.answer.split('\n'):
                if match('^.*\.id.*', line):
                    with io.StringIO() as buf, redirect_stdout(buf):
                        self.router.talk(['/ip/firewall/filter/remove', '=.id=' + match('^.*\.id=(.*)', line).group(1),])
                        deleted = buf.getvalue()
                        logging.debug(deleted)






