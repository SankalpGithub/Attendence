import smtplib
import random



def generate_otp(length=6):
    # Generate a random OTP of the specified length
    otp = ''.join(random.choice('0123456789') for _ in range(length))
    return otp

def send_otp_email(email,password,to_email,subject,body):
    try:
        # Create an SMTP connection to Gmail's SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()

        # Login to your Gmail account
        server.login(email, password)

        # Compose the email
        
        message = f'Subject: {subject}\n\n{body}'

        # Send the email
        server.sendmail(email, to_email, message)

        # Close the SMTP connection
        server.quit()
        
        return True

    except Exception as e:
        return False

# Replace with your Gmail credentials and recipient's email address

