import same


class Scripts(same.Same):

    def __init__(self, router):
        super().__init__(router)

    def make_script(self, host, addr):
        self.make('/system/script/add', '=name=by_api_1_' + host,
                  '=source=: ip firewall filter add chain=forward comment={} place-before=0'.format(host))
        self.make('/system/script/add', '=name=by_api_2_' + host,
                  '=source=: ip firewall filter {{ set [find comment={}] '
                  'action=reject out-interface=all-ethernet src-address={}}}'.format(host, addr))
