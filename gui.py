import tkinter as tk
from tkinter import ttk, messagebox
from ttkthemes import ThemedTk

def create_gui(root, db, on_sign_out=None):
    # Configure style
    style = ttk.Style()
    style.configure('TLabel', font=('Segoe UI', 10))
    style.configure('TEntry', font=('Segoe UI', 10))
    style.configure('TButton', font=('Segoe UI', 10))
    style.configure('Treeview', font=('Segoe UI', 10))
    style.configure('Treeview.Heading', font=('Segoe UI', 10, 'bold'))
    
    # Header frame for title and sign out
    header_frame = ttk.Frame(root)
    header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(10, 0))
    
    # App title
    title_label = ttk.Label(header_frame, text="Book Manager", font=('Segoe UI', 16, 'bold'))
    title_label.pack(side=tk.LEFT)
    
    # Sign out button
    if on_sign_out:
        sign_out_btn = ttk.Button(header_frame, text="Sign Out", command=on_sign_out)
        sign_out_btn.pack(side=tk.RIGHT)
    
    # Main container with padding
    main_frame = ttk.Frame(root, padding="20")
    main_frame.grid(row=1, column=0, sticky="nsew")
    
    # Configure grid weights
    root.grid_rowconfigure(1, weight=1)
    root.grid_columnconfigure(0, weight=1)
    main_frame.grid_columnconfigure(1, weight=1)
    
    # Create form entry fields
    entries = {}
    fields = ['Title', 'Author', 'Year', 'ISBN']
    
    # Create labels and inputs for each field
    for idx, field in enumerate(fields):
        # Label for each input field
        ttk.Label(main_frame, text=f"{field}:").grid(row=idx, column=0, sticky="e", padx=(0, 10), pady=5)
        # Input field stored in dictionary
        entries[field] = ttk.Entry(main_frame, width=30)
        entries[field].grid(row=idx, column=1, sticky="ew", padx=(0, 20), pady=5)

    # Create Treeview instead of Listbox
    columns = ('ID', 'Title', 'Author', 'Year', 'ISBN')
    tree = ttk.Treeview(main_frame, columns=columns, show='headings', height=15)
    
    # Configure column headings
    tree.heading('ID', text='ID')
    tree.heading('Title', text='Title')
    tree.heading('Author', text='Author')
    tree.heading('Year', text='Year')
    tree.heading('ISBN', text='ISBN')
    
    # Configure column widths
    tree.column('ID', width=50)
    tree.column('Title', width=200)
    tree.column('Author', width=150)
    tree.column('Year', width=70)
    tree.column('ISBN', width=150)
    
    # Add scrollbar
    scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    
    # Grid the treeview and scrollbar
    tree.grid(row=len(fields), column=0, columnspan=2, sticky="nsew", pady=10)
    scrollbar.grid(row=len(fields), column=2, sticky="ns")

    def refresh_list():
        # Clear current items
        for item in tree.get_children():
            tree.delete(item)
        # Add books from database
        for book in db.get_books():
            tree.insert('', tk.END, values=book)

    def get_selected_id():
        # Get selected book ID from treeview
        selection = tree.selection()
        if selection:
            return tree.item(selection[0])['values'][0]
        return None

    def validate_inputs():
        # Basic input validation
        title = entries['Title'].get().strip()
        author = entries['Author'].get().strip()
        year = entries['Year'].get().strip()
        isbn = entries['ISBN'].get().strip()
        
        if not title or not author:
            messagebox.showerror("Error", "Title and Author are required fields!")
            return False
            
        if year and not year.isdigit():
            messagebox.showerror("Error", "Year must be a number!")
            return False
            
        return True

    def add_book():
        if validate_inputs():
            try:
                db.add_book(
                    entries['Title'].get().strip(),
                    entries['Author'].get().strip(),
                    entries['Year'].get().strip(),
                    entries['ISBN'].get().strip()
                )
                clear_entries()
                refresh_list()
                messagebox.showinfo("Success", "Book added successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add book: {str(e)}")

    def update_book():
        if not get_selected_id():
            messagebox.showwarning("Warning", "Please select a book to update!")
            return
            
        if validate_inputs():
            try:
                db.update_book(
                    get_selected_id(),
                    entries['Title'].get().strip(),
                    entries['Author'].get().strip(),
                    entries['Year'].get().strip(),
                    entries['ISBN'].get().strip()
                )
                clear_entries()
                refresh_list()
                messagebox.showinfo("Success", "Book updated successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update book: {str(e)}")

    def delete_book():
        if not get_selected_id():
            messagebox.showwarning("Warning", "Please select a book to delete!")
            return
            
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this book?"):
            try:
                db.delete_book(get_selected_id())
                clear_entries()
                refresh_list()
                messagebox.showinfo("Success", "Book deleted successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete book: {str(e)}")

    def clear_entries():
        for entry in entries.values():
            entry.delete(0, tk.END)

    def fill_entries(event):
        selection = tree.selection()
        if selection:
            values = tree.item(selection[0])['values']
            clear_entries()
            entries['Title'].insert(0, values[1])
            entries['Author'].insert(0, values[2])
            entries['Year'].insert(0, values[3])
            entries['ISBN'].insert(0, values[4])

    # Control buttons frame
    btn_frame = ttk.Frame(main_frame)
    btn_frame.grid(row=len(fields) + 1, column=0, columnspan=2, pady=10)
    
    # Create buttons with consistent styling
    ttk.Button(btn_frame, text="Add Book", command=add_book).pack(side=tk.LEFT, padx=5)
    ttk.Button(btn_frame, text="Update Book", command=update_book).pack(side=tk.LEFT, padx=5)
    ttk.Button(btn_frame, text="Delete Book", command=delete_book).pack(side=tk.LEFT, padx=5)
    ttk.Button(btn_frame, text="Clear", command=clear_entries).pack(side=tk.LEFT, padx=5)

    # Event binding for tree selection
    tree.bind('<<TreeviewSelect>>', fill_entries)
    
    # Initial data load
    refresh_list()