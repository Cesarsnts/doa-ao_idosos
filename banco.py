#parte que estava no app.py
import sqlite3
#abrindo uma conexão
conn = sqlite3.connect('banco.db')

SCHEMA ='schemas.sql'
#executar instrução de criação de tabelas(s)

with open (SCHEMA) as f:
    conn.executescript(f.read() )

conn.close()

#insert
import sqlite3

conn = sqlite3.connect('banco.db')

SQL="INSERT INTO users (nome) values (?)"

nome = 'Jaci linda'

conn.execute(SQL,(nome,))
conn.commit()

conn.close()
