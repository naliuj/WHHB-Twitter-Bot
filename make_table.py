from flask_table import Table, Col
import db


class Item(object):
    def __init__(self, show, day, start, end, hosts):
        self.show = show
        self.day = day
        self.start = start
        self.end = end
        self.hosts = hosts

class ItemTable(Table):

    classes = ['table', 'table-striped', 'table-hover']
    show = Col('Show')
    day = Col('Day')
    start = Col('Start Time')
    end = Col('End Time')
    hosts = Col('Host(s)')

    def tr_format(self, item):
            return '<tr onclick="delete()">{}</tr>'


# Yields the name of each host
def host_calc(row):
    row = row[4:9]
    print(row)
    for i in range(0, 4):
        print(i)
        if str(row[i]) is not '':
            yield row[i]


# Puts the table together
def get_table():
    items = db.read()
    shows = []
    for row in items:
        hosts = ', '.join([i for i in host_calc(row)])
        shows.append(Item(row[0], row[1], row[2], row[3], hosts))

    table = ItemTable(shows)

    return table
