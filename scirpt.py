import io
import logging

class Scripts:

    def __init__(self):
        self.choosed_policy = []
        self.id = None

    def script(self, router, name):
        if self.choosed_policy == []:
            logging.debug('Не выбранна политика- установим по умолчанию!')
            self.choosed_policy = 'ftp', 'reboot', 'read', 'write', 'policy', 'test', 'password', 'sniff', 'sensitive', 'romon'
        a = ','
        self.id = router.get_item_id(['/system/script/add', '=name={}'.format(name),
                                      '=policy={}'.format(a.join(self.choosed_policy))])
        if not self.id:
            logging.warning('ID item не был возвращен!!!')
            self.id = self.find_script_name(name)
            logging.debug('Получен ID item {}....'.format(self.id))
        else:
            logging.debug('Получен ID item {}....'.format(self.id))

    def choose_policy(self, *args):
        policy_can = ['ftp', 'reboot', 'read', 'write', 'policy', 'test', 'password', 'sniff', 'sensitive', 'romon']
        if args:
            for policy in args:
                if policy in policy_can:
                    self.choosed_policy.append(policy)

    def find_script_name(self, name):
        return router.get_item_id(['/system/script/print', '?name={}'.format(name)])


