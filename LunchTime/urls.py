from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register_without_verification", views.register_without_verification, name="register_without_verification"),

    path("verify_email", views.verify_email, name="verify_email"),
    path("register", views.register, name="register"),
    path("login", views.login, name="login"),
    path("user_info", views.getUserInfo, name="get_user_info"),

    path("posts", views.getPosts, name="get_posts"),
    path("post_detail", views.getPostDetail, name="get_post_detail"),
    path("search_post", views.getPostsBySearch, name="search_post"),

    path("post", views.post, name="post"),
    path("love_post", views.lovePost, name="love_post"),
    path("save_post", views.savePost, name="save_post"),
    path("comment_post", views.commentPost, name="comment_post"),
    
    path("notice", views.getNotice, name="get_notice"),

    path("attention", views.followUser, name="attention"),
    path("attention_list", views.getAttentionList, name="attention_list"),
    path("hate", views.hateUser, name="hate"),

    path("modify_user_name", views.modifyUserName, name="modify_user_info"),
    path("modify_user_description", views.modifyUserDescription, name="modify_user_description"),
    path("modify_user_image", views.modifyUserImage, name="modify_user_image"),
    path("modify_user_password", views.modifyUserPassword, name="modify_user_password"),
]