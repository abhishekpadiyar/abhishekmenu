import smtplib
import os

def send_email(to, message):
    email_id = os.environ.get('SMTP_USER')  # Your email address
    password = os.environ.get('SMTP_PASS')  # App password

    try:
        # Create the SMTP connection
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Start TLS for security
        server.login(email_id, password)  # Login to your email
        
        # Create the email message
        subject = "Test Email"
        body = f"Subject:{subject}\n\n{message}"
        
        # Send the email
        server.sendmail(email_id, to, body)
        server.quit()  # Close the connection
        return "Email sent successfully"
    except Exception as e:
        return str(e)

# Send email

