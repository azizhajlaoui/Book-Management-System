import mysql.connector
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

def reset_database():
    # Connect to MySQL server
    conn = mysql.connector.connect(
        host=os.getenv('MYSQL_HOST', 'localhost'),
        user=os.getenv('MYSQL_USER', 'root'),
        password=os.getenv('MYSQL_PASSWORD', '')
    )
    
    cursor = conn.cursor()
    
    # Drop database if it exists
    cursor.execute(f"DROP DATABASE IF EXISTS {os.getenv('MYSQL_DATABASE', 'books_db')}")
    
    # Create database
    cursor.execute(f"CREATE DATABASE {os.getenv('MYSQL_DATABASE', 'books_db')}")
    
    conn.commit()
    cursor.close()
    conn.close()
    
    print("Database has been reset successfully!")

if __name__ == "__main__":
    reset_database() 