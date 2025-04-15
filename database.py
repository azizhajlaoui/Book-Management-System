import mysql.connector
import hashlib
import secrets
import string

class BookDatabase:
    def __init__(self, user, password, host='localhost', database='books_db'):
        self.user = user
        self.password = password
        self.host = host
        self.database = database
        self._create_database_and_tables()

    def _create_database_and_tables(self):
        # Create database if it doesn't exist, then connect and create tables
        try:
            with mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password
            ) as cnx:
                cursor = cnx.cursor()
                cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database}")
        except mysql.connector.Error as err:
            print(f"Error creating database: {err}")
            return  # Exit if database creation fails

        # Now that database exists, connect and create tables
        self._create_tables()
    
    def _create_tables(self):
        try:
            with self.connect() as cnx:
                cursor = cnx.cursor()

                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS books (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        title VARCHAR(255) NOT NULL,
                        author VARCHAR(255) NOT NULL,
                        year INT,
                        isbn VARCHAR(20) UNIQUE
                    )
                ''')

                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS users (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        username VARCHAR(255) UNIQUE NOT NULL,
                        password_hash VARCHAR(255) NOT NULL,
                        salt VARCHAR(255) NOT NULL,
                        email VARCHAR(255) UNIQUE NOT NULL,
                        reset_token VARCHAR(255)
                    )
                ''')
                cnx.commit()
        except mysql.connector.Error as err:
            print(f"Error creating tables: {err}")

    def connect(self):
        # Establish a database connection
        return mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )

    def add_book(self, title, author, year, isbn):
        with self.connect() as cnx:
            cursor = cnx.cursor()
            cursor.execute(
                "INSERT INTO books (title, author, year, isbn) VALUES (%s, %s, %s, %s)",
                (title, author, year, isbn)
            )
            cnx.commit()

    def get_books(self):
        with self.connect() as cnx:
            cursor = cnx.cursor()
            cursor.execute("SELECT * FROM books")
            return cursor.fetchall()

    def update_book(self, book_id, title, author, year, isbn):
        with self.connect() as cnx:
            cursor = cnx.cursor()
            cursor.execute(
                "UPDATE books SET title = %s, author = %s, year = %s, isbn = %s WHERE id = %s",
                (title, author, year, isbn, book_id)
            )
            cnx.commit()

    def delete_book(self, book_id):
        with self.connect() as cnx:
            cursor = cnx.cursor()
            cursor.execute("DELETE FROM books WHERE id = %s", (book_id,))
            cnx.commit()

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
                    VALUES (%s, %s, %s, %s)
                ''', (username, password_hash, salt, email))  # Use %s for MySQL
                conn.commit()
                return True
        except mysql.connector.IntegrityError:
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
        with self.connect() as cnx:
            cursor = cnx.cursor()
            cursor.execute("UPDATE users SET reset_token = %s WHERE email = %s", (token, email))
            cnx.commit()
            if cursor.rowcount > 0:
                return token
        return None

    def reset_password(self, token, new_password):
        # Reset password using token
        with self.connect() as cnx:
            cursor = cnx.cursor()
            cursor.execute("SELECT id FROM users WHERE reset_token = %s", (token,))
            user = cursor.fetchone()
            if user:
                password_hash, salt = self._hash_password(new_password)
                conn.execute('''
                    UPDATE users 
                    SET password_hash=?, salt=?, reset_token=NULL 
                    WHERE id=?
                ''', (password_hash, salt, user[0]))
                cnx.commit()
                return True
        return False

    def check_username_exists(self, username):
        # Check if username already exists
        with self.connect() as cnx:
            cursor = cnx.cursor()
            cursor.execute("SELECT 1 FROM users WHERE username = %s", (username,))
            result = cursor.fetchone()
            return bool(result)

    def check_email_exists(self, email):
        # Check if email already exists
        with self.connect() as cnx:
            cursor = cnx.cursor()
            cursor.execute("SELECT 1 FROM users WHERE email = %s", (email,))
            result = cursor.fetchone()
            return bool(result)