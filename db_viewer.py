import tkinter as tk
from tkinter import ttk, messagebox
from database import BookDatabase
import sqlite3

class DatabaseViewer(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Book Manager Database Viewer")
        self.geometry("1000x700")
        
        self.db = BookDatabase()
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Create tabs
        self.books_frame = ttk.Frame(self.notebook)
        self.users_frame = ttk.Frame(self.notebook)
        
        self.notebook.add(self.books_frame, text='Books')
        self.notebook.add(self.users_frame, text='Users')
        
        # Setup both views
        self.setup_books_view()
        self.setup_users_view()
        
        # Add refresh button at the bottom
        self.refresh_btn = ttk.Button(self, text="Refresh All Data", command=self.refresh_all)
        self.refresh_btn.pack(pady=5)
        
        # Load initial data
        self.refresh_all()

    def setup_books_view(self):
        # Create Treeview for books
        columns = ('ID', 'Title', 'Author', 'Year', 'ISBN')
        self.books_tree = self.create_treeview(self.books_frame, columns)
        
        # Configure column widths
        self.books_tree.column('ID', width=50)
        self.books_tree.column('Title', width=250)
        self.books_tree.column('Author', width=200)
        self.books_tree.column('Year', width=100)
        self.books_tree.column('ISBN', width=150)

    def setup_users_view(self):
        # Create Treeview for users
        columns = ('ID', 'Username', 'Email')  # Excluding password-related fields for security
        self.users_tree = self.create_treeview(self.users_frame, columns)
        
        # Configure column widths
        self.users_tree.column('ID', width=50)
        self.users_tree.column('Username', width=200)
        self.users_tree.column('Email', width=300)

    def create_treeview(self, parent, columns):
        # Create container frame
        container = ttk.Frame(parent)
        container.pack(fill='both', expand=True)
        
        # Create Treeview
        tree = ttk.Treeview(container, columns=columns, show='headings')
        
        # Add scrollbars
        yscroll = ttk.Scrollbar(container, orient='vertical', command=tree.yview)
        xscroll = ttk.Scrollbar(container, orient='horizontal', command=tree.xview)
        tree.configure(yscrollcommand=yscroll.set, xscrollcommand=xscroll.set)
        
        # Setup headings
        for col in columns:
            tree.heading(col, text=col, command=lambda c=col: self.sort_treeview(tree, c, False))
        
        # Pack elements
        tree.pack(side='left', fill='both', expand=True)
        yscroll.pack(side='right', fill='y')
        xscroll.pack(side='bottom', fill='x')
        
        return tree

    def load_books(self):
        try:
            # Clear existing items
            for item in self.books_tree.get_children():
                self.books_tree.delete(item)
            
            # Get books from database
            with self.db.connect() as conn:
                cursor = conn.execute('SELECT * FROM books ORDER BY id')
                for row in cursor:
                    self.books_tree.insert('', 'end', values=row)
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error loading books: {str(e)}")

    def load_users(self):
        try:
            # Clear existing items
            for item in self.users_tree.get_children():
                self.users_tree.delete(item)
            
            # Get users from database (excluding sensitive information)
            with self.db.connect() as conn:
                cursor = conn.execute('SELECT id, username, email FROM users ORDER BY id')
                for row in cursor:
                    self.users_tree.insert('', 'end', values=row)
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error loading users: {str(e)}")

    def refresh_all(self):
        self.load_books()
        self.load_users()

    def sort_treeview(self, tree, col, reverse):
        # Get all items in the tree
        data = [(tree.set(item, col), item) for item in tree.get_children('')]
        
        # Sort the data
        data.sort(reverse=reverse)
        
        # Rearrange items in sorted positions
        for index, (val, item) in enumerate(data):
            tree.move(item, '', index)
        
        # Switch the heading command to reverse sort next time
        tree.heading(col, command=lambda: self.sort_treeview(tree, col, not reverse))

if __name__ == '__main__':
    try:
        app = DatabaseViewer()
        app.mainloop()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")
