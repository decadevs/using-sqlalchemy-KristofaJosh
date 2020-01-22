from interface import Interface
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

db = create_engine('postgresql+psycopg2://postgres:chrisjosh1@localhost/postgres')
base = declarative_base()
Session = sessionmaker(db)
session = Session()
base.metadata.create_all(db)


class Books(base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    books_id = Column(Integer)
    author = Column(String)
    title = Column(String)


class PostgresTableStorage(Interface):
    data = []

    def create(self, **kwargs):
        self.new_book = Books(books_id=kwargs['id'], author=kwargs['author'], title=kwargs['title'])
        session.add(self.new_book)
        session.commit()

    def fetch(self, **kwargs):
        books = session.query(Books)
        if len(kwargs) > 1:
            for book in books:
                if book.title == kwargs['title'] and book.author == kwargs['author']:
                    val = {'id': book.id, 'books_id': book.books_id, 'author': book.author, 'title': book.title}
                    self.data.append(val)
            return self.data

        else:
            val = [x for x in kwargs.values()][0]
            for book in books:
                if book.books_id == val or book.author == val:
                    val = {'id': book.id, 'books_id': book.books_id, 'author': book.author, 'title': book.title}
                    self.data.append(val)
            return self.data

    def all(self):
        books = session.query(Books)
        for book in books:
            val = {'id': book.id, 'books_id': book.books_id, 'author': book.author, 'title': book.title}
            self.data.append(val)
        return self.data

    def delete(self, **kwargs):
        # poi_to_delete = session.query(Books).filter(Books.books_id == 8).first()
        poi_to_delete = session.query(Books)
        if len(kwargs) > 1:
            for x in poi_to_delete:
                if x.author == kwargs['author'] and x.title == kwargs['title']:
                    session.delete(x)
                    self.data.append(x.books_id)
                    session.commit()
            return self.data
        else:
            val = [x for x in kwargs.values()][0]
            for x in poi_to_delete:
                if x.books_id == val or x.author == val:
                    session.delete(x)
                    self.data.append(x.books_id)
                    session.commit()
            return self.data