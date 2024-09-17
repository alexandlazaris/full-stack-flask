from apiflask import Schema
from apiflask.fields import Integer, String
class Book(Schema):
    id = Integer(
        required=False
    )
    title = String()
    author = String()