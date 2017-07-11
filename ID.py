import logging

class Id:

    def __init__(self, router):
        self.choosed_policy = []
        self.id = None
        self.router = router

    def make(self, method, name):
        if self.choosed_policy == []:
            logging.debug('Не выбранна политика- установим по умолчанию!')
            self.choosed_policy = 'ftp', 'reboot', 'read', 'write', 'policy', 'test', 'password', 'sniff', 'sensitive', 'romon'
        a = ','
        self.id = self.router.get_item_id(['/system/{}/add'.format(method), '=name={}'.format(name),
                                      '=policy={}'.format(a.join(self.choosed_policy))])
        if not self.id:
            logging.warning('ID item не был возвращен!!!')
            self.id = self.item_id(method, name)
            logging.debug('Получен ID item {}....'.format(self.id))
        else:
            logging.debug('Получен ID item {}....'.format(self.id))

    def choose_policy(self, *args):
        policy_can = ['ftp', 'reboot', 'read', 'write', 'policy', 'test', 'password', 'sniff', 'sensitive', 'romon']
        if args:
            for policy in args:
                if policy in policy_can:
                    self.choosed_policy.append(policy)

    def item_id(self, method, name):
        return self.router.get_item_id(['/system/{}/print'.format(method), '?name={}'.format(name)])

