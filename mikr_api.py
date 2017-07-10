#!/usr/bin/python3

import sys, posix, time, binascii, socket, select
import hashlib
import io

from contextlib import redirect_stdout
from re import match
import logging

logging.basicConfig(filename='mikrotik.log', level=logging.DEBUG)

class ApiRos:
    "Routeros api"

    def __init__(self, sk):
        self.sk = sk
        self.currenttag = 0

    def login(self, username, pwd):
        for repl, attrs in self.talk(["/login"]):
            chal = binascii.unhexlify((attrs['=ret']).encode('UTF-8'))
        md = hashlib.md5()
        md.update(b'\x00')
        md.update(pwd.encode('UTF-8'))
        md.update(chal)
        self.talk(["/login", "=name=" + username,
                   "=response=00" + binascii.hexlify(md.digest()).decode('UTF-8')])

    def talk(self, words):
        if self.writeSentence(words) == 0:
            return
        r = []
        while True:
            i = self.readSentence()
            if len(i) == 0:
                continue
            reply = i[0]
            attrs = {}
            for w in i[1:]:
                j = w.find('=', 1)
                if j == -1:
                    attrs[w] = ''
                else:
                    attrs[w[:j]] = w[j + 1:]
            r.append((reply, attrs))
            if reply == '!done':
                return r

    def writeSentence(self, words):
        ret = 0
        for w in words:
            self.writeWord(w)
            ret += 1
        self.writeWord('')
        return ret

    def readSentence(self):
        r = []
        while 1:
            w = self.readWord()
            if w == '':
                return r
            r.append(w)

    def readall(self):
        r = []
        while True:
            i = self.readSentence()
            if len(i) == 0:
                continue
            reply = i[0]
            attrs = {}
            for w in i[1:]:
                j = w.find('=', 1)
                if j == -1:
                    attrs[w] = ''
                else:
                    attrs[w[:j]] = w[j + 1:]
            r.append((reply, attrs))
            if reply == '!done':
                return r

    def writeWord(self, w):
        print(("<<< " + w))
        self.writeLen(len(w))
        self.writeStr(w)

    def readWord(self):
        ret = self.readStr(self.readLen())
        print((">>> " + ret))
        return ret

    def writeLen(self, l):
        if l < 0x80:
            self.writeStr(chr(l))
        elif l < 0x4000:
            l |= 0x8000
            self.writeStr(chr((l >> 8) & 0xFF))
            self.writeStr(chr(l & 0xFF))
        elif l < 0x200000:
            l |= 0xC00000
            self.writeStr(chr((l >> 16) & 0xFF))
            self.writeStr(chr((l >> 8) & 0xFF))
            self.writeStr(chr(l & 0xFF))
        elif l < 0x10000000:
            l |= 0xE0000000
            self.writeStr(chr((l >> 24) & 0xFF))
            self.writeStr(chr((l >> 16) & 0xFF))
            self.writeStr(chr((l >> 8) & 0xFF))
            self.writeStr(chr(l & 0xFF))
        else:
            self.writeStr(chr(0xF0))
            self.writeStr(chr((l >> 24) & 0xFF))
            self.writeStr(chr((l >> 16) & 0xFF))
            self.writeStr(chr((l >> 8) & 0xFF))
            self.writeStr(chr(l & 0xFF))

    def readLen(self):
        c = ord(self.readStr(1))
        if (c & 0x80) == 0x00:
            pass
        elif (c & 0xC0) == 0x80:
            c &= ~0xC0
            c <<= 8
            c += ord(self.readStr(1))
        elif (c & 0xE0) == 0xC0:
            c &= ~0xE0
            c <<= 8
            c += ord(self.readStr(1))
            c <<= 8
            c += ord(self.readStr(1))
        elif (c & 0xF0) == 0xE0:
            c &= ~0xF0
            c <<= 8
            c += ord(self.readStr(1))
            c <<= 8
            c += ord(self.readStr(1))
            c <<= 8
            c += ord(self.readStr(1))
        elif (c & 0xF8) == 0xF0:
            c = ord(self.readStr(1))
            c <<= 8
            c += ord(self.readStr(1))
            c <<= 8
            c += ord(self.readStr(1))
            c <<= 8
            c += ord(self.readStr(1))
        return c

    def writeStr(self, str):
        n = 0
        while n < len(str):
            r = self.sk.send(bytes(str[n:], 'UTF-8'))
            if r == 0:
                raise RuntimeError("connection closed by remote end")
            n += r

    def readStr(self, length):
        ret = ''
        while len(ret) < length:
            s = self.sk.recv(length - len(ret))
            if s == '':
                raise RuntimeError("connection closed by remote end")
            ret += s.decode('UTF-8', 'replace')
        return ret

    def get_item_id(self, question):
        logging.debug('Отправляю запрос {}'.format(question))
        with io.StringIO() as buf, redirect_stdout(buf):
            self.writeSentence(question)
            self.readall()
            answer = buf.getvalue()
        logging.debug('Получен ответ {}'.format(answer))
        if '>>> =message=failure: item with such name already exists' in answer.split('\n'):
            logging.warning('Указанный item уже существует!!!')
            return
        for line in answer.split('\n'):
            if match('^.*=ret=.*$', line):
                ID_ITEM = match('^.*=ret=(.*)$', line).group(1)
                return ID_ITEM
            if match('^.*=.id=.*$', line):
                ID_ITEM = match('^.*=.id=(.*)$', line).group(1)
                return ID_ITEM

def main(ipaddr):
    s = None
    for res in socket.getaddrinfo(ipaddr, "8728", socket.AF_UNSPEC, socket.SOCK_STREAM):
        af, socktype, proto, canonname, sa = res
        try:
            s = socket.socket(af, socktype, proto)
        except socket.error as msg:
            s = None
            continue
        try:
            s.connect(sa)
        except socket.error as msg:
            s.close()
            s = None
            print('could not open socket - {}'.format(msg))
            continue
        break
    if __name__ == '__main__' and s is None:
        sys.exit(1)

    return s

def interactive():
    s = main(sys.argv[1])
    apiros = ApiRos(s)
    apiros.login(sys.argv[2], sys.argv[3])

    inputsentence = []

    while True:
        r = select.select([s, sys.stdin], [], [], None)
        if s in r[0]:
            # something to read in socket, read sentence
            x = apiros.readSentence()

        if sys.stdin in r[0]:
            # read line from input and strip off newline
            l = sys.stdin.readline()
            l = l[:-1]

            # if empty line, send sentence and start with new
            # otherwise append to input sentence
            if l == '':
                apiros.writeSentence(inputsentence)
                inputsentence = []
            else:
                inputsentence.append(l)


if __name__ == '__main__':
    interactive()