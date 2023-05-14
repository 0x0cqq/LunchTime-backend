from django.db import models

# Create your models here.
class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    def __str__(self):
        return self.id + " " + self.name

class UserAttention(models.Model):
    user_id = models.IntegerField()
    attention_user_id = models.IntegerField()

class VerifyEmail(models.Model):
    email = models.CharField(max_length=200, primary_key=True)
    verification_code = models.CharField(max_length=200)
    def __str__(self):
        return self.email + " " + self.verification_code

class Post(models.Model):
    post_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    create_time = models.DateTimeField(auto_now=True)
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

class PostLove(models.Model):
    post_id = models.IntegerField()
    user_id = models.IntegerField()
    def __str__(self):
        return "postId: " + str(self.post_id) + "  userId: " + str(self.user_id)

class PostSave(models.Model):
    post_id = models.IntegerField()
    user_id = models.IntegerField()
    def __str__(self):
        return "postId: " + str(self.post_id) + "  userId: " + str(self.user_id)

class PostComment(models.Model):
    post_id = models.IntegerField()
    user_id = models.IntegerField()
    create_time = models.DateField(auto_now=True)
    comment = models.CharField(max_length=200)