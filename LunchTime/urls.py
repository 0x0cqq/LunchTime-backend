from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register_without_verification", views.register_without_verification, name="register_without_verification"),

    path("verify_email", views.verify_email, name="verify_email"),
    path("register", views.register, name="register"),
    path("login", views.login, name="login"),
    path("get_posts_by_time", views.getPostsByTime, name="get_posts_by_time"),
    path("get_post_by_popularity", views.getPostByPopularity, name="get_post_by_popularity"),
    path("get_post_by_attention", views.getPostByAttention, name="get_post_by_attention"),
    path("get_post_detail", views.getPostDetail, name="get_post_detail"),
    path("post", views.post, name="post"),
]