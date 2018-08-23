import sqlite3

path_to_file = 'database.db'

def open_connection(path=path_to_file):
    return sqlite3.connect(path)

def close_connection(conn):
    conn.commit()
    conn.close()

def execute_statement(statement, conn):
    c = conn.cursor()
    if isinstance(statement, tuple):
        c.execute(statement[0], statement[1])
    else:
        c.execute(statement)

def fetchone(statement, conn):
    c = conn.cursor()
    if isinstance(statement, tuple):
        c.execute(statement[0], statement[1])
    else:
        c.execute(statement)
    return c.fetchone()

def fetchall(statement, conn):
    c = conn.cursor()
    if isinstance(statement, tuple):
        c.execute(statement[0], statement[1])
    else:
        c.execute(statement)
    return c.fetchall()
