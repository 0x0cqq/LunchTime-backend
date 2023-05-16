from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register_without_verification", views.register_without_verification, name="register_without_verification"),

    path("verify_email", views.verify_email, name="verify_email"),
    path("register", views.register, name="register"),
    path("login", views.login, name="login"),

    path("posts", views.getPosts, name="get_posts"),
    path("post_detail", views.getPostDetail, name="get_post_detail"),
    
    path("post", views.post, name="post"),
    path("love_post", views.lovePost, name="love_post"),
    path("save_post", views.savePost, name="save_post"),
    path("comment_post", views.commentPost, name="comment_post"),

    path("notice", views.getNotice, name="get_notice"),
]