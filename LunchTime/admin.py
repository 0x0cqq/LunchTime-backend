from django.contrib import admin

from .models import *
# Register your models here.
admin.site.register(User)
admin.site.register(UserAttention)
admin.site.register(VerifyEmail)
admin.site.register(Post)
admin.site.register(PostPicture)
admin.site.register(PostLove)
admin.site.register(PostComment)
admin.site.register(PostSave)
