import same


class Scripts(same.Same):

    def __init__(self, router):
        super().__init__(router)

    def make_script(self, host, addr, method, disabled='yes'):
        self.remove_script(host, method)
        self.make('/system/script/add', '=name={}_'.format(method) + host,
                  '=source=: ip firewall filter {{ set [find comment=sched_{}] '
                  'disabled={}}}'.format(addr, disabled))

    def remove_script(self, host, method):
        script_id = self.make('/system/script/print', '?name={}_'.format(method) + host)
        if script_id:
            self.make('/system/script/remove', '=.id='+script_id)

    def script_is_here(self, host, method):
        return self.make('/system/script/print', '?name={}_'.format(method) + host)
