from inMemoryStorage import InMemoryStorage
from postgresTableStorage import PostgresTableStorage
from booksManager import BooksManager


in_memory_storage = InMemoryStorage()
postgres_table_storage = PostgresTableStorage()

# The way BooksManager will take in a storage option
books_manager = BooksManager(in_memory_storage)
# books_manager = BooksManager(postgres_table_storage)

# The way BooksManager will use the storage options internally
# BooksManager does not need to know the type of the storage option

# Create a new book record in the storage
book = books_manager.create(
    id=1,
    author="Aka",
    title="Python Introduction"
)

# Fetch books in the storage based on params
books = books_manager.fetch(id=1)
# print(books)
books = books_manager.fetch(author="Aka")
books = books_manager.fetch(title="Ruby", author="Aka")

# Fetch all books in the storage
books = books_manager.all()

# Delete books in the storage based on params
book_ids = books_manager.delete(id=1)
books_ids = books_manager.delete(author="Aka")
books_ids = books_manager.delete(title="Ruby", author="Aka")



