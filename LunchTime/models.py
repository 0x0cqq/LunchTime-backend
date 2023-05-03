from django.db import models

# Create your models here.
class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    def __str__(self):
        return self.name + " " + self.email

class VerifyEmail(models.Model):
    email = models.CharField(max_length=200, primary_key=True)
    verification_code = models.CharField(max_length=200)
    def __str__(self):
        return self.email + " " + self.verification_code