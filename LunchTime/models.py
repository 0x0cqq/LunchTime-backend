from django.db import models

# Create your models here.
class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    def __str__(self):
        return str(self.id) + " " + self.name

class UserInfo(models.Model):
    id = models.IntegerField(primary_key=True)
    image = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    def __str__(self):
        return str(self.id)


class VerifyEmail(models.Model):
    email = models.CharField(max_length=200, primary_key=True)
    verification_code = models.CharField(max_length=200)
    def __str__(self):
        return self.email + " " + self.verification_code

class Post(models.Model):
    post_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    create_time = models.DateTimeField(auto_now_add=True)
    tag = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    content = models.CharField(max_length=1000)
    location = models.CharField(max_length=200)
    love_count = models.IntegerField()
    comment_count = models.IntegerField()
    save_count = models.IntegerField()
    popularity = models.IntegerField()

class PostPicture(models.Model):
    post_id = models.IntegerField()
    url = models.CharField(max_length=200)

class PostVideo(models.Model):
    post_id = models.IntegerField()
    url = models.CharField(max_length=200)

class PostLove(models.Model):
    post_id = models.IntegerField()
    user_id = models.IntegerField()
    create_time = models.DateTimeField(auto_now=True)
    isRead = models.BooleanField(default=False)
    def __str__(self):
        return "postId: " + str(self.post_id) + "  userId: " + str(self.user_id)

class PostSave(models.Model):
    post_id = models.IntegerField()
    user_id = models.IntegerField()
    create_time = models.DateTimeField(auto_now=True)
    def __str__(self):
        return "postId: " + str(self.post_id) + "  userId: " + str(self.user_id)

class PostComment(models.Model):
    post_id = models.IntegerField()
    user_id = models.IntegerField()
    create_time = models.DateTimeField(auto_now_add=True)
    comment = models.CharField(max_length=200)
    isRead = models.BooleanField(default=False)

class UserFollow(models.Model):
    user_id = models.IntegerField()
    follow_user_id = models.IntegerField()
    def __str__(self):
        return "userId: " + str(self.user_id) + "  followUserId: " + str(self.follow_user_id)

class UserHate(models.Model):
    user_id = models.IntegerField()
    hate_user_id = models.IntegerField()
    def __str__(self):
        return "userId: " + str(self.user_id) + "  hateUserId: " + str(self.hate_user_id)

   
class ChatMessage(models.Model):
    # sender_id and receiver_id are both user_id
    # createtime is the time when the message is sent
    # message is the content of the message
    message_id = models.AutoField(primary_key=True) 
    sender_id = models.IntegerField()
    receiver_id = models.IntegerField()
    create_time = models.DateTimeField()
    message = models.CharField(max_length=2000)
    isRead = models.BooleanField(default=False)
    def __str__(self):  
        return "senderId: " + str(self.sender_id) + "  receiverId: " + str(self.receiver_id) + "  message: " + self.message


class Client(models.Model):
    # client_id is auto generated
    # user_id is the id of the user who is using this client
    # channel_name is the django channel name of the client
    client_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    channel_name = models.CharField(max_length=200)
    def __str__(self):
        return "clientId: " + str(self.client_id) + "  userId: " + str(self.user_id) + "  channelName: " + self.channel_name