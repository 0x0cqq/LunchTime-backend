import smtplib
import random

def send_email(receiver_email):
    # set sender's email address and password
    sender_email_address = "lunchtime2023@163.com"
    sender_email_password = "YNNJNFBCTOPDACGA"
    # generate verification code
    verification_code = ""
    for i in range(6):
        verification_code += str(random.randint(0, 9))
    # write email
    subject = "Verification Code"
    body = "Welcome to LunchTime!\nYour verification code is " + verification_code + ".\n"
    message = f"Subject: {subject}\n\n{body}"
    # send email
    with smtplib.SMTP_SSL("smtp.163.com", 465) as smtp:
        smtp.login(sender_email_address, sender_email_password)
        smtp.sendmail(sender_email_address, receiver_email, message)
        smtp.quit()
    
    return verification_code

def calculate_popularity(like_count, comment_count, save_count):
    return like_count + comment_count + save_count