import sqlite3

def connect_to_db():
    conn = sqlite3.connect('Vortex.db')
    return conn

def connect_to_roles_db():
    conn = sqlite3.connect('roles.db')
    return conn
