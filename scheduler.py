import same
import logging
from re import match

monts = {'01': 'Jan', '02': 'Feb', '03': 'Mar', '04': 'Apr', '05': 'May', '06': 'Jun', '07': 'Jul', '08': 'Aug',
         '09': 'Sep', '10': 'Oct', '11': 'Nov', '12': 'Dec'}

monts_rev = {'jan': '01', 'feb': '02', 'mar': '03', 'apr': '04', 'may': '05', 'jun': '06', 'jul': '07', 'aug': '08',
             'sep': '09', 'oct': '10', 'nov': '11', 'dec': '12'}


def make_day(input_date):
    day = monts[input_date.split('*')[0]] + '/' + input_date.split('*')[1]
    return day


class Scheduler(same.Same):
    def __init__(self, router):
        super().__init__(router)

    def make_sched(self, host, date, interv, method):
        self.make('/system/scheduler/add', '=name={}_'.format(method) + host,
                  '=start-date=' + make_day(date), '=start-time=' + date.split('*')[2],
                  '=interval=' + interv, '=on-event=Enable_' + host, '=disabled=yes')

    def remove_shed(self, host, method):
        shed_id = self.make('/system/scheduler/print', '?name={}_'.format(method) + host)
        if shed_id:
            self.make('/system/scheduler/remove', '=.id=' + shed_id)


    def show_shed(self, host, method):
        answer = self.getanswer('/system/scheduler/print', '?name={}_'.format(method) + host)
        logging.debug(answer)
        if ">>> !re" in answer.split('\n'):
            for line in answer.split('\n'):
                if match('^.*start-date=.*', line):
                    shed_startd = match('^.*start-date=(.*)', line).group(1)
                if match('^.*start-time=.*', line):
                    shed_startt = match('^.*start-time=(.*)', line).group(1)
                if match('^.*interval=.*', line):
                    shed_interv = match('^.*interval=(.*)', line).group(1)
            return [int(shed_startd.split('/')[1]), int(monts_rev[shed_startd.split('/')[0]]),
                    int(shed_startd.split('/')[2]), int(shed_startt.split(':')[0]),
                    int(shed_startt.split(':')[1]), int(shed_startt.split(':')[0])], shed_interv
        else:
            return False, False


    def disable_shed(self, host):
        pass

    def enable_shed(self, host):
        pass