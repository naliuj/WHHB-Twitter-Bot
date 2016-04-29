import sqlite3


# Connect to database
def connect():
    conn = sqlite3.connect(r'C:\Users\Julian\Documents\GitHub\WHHB-Twitter-Bot\data.db')
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
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    shows = []
    for day in days:
        c.execute("SELECT * FROM shows WHERE day=? ORDER BY start", (day,))
        shows += c.fetchall()
    return shows
    disconnect(conn)


# Returns the show data for a certain timeslot
def show(day, time):
    conn, c = connect()
    if time > 12:
        time -= 12
    elif time == 0:
        time = 12
    c.execute("SELECT * FROM shows WHERE day=? AND start=?", (day, "{}:00".format(time)))
    data = c.fetchone()
    if data is None:
        disconnect(conn)
        return None
    else:
        disconnect(conn)
        return data


# Remove a single value from the database
def remove(slot):
    conn, c = connect()
    c.execute("DELETE FROM shows WHERE day=? AND start=? AND end=?", (slot[0], slot[1], slot[2]))
    commit(conn)
    disconnect(conn)


# Clear the entire database
def clear():
    conn, c = connect()
    c.execute("DELETE FROM shows")
    commit(conn)
    disconnect(conn)
