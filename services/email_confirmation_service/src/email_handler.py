import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
from os import environ

def send_email(receiver_email, subject, message_body):
    # Configure your email settings
    sender_email = environ.get('MAIL_ACCOUNT')  # Replace with your email
    sender_password = environ.get('MAIL_ACCOUNT_PASSWORD')  # Replace with your email's app-specific password

    # Create the email message
    message = EmailMessage()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.set_content(message_body)

    # Connect to the SMTP server
    with smtplib.SMTP("smtp.gmail.com", 587) as server:  # Adjust for your SMTP server
        server.starttls()  # Start TLS encryption
        server.login(sender_email, sender_password)  # Log in to the SMTP server
        server.send_message(message)  # Send the email
        print("Email sent successfully!")

if __name__ == '__main__':
    load_dotenv()
    # Example usage
    send_email(
        receiver_email="dkc.camargo@gmail.com",
        subject="Douglas App confirmation code",
        message_body="Your confirmation code is: A1B2C3 do not share with anybody."
    )
