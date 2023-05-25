import smtplib
import random
from LunchTime.models import *

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

def getSingleUserInfo(user_id: int, target_user_id: int, root_url: str):
    tmp = {}
    tmp['user_name'] = User.objects.filter(id=target_user_id).first().name
    user_info = UserInfo.objects.filter(id=target_user_id).first()
    # get target user's image
    tmp['user_image'] = root_url + '/media/userImage/' + user_info.image
    tmp['user_description'] = user_info.description
    # get user's follow count
    query = UserFollow.objects.filter(user_id=target_user_id)
    tmp['follow_count'] = query.count()
    # get user's fans count
    query = UserFollow.objects.filter(follow_user_id=target_user_id)
    tmp['fans_count'] = query.count()
    # check if user follows target user
    query = UserFollow.objects.filter(user_id=user_id, follow_user_id=target_user_id)
    if query:
        tmp['is_following'] = True
    else:
        tmp['is_following'] = False
    # check if user hate target user
    query = UserHate.objects.filter(user_id=user_id, hate_user_id=target_user_id)
    if query:
        tmp['is_hating'] = True
    else:
        tmp['is_hating'] = False
    return tmp