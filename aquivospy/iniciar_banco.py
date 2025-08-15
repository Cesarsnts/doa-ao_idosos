import sqlite3

SCHEMA = 'schemas.sql'

conn = sqlite3.connect('banco.db')

with open(SCHEMA) as f:
    conn.executescript(f.read())

conn.close()
