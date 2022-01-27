from mongoengine import Document, DateTimeField, StringField, IntField


class Book(Document):
    bid = IntField(required=True, unique=True)
    name = StringField(required=True, max_length=50)
    author = StringField(required=True, max_length=50)
    published = DateTimeField()
