import sqlite3
#abrindo uma conexão
conn = sqlite3.connect('banco.db')

SCHEMA ='schemas.sql'

with open (SCHEMA) as f:
    conn.executescript(f.read() )

conn.close()
