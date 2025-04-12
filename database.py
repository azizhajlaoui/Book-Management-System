import sqlite3
import hashlib
import secrets
import string

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
            
            # Create users table if not exists
            conn.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    salt TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    reset_token TEXT
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

    def _hash_password(self, password, salt=None):
        if salt is None:
            salt = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(16))
        password_hash = hashlib.sha256((password + salt).encode()).hexdigest()
        return password_hash, salt

    def register_user(self, username, password, email):
        # Register a new user
        password_hash, salt = self._hash_password(password)
        try:
            with self.connect() as conn:
                conn.execute('''
                    INSERT INTO users (username, password_hash, salt, email)
                    VALUES (?, ?, ?, ?)
                ''', (username, password_hash, salt, email))
                return True
        except sqlite3.IntegrityError:
            return False

    def verify_user(self, username, password):
        # Verify user credentials
        with self.connect() as conn:
            user = conn.execute('SELECT password_hash, salt FROM users WHERE username=?', (username,)).fetchone()
            if user:
                password_hash, salt = user
                verify_hash, _ = self._hash_password(password, salt)
                return password_hash == verify_hash
        return False

    def generate_reset_token(self, email):
        # Generate and store password reset token
        token = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(32))
        with self.connect() as conn:
            result = conn.execute('UPDATE users SET reset_token=? WHERE email=?', (token, email))
            if result.rowcount > 0:
                return token
        return None

    def reset_password(self, token, new_password):
        # Reset password using token
        with self.connect() as conn:
            user = conn.execute('SELECT id FROM users WHERE reset_token=?', (token,)).fetchone()
            if user:
                password_hash, salt = self._hash_password(new_password)
                conn.execute('''
                    UPDATE users 
                    SET password_hash=?, salt=?, reset_token=NULL 
                    WHERE id=?
                ''', (password_hash, salt, user[0]))
                return True
        return False

    def check_username_exists(self, username):
        # Check if username already exists
        with self.connect() as conn:
            result = conn.execute('SELECT 1 FROM users WHERE username=?', (username,)).fetchone()
            return bool(result)

    def check_email_exists(self, email):
        # Check if email already exists
        with self.connect() as conn:
            result = conn.execute('SELECT 1 FROM users WHERE email=?', (email,)).fetchone()
            return bool(result)