import requests

def test_can_create_a_book():
    # Arrange
    base_url = "http://127.0.0.1:5000/book"
    title = 'a test book'
    author = 'a test author'
    payload = {'title': title, 'author': author}
    # Act
    response = requests.post(f'{base_url}', json=payload)
    # Assertion
    assert response.status_code == 200
    data = response.json() 
    print(data) 
    assert data['title'] == title
    assert data['author'] == author
    assert 'id' in data

def test_can_delete_all_books():
    # Arrange
    base_url = "http://127.0.0.1:5000/books"
    # Act
    response = requests.delete(f'{base_url}')
    # Assertion
    assert response.status_code == 200
    data = response.json() 
    print(data) 
    assert data['message'] 
