"""
Напишите класс, реализующий функциональность маршрутизатора.
Атрибуты класса должны включать:
1. Таблицу интерфейсов - словарь вида
{'fa0/0':[address, mask], 'serial 0/0':[address, mask] и т.д.}
2. Таблицу маршрутизации - список вида
[[dstaddr, dstmask, nexthop],
[dstaddr, dstmask, nexthop],
[dstaddr, dstmask, nexthop]]

Методы класса:
ipAddr('interface', 'address', 'mask')
Присваивание адреса интерфейсу, адрес и маска - в точечно-десятичной нотации
ipRoute('destinationAddress', 'destinationMask', 'nextHopAddress')
Добавление маршрута
listIntr()
Выводит список интерфейсов
listRoutes()
Выводит таблицу маршрутизации

route(dstaddr)
Возвращает кортеж вида: выходной интерфейс, адрес следующего перехода
"""
from re import match
import ipaddress


def test_mask2(mask):
    liter1 = mask.split('.')
    liter = list()
    for i in liter1:
        liter.append(int(i))
    loct = liter[:]

    for i in liter:
        loct.remove(i)
        if i == 0:
            for m in loct:
                if m > 0:
                    return False

    mask_can = [128, 192, 224, 240, 248, 252, 254]

    if 0 < liter[0] < 255:
        if liter[1] == 0 and liter[2] == 0 and liter[3] == 0 and liter[0] in mask_can:
            return True
        else:
            return False
    else:
        if 0 < liter[1] < 255:
            if liter[2] == 0 and liter[3] == 0 and liter[1] in mask_can:
                return True
            else:
                return False
        else:
            if 0 < liter[2] < 255:
                if liter[3] == 0 and liter[2] in mask_can:
                    return True
                else:
                    return False
            else:
                if 0 < liter[3] < 255:
                    if liter[3] in mask_can:
                        return True
                    else:
                        return False
                else:
                    return True


def test_mask1(mask):
    if not type(mask) == 'string':
        print("mask not correct!!!\nformat: '255.255.255.255' ")
        return False
    if not match('^(\d{1,3}).(\d{1,3}).(\d{1,3}).(\d{1,3})$', mask):
        print("mask not correct!!!\nformat: 255.255.255.255")
        return False
    a, b, c, d = match('^(\d{1,3}).(\d{1,3}).(\d{1,3}).(\d{1,3})$', mask).group(1, 2, 3, 4)
    if 0 <= int(a) <= 255 and 0 <= int(b) <= 255 and 0 <= int(c) <= 255 and 0 <= int(d) <= 255:
        if test_mask2(mask):
            return True
        else:
            print("mask not correct!!!\nformat: '255.255.255.255' ")
            return False
    else:
        print("mask not correct!!!"
              "\nformat: 255.255.255.255")
        return False


def test_ipadrr(ip):
    if not match('^(\d{1,3}).(\d{1,3}).(\d{1,3}).(\d{1,3})$', ip):
        print("ip addr not correct!!!")
        return False
    a, b, c, d = match('^(\d{1,3}).(\d{1,3}).(\d{1,3}).(\d{1,3})$', ip).group(1, 2, 3, 4)
    if 0 <= int(a) <= 255 and 0 <= int(b) <= 255 and 0 <= int(c) <= 255 and 0 <= int(d) <= 255:
        return True
    else:
        print("ip addr not correct!!!")
        return False


def mask_to_bin(mask):
    length = 0
    mask_oct = mask.split('.')
    for i in mask_oct:
        mask_oct[mask_oct.index(i)] = list('{:08b}'.format(int(i)))
    for a in mask_oct:
        for b in a:
            if b == '1':
                length += 1
    return str(length)


def find_subnet(ipaddr, mask):
    mask_oct = mask.split('.')
    ipaddr_oct = ipaddr.split('.')
    for i in mask_oct:
        mask_oct[mask_oct.index(i)] = list('{:08b}'.format(int(i)))
    for n in ipaddr_oct:
        ipaddr_oct[ipaddr_oct.index(n)] = list('{:08b}'.format(int(n)))
    for m in range(0, 4):
        for k in range(0, 8):
            if mask_oct[m][k] == '0':
                ipaddr_oct[m][k] = '0'
    for b in ipaddr_oct:
        sub_oct = ''
        for c in b:
            sub_oct += c
        sub_oct = str(int(sub_oct, 2))
        ipaddr_oct[ipaddr_oct.index(b)] = sub_oct

    str_sub = ''

    for d in ipaddr_oct:
        str_sub += d + '.'

    return str_sub[:-1]


class Router:
    def __init__(self):
        self.iftable = {'serial': ['no ip addr', 'mask'], 'fa0/0': ['no ip addr', 'mask'],
                        'fa0/1': ['no ip addr', 'mask'], 'fa0/2': ['no ip addr', 'mask'],
                        'fa1/0': ['no ip addr', 'mask'], 'fa1/1': ['no ip addr', 'mask'],
                        'fa1/2': ['no ip addr', 'mask']}
        self.route_table = []

    def ipAddr(self, iface, addr, mask):
        if iface in self.iftable.keys() and test_ipadrr(addr) and test_mask1(mask):
            self.iftable[iface] = [addr, mask]
            self.ipRoute(find_subnet(addr, mask), mask, ipaddress.ip_network(find_subnet(addr, mask) + '/' \
                    + mask_to_bin(mask)).broadcast_address.__str__())
        else:
            print("Введенные данные не корректны!!!\nInterfaces:")
            self.listIntr()

    def ipRoute(self, dst, dmask, nHop):
        if not test_ipadrr(dst) or not test_ipadrr(nHop):
            print('Введенный адрес не корректен!!\nFormat 10.128.0.1')
            return
        if not test_mask1(dmask):
            print ('try again')
            return
        if not self.check_nhope_have_int(nHop):
            print('no interface connected to this nHop,aborted')
            return
        if not [dst, dmask, nHop] in self.route_table:
            route = list()
            route.append(dst)
            route.append(dmask)
            route.append(nHop)
            return self.route_table.append(route)
        else:
            print("such route already exist")
            return

    def listIntr(self):
        for i in sorted(self.iftable.keys()):
            joined = '/'
            print('{} - {}'.format(i, joined.join(self.iftable[i])))

    def listRoutes(self):
        for i in self.route_table:
            print(i)

    def route(self, dst):
        if not test_ipadrr(dst):
            print('Введенный ip адрес не корректный!!!\nFormat 10.128.0.1')
            return
        nHop = self.has_ip_route(dst)
        if nHop:
            if not self.check_nhope_have_int(nHop):
                print('no interface connected to this destination,aborted')
                return
        else:
            print('no route to this destination,aborted')
            return

        return (self.check_nhope_have_int(nHop), self.has_ip_route(dst))

    def check_nhope_have_int(self, dst):
        for i in self.iftable:
            if self.iftable[i][0] != 'no ip addr' and self.iftable[i][1] != 'mask':
                subnet_int = find_subnet(self.iftable[i][0], self.iftable[i][1]) + '/' \
                             + mask_to_bin(self.iftable[i][1])
                if ipaddress.IPv4Address(dst) in ipaddress.ip_network(subnet_int):
                    return i
        return

    def has_ip_route(self, dst):
        for i in self.route_table:
            if i[1] == '255.255.255.255':
                if i[0] == dst:
                    return i[2]
            else:
                subnet_int = find_subnet(i[0], i[1]) + '/' + mask_to_bin(i[1])
                if ipaddress.IPv4Address(dst) in ipaddress.ip_network(subnet_int):
                    return i[2]
        return False



if __name__ == "__main__":
    Mikr = Router()
    Mikr.ipAddr('fa0/0', '192.168.3.1', '255.255.0.0')
    Mikr.ipRoute('192.168.2.0', '255.255.255.255', '192.168.2.0')
    Mikr.listRoutes()
    print(Mikr.route('192.168.2.0'))



