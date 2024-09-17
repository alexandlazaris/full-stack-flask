from flask import jsonify, render_template, request
from apiflask import APIFlask, abort
from view.db_actions import check_db, create_book_table, get_books, create_book, delete_books
from model.book import Book

app = APIFlask(__name__, title='Basic Flask API', version='1.0')
app.config['SYNC_LOCAL_SPEC'] = True
app.config['LOCAL_SPEC_PATH'] = 'openapi.json'

@app.get('/')
def home():
    print('loading homepage')
    data = get_books()
    books = []
    for book in data:
        books.append({'id': book[0], 'title': book[1], 'author': book[2]})
    return render_template('index.html', books=books)

@app.get('/books')
@app.output(Book(many=True), status_code=200, description='Fetch all book entries')
def get_all():
    data = get_books()
    print(data)
    books = []
    for book in data:
        books.append({'id': book[0], 'title': book[1], 'author': book[2]})
    return books

@app.get('/book/<int:id>')
@app.output(Book(many=False), status_code=200, description='Fetch a single book by id')
def get(id):
    data = get_books(id)
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
def post():
    book = create_book(request)
    request_body = request.get_json()
    all_books = get_books()
    # TODO: why god why, must do better
    new_book_id = all_books[all_books.__len__()-1]
    book = Book()
    book.id = new_book_id[0]
    book.title = request_body['title']
    book.author = request_body['author']
    return book

@app.delete('/book/<int:id>')
def delete_book_by_id(id):
    print (f'deleting book: {id}')
    delete_books(id)
    return jsonify({'message': 'book successfully deleted'}), 200 
    
# @app.put('/book/<int:id>')
# @app.output(Book,status_code=200)
# def update_book_by_id(id):
#     print (f'updating book: {request.get_json()}')
#     request_body = request.get_json()
#     get_data('SELECT * FROM books WHERE id = ?', (id,))
#     data = get_data('SELECT * FROM books WHERE id = ?', (id,))
#     if data:
#         print('found book to update')    
#         print(data)    
#         run_query('UPDATE books SET title = ?, author = ? WHERE id = ?', (request_body['title'], request_body['author'], id))
#         book = Book()
#         book.author = request_body['author']
#         book.title = request_body['title']
#         book.id = id
#         return book
#     else:
#         message = 'book id not found'
#         abort(404, message, detail=id)
    
@app.delete('/books')
def delete_all_books():
    print (f'deleting all books')
    delete_books()
    return jsonify({'message': 'all books successfully deleted'}), 200 


if __name__ == '__main__':
    check_db()
    create_book_table()
    app.run(debug=True, port=5000)
