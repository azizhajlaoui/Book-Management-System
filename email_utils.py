import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

class EmailSender:
    def __init__(self):
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.sender_email = os.getenv('BOOK_MANAGER_EMAIL')
        self.sender_password = os.getenv('BOOK_MANAGER_PASSWORD')

    def send_reset_token(self, recipient_email, token):
        if not self.sender_email or not self.sender_password:
            raise ValueError("Email credentials not set in environment variables")

        # Create message
        message = MIMEMultipart()
        message["From"] = self.sender_email
        message["To"] = recipient_email
        message["Subject"] = "Book Manager - Password Reset"

        # Create HTML body
        html = f"""
        <html>
            <body style="font-family: Arial, sans-serif; padding: 20px;">
                <h2 style="color: #2c3e50;">Password Reset Request</h2>
                <p>You have requested to reset your password for the Book Manager application.</p>
                <p>Your password reset token is:</p>
                <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0;">
                    <code style="font-size: 18px; color: #e74c3c;">{token}</code>
                </div>
                <p>Please enter this token in the application to reset your password.</p>
                <p>If you did not request this password reset, please ignore this email.</p>
                <p style="color: #7f8c8d; font-size: 12px; margin-top: 30px;">
                    This is an automated message, please do not reply.
                </p>
            </body>
        </html>
        """

        # Attach HTML content
        message.attach(MIMEText(html, "html"))

        try:
            # Create SMTP session
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(message)
            return True
        except Exception as e:
            print(f"Failed to send email: {str(e)}")
            return False
