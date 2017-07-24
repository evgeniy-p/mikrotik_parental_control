import logging
import io
from contextlib import redirect_stdout


class Same:

    def __init__(self, router):
        self.router = router

    def make(self, *args):
        with io.StringIO() as buf, redirect_stdout(buf):
            if not self.router.talk(args):
                logging.debug('Already exist')
            answer = buf.getvalue()
            logging.debug(answer)