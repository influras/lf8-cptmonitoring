import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from tkinter import *
from tkinter import DISABLED

# E-Mail details
sender_email='youremail'
sender_password='yourpasswort'

error_window = Tk()
error_window.geometry("600x600")
error_window.title("Fehlerbericht")
error_text = Text(error_window, height=10, width=60, state=DISABLED)
error_text.pack()
error_window.withdraw()


def send_email(recipient_email, message, hostname):
    # Set up the SMTP server
    smtp_server = 'smtp.web.de'
    smtp_port = 587

    # Create a multipart message and set headers
    email_message = MIMEMultipart()
    email_message['From'] = sender_email
    email_message['To'] = recipient_email
    email_message['Subject'] = "Hardware Report - " + hostname + datetime.datetime.now().strftime("%Y-%m-%d %H:%M") + hostname

    # Add body to the email
    email_message.attach(MIMEText(message, 'plain'))

    try:
        # Start the SMTP server and send the email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(email_message)
        print("Email sent successfully!")
        return True
    except Exception as e:
        print(f"An error occurred while sending the email: {str(e)}")
        error_text.config(state=NORMAL)
        error_text.delete("1.0", END)
        error_text.insert(END, str(e))
        error_text.config(state=DISABLED)
        error_window.deiconify()
        return False
