import tkinter as tk
from ttkthemes import ThemedTk
from gui import create_gui
from auth_gui import AuthFrame
from database import BookDatabase
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

class App:
    def __init__(self):
        # Create themed root window
        self.root = ThemedTk(theme="arc") 
        self.root.title("Book Manager")
        self.root.geometry("900x700")
        
        # Initialize database with environment variables
        self.db = BookDatabase(
            user=os.getenv('MYSQL_USER', 'root'),
            password=os.getenv('MYSQL_PASSWORD', ''),
            host=os.getenv('MYSQL_HOST', 'localhost'),
            database=os.getenv('MYSQL_DATABASE', 'books_db')
        )
        
        # Create authentication frame
        self.auth_frame = AuthFrame(self.root, self.db, self.on_login_success)
        self.auth_frame.pack(expand=True, fill='both')
        
        # Main application frame (initially hidden)
        self.main_frame = tk.Frame(self.root)
        
        # Create menu bar
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)
        
        # Create account menu
        self.account_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.account_menu.add_command(label="Sign Out", command=self.on_sign_out)
        self.menu_bar.add_cascade(label="Account", menu=self.account_menu)
        
        # Hide menu bar initially
        self.root.config(menu="")
    
    def on_login_success(self):
        # Remove authentication frame
        self.auth_frame.pack_forget()
        
        # Show main application
        self.main_frame.pack(expand=True, fill='both')
        create_gui(self.main_frame, self.db, self.on_sign_out)
        
        # Show menu bar
        self.root.config(menu=self.menu_bar)
    
    def on_sign_out(self):
        # Hide menu bar
        self.root.config(menu="")
        
        # Hide main application
        self.main_frame.pack_forget()
        
        # Clear main frame widgets
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        # Show authentication frame
        self.auth_frame.show_frame('login')
        self.auth_frame.pack(expand=True, fill='both')
    
    def run(self):
        self.root.mainloop()

def main():
    app = App()
    app.run()

if __name__ == "__main__":
    main()