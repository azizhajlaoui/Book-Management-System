import tkinter as tk
from ttkthemes import ThemedTk
from gui import create_gui
from database import BookDatabase

def main():
    # Create themed root window
    root = ThemedTk(theme="arc")  # Using the 'arc' theme for a modern look
    root.title("Book Manager")
    root.geometry("800x600")  # Set a reasonable default size
    
    # Initialize database
    db = BookDatabase()
    
    # Create GUI
    create_gui(root, db)
    
    # Start the application
    root.mainloop()

if __name__ == "__main__":
    main()