import tkinter as tk
from tkinter import ttk, messagebox
import re
from database import BookDatabase
from email_utils import EmailSender

class AuthFrame(ttk.Frame):
    def __init__(self, parent, db, on_login_success):
        super().__init__(parent)
        self.db = db
        self.on_login_success = on_login_success
        self.email_sender = EmailSender()

        # Create main container
        self.main_container = ttk.Frame(self)
        self.main_container.pack(expand=True, fill='both', padx=10, pady=10)
        
        # Create all frames
        self.login_frame = self._create_login_frame()
        self.signup_frame = self._create_signup_frame()
        self.forgot_frame = self._create_forgot_password_frame()
        
        # Initially show login frame
        self.current_frame = self.login_frame
        self.show_frame('login')

    def show_frame(self, frame_name):
        # Hide current frame
        if hasattr(self, 'current_frame') and self.current_frame:
            self.current_frame.pack_forget()
        
        # Show requested frame
        if frame_name == 'login':
            self.current_frame = self.login_frame
        elif frame_name == 'signup':
            self.current_frame = self.signup_frame
        elif frame_name == 'forgot':
            self.current_frame = self.forgot_frame
        
        self.current_frame.pack(expand=True, fill='both', in_=self.main_container)
    
    def _create_login_frame(self):
        frame = ttk.Frame(self.main_container, padding="20")
        
        # Username
        ttk.Label(frame, text="Username:").grid(row=0, column=0, sticky='w', pady=5)
        self.login_username = ttk.Entry(frame, width=30)
        self.login_username.grid(row=0, column=1, pady=5)
        
        # Password
        ttk.Label(frame, text="Password:").grid(row=1, column=0, sticky='w', pady=5)
        self.login_password = ttk.Entry(frame, show="*", width=30)
        self.login_password.grid(row=1, column=1, pady=5)
        
        # Login button
        ttk.Button(frame, text="Login", command=self._handle_login).grid(row=2, column=0, columnspan=2, pady=20)
        
        # Navigation buttons
        nav_frame = ttk.Frame(frame)
        nav_frame.grid(row=3, column=0, columnspan=2, pady=10)
        
        ttk.Button(nav_frame, text="Create Account", 
                   command=lambda: self.show_frame('signup')).pack(side=tk.LEFT, padx=5)
        ttk.Button(nav_frame, text="Forgot Password", 
                   command=lambda: self.show_frame('forgot')).pack(side=tk.LEFT, padx=5)
        
        return frame

    def _create_signup_frame(self):
        frame = ttk.Frame(self.main_container, padding="20")
        
        # Username
        ttk.Label(frame, text="Username:").grid(row=0, column=0, sticky='w', pady=5)
        self.signup_username = ttk.Entry(frame, width=30)
        self.signup_username.grid(row=0, column=1, pady=5)
        
        # Email
        ttk.Label(frame, text="Email:").grid(row=1, column=0, sticky='w', pady=5)
        self.signup_email = ttk.Entry(frame, width=30)
        self.signup_email.grid(row=1, column=1, pady=5)
        
        # Password
        ttk.Label(frame, text="Password:").grid(row=2, column=0, sticky='w', pady=5)
        self.signup_password = ttk.Entry(frame, show="*", width=30)
        self.signup_password.grid(row=2, column=1, pady=5)
        
        # Confirm Password
        ttk.Label(frame, text="Confirm Password:").grid(row=3, column=0, sticky='w', pady=5)
        self.signup_confirm = ttk.Entry(frame, show="*", width=30)
        self.signup_confirm.grid(row=3, column=1, pady=5)
        
        # Sign Up button
        ttk.Button(frame, text="Sign Up", command=self._handle_signup).grid(row=4, column=0, columnspan=2, pady=20)
        
        # Back to login button
        ttk.Button(frame, text="Back to Login", 
                   command=lambda: self.show_frame('login')).grid(row=5, column=0, columnspan=2, pady=10)
        
        return frame

    def _create_forgot_password_frame(self):
        frame = ttk.Frame(self.main_container, padding="20")
        
        # Email
        ttk.Label(frame, text="Email:").grid(row=0, column=0, sticky='w', pady=5)
        self.forgot_email = ttk.Entry(frame, width=30)
        self.forgot_email.grid(row=0, column=1, pady=5)
        
        # Submit button
        ttk.Button(frame, text="Reset Password", command=self._handle_forgot_password).grid(row=1, column=0, columnspan=2, pady=20)
        

        # Back to login button
        ttk.Button(frame, text="Back to Login", 
                   command=lambda: self.show_frame('login')).grid(row=2, column=0, columnspan=2, pady=10)
        
        # Reset token frame (initially hidden)
        self.reset_frame = ttk.Frame(frame)
        ttk.Label(self.reset_frame, text="Reset Token:").grid(row=0, column=0, sticky='w', pady=5)
        self.reset_token = ttk.Entry(self.reset_frame, width=30)
        self.reset_token.grid(row=0, column=1, pady=5)
        
        ttk.Label(self.reset_frame, text="New Password:").grid(row=1, column=0, sticky='w', pady=5)
        self.reset_password = ttk.Entry(self.reset_frame, show="*", width=30)
        self.reset_password.grid(row=1, column=1, pady=5)
        
        ttk.Button(self.reset_frame, text="Set New Password", command=self._handle_reset_password).grid(row=2, column=0, columnspan=2, pady=20)
        
        return frame

    def _handle_login(self):
        username = self.login_username.get().strip()
        password = self.login_password.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please fill in all fields")
            return
        
        if self.db.verify_user(username, password):
            self.on_login_success()
        else:
            messagebox.showerror("Error", "Invalid username or password")

    def _handle_signup(self):
        username = self.signup_username.get().strip()
        email = self.signup_email.get().strip()
        password = self.signup_password.get()
        confirm = self.signup_confirm.get()
        
        # Validation
        if not all([username, email, password, confirm]):
            messagebox.showerror("Error", "Please fill in all fields")
            return
        
        if password != confirm:
            messagebox.showerror("Error", "Passwords do not match")
            return
        
        if len(password) < 8:
            messagebox.showerror("Error", "Password must be at least 8 characters long")
            return
        
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            messagebox.showerror("Error", "Invalid email format")
            return
        
        if self.db.check_username_exists(username):
            messagebox.showerror("Error", "Username already exists")
            return
        
        if self.db.check_email_exists(email):
            messagebox.showerror("Error", "Email already registered")
            return
        
        if self.db.register_user(username, password, email):
            messagebox.showinfo("Success", "Registration successful! Please login.")
            self.show_frame('login')  # Switch to login frame
        else:
            messagebox.showerror("Error", "Registration failed")

    def _handle_forgot_password(self):
        email = self.forgot_email.get().strip()
        
        if not email:
            messagebox.showerror("Error", "Please enter your email")
            return

        token = self.db.generate_reset_token(email)
        if token:
            if self.email_sender.send_reset_token(email, token):
                messagebox.showinfo("Success", "A password reset token has been sent to your email.")
                self.reset_frame.grid(row=2, column=0, columnspan=2, pady=10)
            else:
                messagebox.showerror("Error", "Failed to send reset token email. Please try again later.")
        else:
            messagebox.showerror("Error", "Email not found")

    def _handle_reset_password(self):
        token = self.reset_token.get().strip()
        new_password = self.reset_password.get()
        
        if not token or not new_password:
            messagebox.showerror("Error", "Please fill in all fields")
            return
        
        if len(new_password) < 8:
            messagebox.showerror("Error", "Password must be at least 8 characters long")
            return
        
        if self.db.reset_password(token, new_password):
            messagebox.showinfo("Success", "Password reset successful! Please login.")
            self.show_frame('login')  # Switch to login frame
            self.reset_frame.grid_remove()  # Hide reset frame
            self.forgot_email.delete(0, tk.END)  # Clear email field
            self.reset_token.delete(0, tk.END)  # Clear token field
            self.reset_password.delete(0, tk.END)  # Clear new password field
        else:
            messagebox.showerror("Error", "Invalid or expired reset token")
