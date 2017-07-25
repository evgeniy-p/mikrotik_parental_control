import logging
import io
from contextlib import redirect_stdout
from re import match


class Same:

    def __init__(self, router):
        self.router = router

    def make(self, *args):
        with io.StringIO() as buf, redirect_stdout(buf):
            if not self.router.talk(args):
                logging.debug('Already exist')
            self.answer = buf.getvalue()
            logging.debug(self.answer)
            if ">>> !re" in self.answer.split('\n'):
                for line in self.answer.split('\n'):
                    if match('^.*\.id.*', line):
                        return match('^.*\.id=(.*)', line).group(1)
            else:
                return False

    def getanswer(self, *args):
        with io.StringIO() as buf, redirect_stdout(buf):
            self.router.talk(args)
            return buf.getvalue()
