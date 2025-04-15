import mysql.connector
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

def update_database():
    try:
        # Connect to MySQL server
        conn = mysql.connector.connect(
            host=os.getenv('MYSQL_HOST', 'localhost'),
            user=os.getenv('MYSQL_USER', 'root'),
            password=os.getenv('MYSQL_PASSWORD', ''),
            database=os.getenv('MYSQL_DATABASE', 'books_db')
        )
        
        cursor = conn.cursor()
        
        # Drop existing tables if they exist
        cursor.execute("DROP TABLE IF EXISTS books")
        cursor.execute("DROP TABLE IF EXISTS users")
        
        # Create books table
        cursor.execute('''
            CREATE TABLE books (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                author VARCHAR(255) NOT NULL,
                year INT,
                isbn VARCHAR(20) UNIQUE
            )
        ''')
        
        # Create users table with all required columns
        cursor.execute('''
            CREATE TABLE users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(255) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                salt VARCHAR(255) NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                reset_token VARCHAR(255),
                reset_token_expiry DATETIME
            )
        ''')
        
        conn.commit()
        print("Database tables have been updated successfully!")
        
    except mysql.connector.Error as err:
        print(f"Error updating database: {err}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    update_database() 