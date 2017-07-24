import same

"""

/system/scheduler/add
=name=test
=start-date=Oct/14/1993
=start-time=08:00:00
=interval=1d 00:00:00
=on-event=yestes

"""
class Scheduler(same.Same):

    def __init__(self, router):
        super().__init__(router)

    def make_shed(self, host, time):
        pass

