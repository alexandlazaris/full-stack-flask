from flask import jsonify, render_template, request
from apiflask import APIFlask, Schema, abort
from apiflask.fields import Integer, String
import os
import sqlite3

TABLE_NAME = 'books'
DATABASE_NAME = 'main.db'

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

def get_data_single(query, params=None):
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

def create_book_table():
    print ('checking if table exists')
    result = get_data('SELECT name FROM sqlite_master')
    if result.__len__() == 0:
        print (f'table <{TABLE_NAME}> does not exist, creating now')
        run_query('CREATE TABLE IF NOT EXISTS books (id INTEGER PRIMARY KEY, title TEXT, author TEXT)')
        print (f"created new table: {TABLE_NAME}")
    else:
        print (f"<{TABLE_NAME}> table already exists")

app = APIFlask(__name__, title='Basic Flask API', version='1.0')
app.config['SYNC_LOCAL_SPEC'] = True
app.config['LOCAL_SPEC_PATH'] = 'openapi.json'

class Book(Schema):
    id = Integer(
        required=False
    )
    title = String()
    author = String()

@app.get('/')
def home():
    print('loading homepage')
    dbBooks = get_data('SELECT * FROM books ORDER BY id, title, author')
    print(dbBooks)
    books = []
    for dbBook in dbBooks:
        books.append({'id': dbBook[0], 'title': dbBook[1], 'author': dbBook[2]})
    return render_template('index.html', books=books)

@app.get('/books')
@app.output(Book(many=True), status_code=200, description='Fetch all book entries')
def get_books():
    data = get_data('SELECT * FROM books ORDER BY id, title, author')
    print(data)
    books = []
    for dbBook in data:
        books.append({'id': dbBook[0], 'title': dbBook[1], 'author': dbBook[2]})
    return books

@app.get('/book/<int:id>')
@app.output(Book(many=False), status_code=200, description='Fetch a single book by id')
def get_book_by_id(id):
    data = get_data('SELECT * FROM books WHERE id = ? ORDER BY id, title, author', (id,))
    print (len(data))
    if len(data) == 1:
        if data[0]:
            book = Book()
            book.title = data[0][1]
            book.author = data[0][2]
            book.id = id
            return book
    else:
        message = 'book id not found'
        abort(404, message, detail=id)    

@app.post('/book')
@app.output(Book,status_code=200, description='Create new book entry', example={'title': 'Captain Underpants', 'author': 'Dav Pilkey'})
def create_book():
    print (f'new book request body: {request.get_json()}')
    request_body = request.get_json()
    sql_command = '''INSERT INTO books (title, author) VALUES (?, ?)'''
    params = (request_body['title'], request_body['author'])
    run_query(sql_command, params)
    new_book_id = get_data('SELECT * FROM books ORDER BY id, title, author')
    # TODO: why god why, must do better
    id = new_book_id[new_book_id.__len__()-1]
    book = Book()
    book.author = request_body['author']
    book.title = request_body['title']
    book.id = id[0]
    return book

@app.delete('/book/<int:id>')
def delete_book_by_id(id):
    print (f'deleting book: {id}')
    run_query('DELETE FROM books WHERE id = ?', (id,))
    return jsonify({'message': 'book successfully deleted'}), 200 
    
@app.put('/book/<int:id>')
@app.output(Book,status_code=200)
def update_book_by_id(id):
    print (f'updating book: {request.get_json()}')
    request_body = request.get_json()
    get_data('SELECT * FROM books WHERE id = ?', (id,))
    data = get_data('SELECT * FROM books WHERE id = ?', (id,))
    if data:
        print('found book to update')    
        print(data)    
        run_query('UPDATE books SET title = ?, author = ? WHERE id = ?', (request_body['title'], request_body['author'], id))
        book = Book()
        book.author = request_body['author']
        book.title = request_body['title']
        book.id = id
        return book
    else:
        message = 'book id not found'
        abort(404, message, detail=id)
    
@app.delete('/books')
def delete_all_books():
    print (f'deleting all books')
    run_query('DELETE FROM books WHERE id >= 1')
    return jsonify({'message': 'all books successfully deleted'}), 200 

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

if __name__ == '__main__':
    check_db()
    create_book_table()
    app.run(debug=True, port=5000)
