import sqlite3

class BookDatabase:
    def __init__(self, db_name='books.db'):
        # Initialize database connection and create table
        self.db_name = db_name
        self._create_table()  # Create table on instantiation
    
    def _create_table(self):
        # Create books table if not exists
        with self.connect() as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS books (
                    id INTEGER PRIMARY KEY,       -- Auto-incrementing ID
                    title TEXT NOT NULL,          -- Book title
                    author TEXT NOT NULL,         -- Book author
                    year INTEGER,                 -- Publication year
                    isbn TEXT UNIQUE              -- Unique ISBN number
                )
            ''')
    
    def connect(self):
        # Create new database connection
        return sqlite3.connect(self.db_name)
    
    def add_book(self, title, author, year, isbn):
        # Insert new book record
        with self.connect() as conn:
            conn.execute('''
                INSERT INTO books (title, author, year, isbn)
                VALUES (?, ?, ?, ?)  -- Parameterized query for safety
            ''', (title, author, year, isbn))
    
    def get_books(self):
        # Retrieve all books from database
        with self.connect() as conn:
            return conn.execute('SELECT * FROM books').fetchall()
    
    def update_book(self, book_id, title, author, year, isbn):
        # Update existing book record
        with self.connect() as conn:
            conn.execute('''
                UPDATE books 
                SET title=?, author=?, year=?, isbn=?
                WHERE id=?  -- Update specific book by ID
            ''', (title, author, year, isbn, book_id))
    
    def delete_book(self, book_id):
        # Delete book by ID
        with self.connect() as conn:
            conn.execute('DELETE FROM books WHERE id=?', (book_id,))