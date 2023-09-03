import sqlite3

connection = sqlite3.connect("hands_on.db", check_same_thread=False)


def init_db():
	cursor = connection.cursor()
	cursor.execute('''
		CREATE TABLE IF NOT EXISTS users (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			username TEXT NOT NULL UNIQUE,
			password TEXT NOT NULL
		)
	''')
	connection.commit()

def add_user(connection, username, password):
    cursor = connection.cursor()
    query = '''INSERT INTO users (username, password) VALUES (?, ?)'''
    cursor.execute(query, (username, password))
    connection.commit()

def get_all_users(connection):
	cursor = connection.cursor()
	query = 'SELECT * FROM users'
	cursor.execute(query)
	return cursor.fetchall()


