import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email(sender_email, sender_password, recipient_email, subject, message):
    # Set up the SMTP server
    smtp_server = 'smtp.web.de'
    smtp_port = 587

    # Create a multipart message and set headers
    email_message = MIMEMultipart()
    email_message['From'] = sender_email
    email_message['To'] = recipient_email
    email_message['Subject'] = subject

    # Add body to the email
    email_message.attach(MIMEText(message, 'plain'))

    try:
        # Start the SMTP server and send the email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(email_message)
        print("Email sent successfully!")
    except Exception as e:
        print(f"An error occurred while sending the email: {str(e)}")


# Provide your email details
sender_email = 'captainmonitoring@web.de'
sender_password = 'Monitoring!23'
recipient_email = 'kaicjankowski@gmail.com'
subject = 'Test Email'
message = 'This is a test email sent from Python.'

# Call the send_email function with the provided details
send_email(sender_email, sender_password, recipient_email, subject, message)
