from user_management.login_db import read
from flask_table import Table, Col


class Item(object):

    def __init__(self, username, role):
        self.username = username
        self.role = role


class ItemTable(Table):

    classes = ['table', 'table-striped', 'table-hover']
    username = Col('Username')
    role = Col('Account Type')


def get_table():
    items = read()
    users = []
    for row in items:
        users.append(Item(row[0], row[2]))

    table = ItemTable(users)

    return table