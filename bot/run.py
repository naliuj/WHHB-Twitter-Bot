from bot.twitter_auth import authenticate
from bot import today
import db
from make_table import host_calc
from random import choice


def get_show(day, time):
    show = db.show(day, time)
    hosts = [i for i in host_calc(show)]
    if len(hosts) == 2:
        hosts = ' and '.join(hosts)
    elif len(hosts) >= 3:
        hosts = ', '.join(hosts[0:len(hosts)-1]) + ', and {}'.format(hosts[-1])
    show_templates = ["Tune in to 99.9 FM now for {} with {}!".format(show[0], hosts),
                      "{} is now live with {} on 99.9 FM!".format(show[0], hosts)]
    if show is None:
        pass
    else:
        twit = authenticate()
        twit.update_status(choice(show_templates))

weekday, hour = today.now()

get_show(weekday, hour)
