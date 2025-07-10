import sqlite3

#insert

conn = sqlite3.connect('banco.db')

SQL="INSERT INTO users (nome) values (?)"

nome = 'Jaci linda'

conn.execute(SQL,(nome,))
conn.commit()

conn.close()