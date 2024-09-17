import sqlite3
import os

TABLE_NAME = 'books'
DATABASE_NAME = 'main.db'

def check_db():
    print(f"checking if db <{DATABASE_NAME}> exists")
    path = os.path.exists(DATABASE_NAME)
    if path:
        print(f"db <{DATABASE_NAME}> does exist")
        conn = sqlite3.connect(DATABASE_NAME)
        c = conn.cursor()
        c.execute('''SELECT name FROM sqlite_master WHERE type='table';''')
        result = c.fetchall()
        print(result)
    else:
        print(f"db <{DATABASE_NAME}> does not exist, creating now")
        conn = sqlite3.connect(DATABASE_NAME)
        c = conn.cursor()
        c.execute('''SELECT name FROM sqlite_master WHERE type='table';''')
        result = c.fetchall()
        print(result)
        conn.close()

def create_book_table():
    print ('checking if table exists')
    result = get_data('SELECT name FROM sqlite_master')
    if result.__len__() == 0:
        print (f'table <{TABLE_NAME}> does not exist, creating now')
        run_query('CREATE TABLE IF NOT EXISTS books (id INTEGER PRIMARY KEY, title TEXT, author TEXT)')
        print (f"created new table: {TABLE_NAME}")
    else:
        print (f"<{TABLE_NAME}> table already exists")

def run_query(query, params=None):
    conn = sqlite3.connect(DATABASE_NAME)
    try:
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        conn.commit()
    finally:
        conn.close()

def get_data(query, params=None):
    conn = sqlite3.connect(DATABASE_NAME)
    try:
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        return cursor.fetchall()
    finally:
        conn.close()

def get_books(id=None):
    if id:
        data = get_data('SELECT * FROM books WHERE id = ? ORDER BY id, title, author', (id,))
        return data
    else:
        data = get_data('SELECT * FROM books ORDER BY id, title, author')
        return data

def create_book(request):
    request_body = request.get_json()
    print (f'new book request body: {request_body}')
    sql_command = '''INSERT INTO books (title, author) VALUES (?, ?)'''
    params = (request_body['title'], request_body['author'])
    run_query(sql_command, params)

def delete_books(id=None):
    if id:
        run_query('DELETE FROM books WHERE id = ?', (id,))
    else:
        run_query('DELETE FROM books WHERE id >= 1')

