from db import connect, disconnect, commit
from passlib.hash import sha256_crypt


# Initialize log in information table
def init():
    conn, c = connect()
    c.execute("CREATE TABLE users (username text, password text)")
    commit(conn)
    disconnect(conn)


# Adds a user
def add(info):
    print(info)
    conn, c = connect()
    c.execute("SELECT * FROM users WHERE username=?", (info[0],))
    data = c.fetchone()
    if data is None:
        c.execute("INSERT INTO users VALUES (?,?)", [info[0], sha256_crypt.encrypt(info[1])])
        commit(conn)
        disconnect(conn)
        return "success"
    else:
        return "username taken"


# Verify that a username matches a password
def verify(username, password):
    conn, c = connect()
    c.execute("SELECT * FROM users")
    users = c.fetchall()
    for user in users:
        if sha256_crypt.verify(password, user[1]) and user[0] == username:
            disconnect(conn)
            return True
        else:
            disconnect(conn)
    return False


# Removes a user
def remove(user):
    conn, c = connect()
    c.execute("DELETE FROM users WHERE username=?", (user,))
    commit(conn)
    disconnect(conn)


# Clears the table
def clear():
    conn, c = connect()
    c.execute("DELETE FROM users")