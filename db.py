import sqlite3


# Connect to database
def connect():
    conn = sqlite3.connect('shows.db')
    c = conn.cursor()
    return conn, c


# Commit changes to database
def commit(conn):
    conn.commit()


# Disconnect from database
def disconnect(conn):
    conn.close()


# Initialize database
def init():
    conn, c = connect()
    c.execute('''CREATE TABLE shows
                 (name text,
                 day text,
                 start text,
                 end text,
                 mem1 text,
                 mem2 text,
                 mem3 text,
                 mem4 text,
                 mem5 text)''')
    commit(conn)
    disconnect(conn)


# Adds a show to database
def add(info):
    conn, c = connect()
    # Verify that the slot isn't already taken by someone
    c.execute("SELECT * FROM shows WHERE day=? AND start=? AND end=?", (info[1], info[2], info[3]))
    data = c.fetchone()
    if data is None:
        c.execute("INSERT INTO shows VALUES (?,?,?,?,?,?,?,?,?)", info)
    commit(conn)
    disconnect(conn)


# Read information from that database
def read():
    conn, c = connect()
    c.execute("SELECT * FROM shows")
    return c.fetchall()
    disconnect(conn)


# Remove a single value from the database
def remove(slot):
    conn, c = connect()
    c.execute("DELETE FROM shows WHERE day=? AND start=? and end=?", (slot[0], slot[1], slot[2]))
    commit(conn)
    disconnect(conn)


# Clear the entire database
def clear():
    conn, c = connect()
    c.execute("DELETE FROM shows")
    commit(conn)
    disconnect(conn)
