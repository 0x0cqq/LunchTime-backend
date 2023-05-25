from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.utils import timezone
from LunchTime.models import *
from LunchTime.utils import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
import os
from time import time

root_url = "http://localhost:8000"
# root_url = "http://lunchtime.cqqqwq.com:8000"
# Create your views here.
def index(request: HttpRequest):
    return HttpResponse("Hello, world. You're at the LunchTime index.")

def register_without_verification(request: HttpRequest):
    res = {}
    if request.method != 'POST':
        res['status'] = False
        res['message'] = 'false method'
        return JsonResponse(res)
    try:
        name = request.POST.get('name')
        password = request.POST.get('password')
        email = request.POST.get('email')
        # check if name exists
        query = User.objects.filter(name=name)
        if query:
            res['status'] = False
            res['message'] = 'name exists'
            return JsonResponse(res)
        # check if email exists
        query = User.objects.filter(email=email)
        if query:
            res['status'] = False
            res['message'] = 'email exists'
            return JsonResponse(res)
        # add new user to database
        user = User(name=name, password=password, email=email)
        user.save()
        res['status'] = True
        res['message'] = 'ok'
    except:
        res['status'] = False
        res['message'] = 'unexpected parameters'
    return JsonResponse(res)

@api_view(['POST'])
def verify_email(request: HttpRequest):
    res = {}
    if request.method != 'POST':
        res['status'] = False
        res['message'] = 'false method'
        return JsonResponse(res)
    try:
        email = request.POST.get('email')
        # send verification code
        verification_code = send_email(email)
        # add VerifyEmail to database
        query = VerifyEmail.objects.filter(email=email)
        if query:
            verify_email = query.first()
            verify_email.verification_code = verification_code
            verify_email.save()
        else:
            verify_email = VerifyEmail(email=email, verification_code=verification_code)
            verify_email.save()
        res['status'] = True
        res['message'] = 'ok'
    except:
        res['status'] = False
        res['message'] = 'unexpected parameters'
    return JsonResponse(res)

@api_view(['POST'])
def register(request: HttpRequest):
    res = {}
    if request.method != 'POST':
        res['status'] = False
        res['message'] = 'false method'
        return JsonResponse(res)
    try:
        name = request.POST.get('name')
        password = request.POST.get('password')
        email = request.POST.get('email')
        verification = request.POST.get('verification')
        # check if name exists
        query = User.objects.filter(name=name)
        if query:
            res['status'] = False
            res['message'] = 'name exists'
            return JsonResponse(res)
        # check if email exists
        query = User.objects.filter(email=email)
        if query:
            res['status'] = False
            res['message'] = 'email exists'
            return JsonResponse(res)
        # check verification code
        query = VerifyEmail.objects.filter(email=email)
        if not query:
            res['status'] = False
            res['message'] = 'No verfication code sent'
            return JsonResponse(res)
        if query:
            verify_email = query.first()
            if verification != verify_email.verification_code:
                res['status'] = False
                res['message'] = 'wrong verification code'
                return JsonResponse(res)
        # add new user to database
        user = User(name=name, password=password, email=email)
        user.save()
        userInfo = UserInfo(id=user.id, image='default.jpg', description='')
        userInfo.save()
        res['status'] = True
        res['message'] = 'ok'
    except:
        res['status'] = False
        res['message'] = 'unexpected parameters'
    return JsonResponse(res)

@api_view(['POST'])
def login(request: HttpRequest):
    res = {}
    if request.method != 'POST':
        res['status'] = False
        res['message'] = 'false method'
        return JsonResponse(res)

    try:
        name = request.POST.get('name')
        password = request.POST.get('password')
        # check if name exists
        query = User.objects.filter(name=name)
        if not query:
            res['status'] = False
            res['message'] = 'name does not exist'
            return JsonResponse(res)
        # check if password is correct
        query = User.objects.filter(name=name, password=password)
        if not query:
            res['status'] = False
            res['message'] = 'wrong password'
            return JsonResponse(res)
        # login successfully
        res['status'] = True    
        res['message'] = 'ok'
    except:
        res['status'] = False
        res['message'] = 'unexpected parameters'
    return JsonResponse(res)

@api_view(['GET'])
def getUserInfo(request: HttpRequest):
    res = {}
    if request.method != "GET":
        res['status'] = False
        res['message'] = 'false method'
        return JsonResponse(res)
    try:
        # get parameters
        user_name = request.GET.get('user_name')
        target_user_name = request.GET.get('target_user_name')
        # check if user exists
        query = User.objects.filter(name=user_name)
        if not query:
            res['status'] = False
            res['message'] = 'user does not exist'
            return JsonResponse(res)
        user_id = query.first().id
        # check if target user exists
        query = User.objects.filter(name=target_user_name)
        if not query:
            res['status'] = False
            res['message'] = 'target user does not exist'
            return JsonResponse(res)
        target_user_id = query.first().id
        # get user's info
        res['user_info'] = getSingleUserInfo(user_id, target_user_id, root_url)
        res['status'] = True
        res['message'] = 'ok'
    except Exception as e:
        print(e)
        res['status'] = False
        res['message'] = 'unexpected parameters'
    return JsonResponse(res)

@api_view(['GET'])
def getPosts(request: HttpRequest):
    res = {}
    if request.method != "GET":
        res['status'] = False
        res['message'] = 'false method'
        return JsonResponse(res)
    try:
        user_name = request.GET.get('user_name')
        type = int(request.GET.get('type'))
        target_user_name = request.GET.get('target_user_name')
        # get user id
        query = User.objects.filter(name=user_name)
        if not query:
            res['status'] = False
            res['message'] = 'user does not exist'
            return JsonResponse(res)
        user_id = query.first().id
        # get all posts
        objects = Post.objects.all()
        posts = []
        for post in objects:
            tmp = {}
            query = User.objects.filter(id=post.user_id)
            post_user_name = query.first().name
            if target_user_name and target_user_name != post_user_name:
                continue
            tmp['post_id'] = post.post_id
            tmp['user_name'] = post_user_name
            # get user's info
            query = UserInfo.objects.filter(id=post.user_id)
            if not query:
                res['status'] = False
                res['message'] = 'user info does not exist'
                return JsonResponse(res)
            user_info = query.first()
            tmp['user_image'] = root_url + '/media/userImage/' + user_info.image
            tmp['create_time'] = post.create_time.timestamp().__floor__()
            tmp['tag'] = post.tag
            tmp['title'] = post.title
            tmp['content'] = post.content
            tmp['location'] = post.location
            tmp['love_count'] = post.love_count
            tmp['comment_count'] = post.comment_count
            tmp['save_count'] = post.save_count
            tmp['picture'] = []
            tmp['popularity'] = post.popularity
            # check if user has loved this post
            query = PostLove.objects.filter(post_id=post.post_id, user_id=user_id)
            if query:
                tmp['is_loved'] = True
            else:
                tmp['is_loved'] = False
            # check if user has saved this post
            query = PostSave.objects.filter(post_id=post.post_id, user_id=user_id)
            if query:
                tmp['is_saved'] = True
            else:
                tmp['is_saved'] = False
            # get picture list
            queries = PostPicture.objects.filter(post_id=post.post_id)
            for q in queries:
                tmp['picture'].append(root_url + "/media/postImage/" + q.url)
            posts.append(tmp)
        if type == 0:
            sorted_posts = sorted(posts, key=lambda x: x["create_time"], reverse=True)
        elif type == 1:
            sorted_posts = sorted(posts, key=lambda x: x["popularity"], reverse=True)
        elif type == 2:
            sorted_posts = sorted(posts, key=lambda x: x["comment_count"], reverse=True)
        elif type == 3:
            queries = UserFollow.objects.filter(user_id=user_id)
            follow_list = []
            for q in queries:
                # get user's name
                query = User.objects.filter(id=q.follow_user_id)
                follow_list.append(query.first().name)
            sorted_posts = []
            for post in posts:
                if post['user_name'] in follow_list:
                    sorted_posts.append(post)
        elif type == 4:
            # get posts that user saved
            queries = PostSave.objects.filter(user_id=user_id)
            save_list = []
            for q in queries:
                save_list.append(q.post_id)
            sorted_posts = []
            for post in posts:
                if post['post_id'] in save_list:
                    sorted_posts.append(post)
        else:
            sorted_posts = posts
        res['status'] = True
        res['message'] = 'ok'
        res['posts'] = sorted_posts

    except Exception as e:
        print(e)
        res['status'] = False
        res['message'] = 'unexpected parameters'
    return JsonResponse(res)

@api_view(['GET'])
def getPostsBySearch(request: HttpRequest):
    res = {}
    if request.method != "GET":
        res['status'] = False
        res['message'] = 'false method'
        return JsonResponse(res)
    try:
        # get parameters
        user_name = request.GET.get('user_name')
        keyword = request.GET.get('keyword')
        field = request.GET.get('field')
        # get user id
        query = User.objects.filter(name=user_name)
        if not query:
            res['status'] = False
            res['message'] = 'user does not exist'
            return JsonResponse(res)
        user_id = query.first().id
        # split keyword to list
        keywords = keyword.split()
        # search posts
        field_posts = []
        if field == 'username':
            # search by user name
            for user in User.objects.all():
                contains_all_keywords = all(keyword in user.name for keyword in keywords)
                if contains_all_keywords:
                    target_user_id = user.id
                    objects = Post.objects.filter(user_id=target_user_id)
                    for post in objects:
                        field_posts.append(post)
        elif field == 'title':
            # 遍历所有的帖子对象
            for post in Post.objects.all():
                # 检查帖子是否包含keywords列表中所有元素
                contains_all_keywords = all(keyword in post.title for keyword in keywords)
                
                # 如果帖子包含所有关键词，则将其添加到field_posts列表中
                if contains_all_keywords:
                    field_posts.append(post)
        elif field == 'content':
            # 遍历所有的帖子对象
            for post in Post.objects.all():
                # 检查帖子是否包含keywords列表中所有元素
                contains_all_keywords = all(keyword in post.content for keyword in keywords)
                
                # 如果帖子包含所有关键词，则将其添加到field_posts列表中
                if contains_all_keywords:
                    field_posts.append(post)
        elif field == 'tag':
            # 遍历所有的帖子对象
            for post in Post.objects.all():
                # 检查帖子是否包含keywords列表中所有元素
                contains_all_keywords = all(keyword in post.tag for keyword in keywords)
                
                # 如果帖子包含所有关键词，则将其添加到field_posts列表中
                if contains_all_keywords:
                    field_posts.append(post)
        elif field == 'all':
            # get user id
            user_id_list = []
            for user in User.objects.all():
                contains_all_keywords = all(keyword in user.name for keyword in keywords)
                if contains_all_keywords:
                    target_user_id = user.id
                    user_id_list.append(target_user_id)
            # search all fields
            for post in Post.objects.all():
                flag_username = post.user_id in user_id_list
                flag_title = all(keyword in post.title for keyword in keywords)
                flag_tag = all(keyword in post.tag for keyword in keywords)
                flag_content = all(keyword in post.content for keyword in keywords)
                if flag_username or flag_title or flag_tag or flag_content:
                    field_posts.append(post)
        else:
            res['status'] = False
            res['message'] = 'wrong field'
            return JsonResponse(res)
        # generate response data
        posts = []
        for post in field_posts:
            query = User.objects.filter(id=post.user_id)
            post_user_name = query.first().name
            tmp = {}
            tmp['post_id'] = post.post_id
            tmp['user_name'] = post_user_name
            # get user's info
            query = UserInfo.objects.filter(id=post.user_id)
            if not query:
                res['status'] = False
                res['message'] = 'user info does not exist'
                return JsonResponse(res)
            user_info = query.first()
            tmp['user_image'] = root_url + '/media/userImage/' + user_info.image
            tmp['create_time'] = post.create_time.timestamp().__floor__()
            tmp['tag'] = post.tag
            tmp['title'] = post.title
            tmp['content'] = post.content
            tmp['location'] = post.location
            tmp['love_count'] = post.love_count
            tmp['comment_count'] = post.comment_count
            tmp['save_count'] = post.save_count
            tmp['picture'] = []
            tmp['popularity'] = post.popularity
            # check if user has loved this post
            query = PostLove.objects.filter(post_id=post.post_id, user_id=user_id)
            if query:
                tmp['is_loved'] = True
            else:
                tmp['is_loved'] = False
            # check if user has saved this post
            query = PostSave.objects.filter(post_id=post.post_id, user_id=user_id)
            if query:
                tmp['is_saved'] = True
            else:
                tmp['is_saved'] = False
            # get picture list
            queries = PostPicture.objects.filter(post_id=post.post_id)
            for q in queries:
                tmp['picture'].append(root_url + "/media/postImage/" + q.url)
            posts.append(tmp)
        res['posts'] = posts
        res['status'] = True
        res['message'] = 'ok'
    except Exception as e:
        print(e)
        res['status'] = False
        res['message'] = 'unexpected parameters'
    return JsonResponse(res)

@api_view(['GET'])
def getPostDetail(request : HttpRequest):
    res = {}
    if request.method != "GET":
        res['status'] = False
        res['message'] = 'false method'
        return JsonResponse(res)
    try:
        user_name = request.GET.get('user_name')
        post_id = int(request.GET.get('post_id'))
        # get user id
        query = User.objects.filter(name=user_name)
        user_id = query.first().id
        if not query:
            res['status'] = False
            res['message'] = 'user does not exist'
            return JsonResponse(res)
        # get post
        query = Post.objects.filter(post_id=post_id)
        if not query:
            res['status'] = False
            res['message'] = 'post does not exist'
            return JsonResponse(res)
        post = query.first()
        tmp = {}
        query = User.objects.filter(id=post.user_id)
        post_user_name = query.first().name
        tmp['user_name'] = post_user_name
        # get user's info
        query = UserInfo.objects.filter(id=post.user_id)
        if not query:
            res['status'] = False
            res['message'] = 'user info does not exist'
            return JsonResponse(res)
        user_info = query.first()
        tmp['user_image'] = root_url + '/media/userImage/' + user_info.image
        tmp['post_id'] = post.post_id
        tmp['create_time'] = post.create_time.timestamp().__floor__()
        tmp['tag'] = post.tag
        tmp['title'] = post.title
        tmp['content'] = post.content
        tmp['location'] = post.location
        tmp['love_count'] = post.love_count
        tmp['save_count'] = post.save_count
        tmp['comment_count'] = post.comment_count
        # check if user has loved this post
        query = PostLove.objects.filter(post_id=post_id, user_id=user_id)
        if query:
            tmp['is_loved'] = True
        else:
            tmp['is_loved'] = False
        # check if user has saved this post
        query = PostSave.objects.filter(post_id=post_id, user_id=user_id)
        if query:
            tmp['is_saved'] = True
        else:
            tmp['is_saved'] = False
        # add picture list
        tmp['picture'] = []
        queries = PostPicture.objects.filter(post_id=post_id)
        for q in queries:
            tmp['picture'].append(root_url + "/media/postImage/" + q.url)
        res['post'] = tmp
        # add comment list
        comments = []
        queries = PostComment.objects.filter(post_id=post_id)
        for q in queries:
            tmp = {}
            query = User.objects.filter(id=q.user_id)
            tmp['user_name'] = query.first().name
            # get user's info
            query = UserInfo.objects.filter(id=q.user_id)
            if not query:
                res['status'] = False
                res['message'] = 'user info does not exist'
                return JsonResponse(res)
            user_info = query.first()
            tmp['user_image'] = root_url + '/media/userImage/' + user_info.image
            tmp['content'] = q.comment
            tmp['create_time'] = q.create_time.timestamp().__floor__()
            comments.append(tmp)
        # sorted by create_time
        # sorted_comments = sorted(comments, key=lambda x: x["create_time"], reverse=False)
        res['comments'] = comments
        res['status'] = True
        res['message'] = 'ok'
    except Exception as e:
        print(e)
        res['status'] = False
        res['message'] = 'unexpected parameters'
    return JsonResponse(res)

@api_view(['POST'])
def post(request: HttpRequest):
    res = {}
    if request.method != "POST":
        res['status'] = False
        res['message'] = 'false method'
        return JsonResponse(res)
    try:
        user_name = request.POST.get('user_name')
        tag = request.POST.get('tag')
        title = request.POST.get('title')
        content = request.POST.get('content')
        location = request.POST.get('location')
        # match user_id by user_name
        query = User.objects.filter(name=user_name)
        if not query:
            res['status'] = False
            res['message'] = 'user does not exist'
            return JsonResponse(res)
        user_id = query.first().id
        # get current time
        create_time = timezone.now()
        create_time = timezone.localtime(create_time)
        create_time = create_time.strftime("%Y-%m-%d %H:%M:%S")
        # add new post to database
        post = Post(user_id=user_id, tag=tag, title=title, content=content, location=location, create_time=create_time,
            love_count=0, comment_count=0, save_count=0, popularity=0)
        post.save()

        # get picture list
        files = request.FILES.getlist('picture')
        for index, file in enumerate(files):
            file_dir = './media/postImage/'
            if not os.path.exists(file_dir):
                os.makedirs(file_dir)
            file_name =  str(int(time())) + "_" + str(index) + '.' + file.name.split('.')[-1]
            file_path = file_dir + file_name
            if file.name.split('.')[-1] not in ['jpeg','jpg','png']:
                res['status'] = False
                res['message'] = 'file error'
                return JsonResponse(res)
            with open(file_path,'wb+') as f:
                f.write(file.read())
            # add picture to database
            picture = PostPicture(post_id=post.post_id, url=file_name)
            picture.save()
        res['status'] = True
        res['message'] = "ok"
        res['post_id'] = post.post_id

    except Exception as e:
        print(e)
        res['status'] = False
        res['message'] = 'unexpected parameters'
    return JsonResponse(res)

@api_view(['POST'])
def lovePost(request: HttpRequest):
    res = {}
    if request.method != "POST":
        res['status'] = False
        res['message'] = 'false method'
        return JsonResponse(res)
    try:
        # get parameters
        user_name = request.POST.get('user_name')
        post_id = request.POST.get('post_id')
        # check if user exists
        query = User.objects.filter(name=user_name)
        if not query:
            res['status'] = False
            res['message'] = 'user does not exist'
            return JsonResponse(res)
        user_id = query.first().id
        # check if post exists
        query = Post.objects.filter(post_id=post_id)
        if not query:
            res['status'] = False
            res['message'] = 'post does not exist'
            return JsonResponse(res)
        post = query.first()
        # check if user has loved this post
        query = PostLove.objects.filter(user_id=user_id, post_id=post_id)
        if query:
            # cancel love
            query.delete()
            # update post love count and popularity
            post.popularity = calculate_popularity(post.love_count - 1, post.comment_count, post.save_count)
            post.love_count -= 1
            post.save()
            res['result'] = 0
        else:
            # add love
            love = PostLove(user_id=user_id, post_id=post_id)
            love.save()
            # update post love count and popularity
            post.popularity = calculate_popularity(post.love_count + 1, post.comment_count, post.save_count)
            post.love_count += 1
            post.save()
            res['result'] = 1
        res['status'] = True
        res['message'] = 'ok'
    except Exception as e:
        print(e)
        res['status'] = False
        res['message'] = 'unexpected parameters'
    return JsonResponse(res)

@api_view(['POST'])
def commentPost(request: HttpRequest):
    res = {}
    if request.method != "POST":
        res['status'] = False
        res['message'] = 'false method'
        return JsonResponse(res)
    try:
        # get parameters
        user_name = request.POST.get('user_name')
        post_id = request.POST.get('post_id')
        comment = request.POST.get('comment')
        # check if user exists
        query = User.objects.filter(name=user_name)
        if not query:
            res['status'] = False
            res['message'] = 'user does not exist'
            return JsonResponse(res)
        user_id = query.first().id
        # check if post exists
        query = Post.objects.filter(post_id=post_id)
        if not query:
            res['status'] = False
            res['message'] = 'post does not exist'
            return JsonResponse(res)
        post = query.first()
        # add comment
        comment = PostComment(user_id=user_id, post_id=post_id, comment=comment)
        comment.save()
        # update post comment count and popularity
        post.popularity = calculate_popularity(post.love_count, post.comment_count + 1, post.save_count)
        post.comment_count += 1
        post.save()
        res['status'] = True
        res['message'] = 'ok'
    except Exception as e:
        print(e)
        res['status'] = False
        res['message'] = 'unexpected parameters'
    return JsonResponse(res)


@api_view(['POST'])
def savePost(request):
    res = {}
    if request.method != "POST":
        res['status'] = False
        res['message'] = 'false method'
        return JsonResponse(res)
    try:
        # get parameters
        user_name = request.POST.get('user_name')
        post_id = request.POST.get('post_id')
        # check if user exists
        query = User.objects.filter(name=user_name)
        if not query:
            res['status'] = False
            res['message'] = 'user does not exist'
            return JsonResponse(res)
        user_id = query.first().id
        # check if post exists
        query = Post.objects.filter(post_id=post_id)
        if not query:
            res['status'] = False
            res['message'] = 'post does not exist'
            return JsonResponse(res)
        post = query.first()
        # check if user has saved this post
        query = PostSave.objects.filter(user_id=user_id, post_id=post_id)
        if query:
            # cancel save
            query.delete()
            # update post save count
            post.popularity = calculate_popularity(post.love_count, post.comment_count, post.save_count - 1)
            post.save_count -= 1
            post.save()
            res['result'] = 0
        else:
            # add save
            save = PostSave(user_id=user_id, post_id=post_id)
            save.save()
            # update post save count and popularity
            post.popularity = calculate_popularity(post.love_count, post.comment_count, post.save_count + 1)
            post.save_count += 1
            post.save()
            res['result'] = 1
        res['status'] = True
        res['message'] = 'ok'
    except Exception as e:
        print(e)
        res['status'] = False
        res['message'] = 'unexpected parameters'
    return JsonResponse(res)

@api_view(['GET'])
def getNotice(request: HttpRequest):
    res = {}
    if request.method != "GET":
        res['status'] = False
        res['message'] = 'false method'
        return JsonResponse(res)
    try:
        # get parameters
        user_name = request.GET.get('user_name')
        qeury_type = int(request.GET.get('type'))
        # check if user exists
        query = User.objects.filter(name=user_name)
        if not query:
            res['status'] = False
            res['message'] = 'user does not exist'
            return JsonResponse(res)
        user_id = query.first().id
        # get user's post list
        query = Post.objects.filter(user_id=user_id)
        post_ids = []
        for item in query:
            post_ids.append(item.post_id)
        # get user's comment/love/chat list
        noticeList = []
        if qeury_type == 1:
            query = PostComment.objects.filter(post_id__in=post_ids)
            for item in query:
                tmp = {}
                tmp['post_id'] = item.post_id
                tmp['user_name'] = User.objects.filter(id=item.user_id).first().name
                # get user's info
                query = UserInfo.objects.filter(id=item.user_id)
                if not query:
                    res['status'] = False
                    res['message'] = 'user info does not exist'
                    return JsonResponse(res)
                user_info = query.first()
                tmp['user_image'] = root_url + '/media/userImage/' + user_info.image
                tmp['create_time'] = item.create_time.timestamp().__floor__()
                tmp['content'] = item.comment
                q = PostPicture.objects.filter(post_id=item.post_id)
                if q:
                    tmp['picture'] = root_url + "/media/postImage/" + q.first().url
                else:   
                    tmp['picture'] = ""
                noticeList.append(tmp)
        elif qeury_type == 2:
            query = PostLove.objects.filter(post_id__in=post_ids)
            for item in query:
                tmp = {}
                tmp['post_id'] = item.post_id
                tmp['user_name'] = User.objects.filter(id=item.user_id).first().name
                # get user's info
                query = UserInfo.objects.filter(id=item.user_id)
                if not query:
                    res['status'] = False
                    res['message'] = 'user info does not exist'
                    return JsonResponse(res)
                user_info = query.first()
                tmp['user_image'] = root_url + '/media/userImage/' + user_info.image
                tmp['create_time'] = item.create_time.timestamp().__floor__()
                tmp['content'] = ""
                q = PostPicture.objects.filter(post_id=item.post_id)
                tmp['create_time'] = item.create_time.timestamp().__floor__()
                tmp['content'] = ""
                tmp['picture'] = ""
                noticeList.append(tmp)
        else:
            pass
        res['notice_list'] = sorted(noticeList, key=lambda x: x['create_time'], reverse=True)
        res['status'] = True
        res['message'] = 'ok'
    except Exception as e:
        print(e)
        res['status'] = False
        res['message'] = 'unexpected parameters'
    return JsonResponse(res)

@api_view(['POST'])
def followUser(request: HttpRequest):
    res = {}
    if request.method != "POST":
        res['status'] = False
        res['message'] = 'false method'
        return JsonResponse(res)
    try:
        # get parameters
        user_name = request.POST.get('user_name')
        target_user_name = request.POST.get('target_user_name')
        # check if user exists
        query = User.objects.filter(name=user_name)
        if not query:
            res['status'] = False
            res['message'] = 'user does not exist'
            return JsonResponse(res)
        user_id = query.first().id
        # check if target user exists
        query = User.objects.filter(name=target_user_name)
        if not query:
            res['status'] = False
            res['message'] = 'target user does not exist'
            return JsonResponse(res)
        target_user_id = query.first().id
        # check if user has followed target user
        query = UserFollow.objects.filter(user_id=user_id, follow_user_id=target_user_id)
        if query:
            # cancel follow
            query.delete()
            res['result'] = 0
        else:
            # add follow
            follow = UserFollow(user_id=user_id, follow_user_id=target_user_id)
            follow.save()
            res['result'] = 1
        res['status'] = True
        res['message'] = 'ok'
    except Exception as e:
        print(e)
        res['status'] = False
        res['message'] = 'unexpected parameters'
    return JsonResponse(res)

@api_view(['GET'])
def getAttentionList(request: HttpRequest):
    res = {}
    if request.method != "GET":
        res['status'] = False
        res['message'] = 'false method'
        return JsonResponse(res)
    try:
        # get parameters
        user_name = request.GET.get('user_name')
        type = int(request.GET.get('type'))
        # check if user exists
        query = User.objects.filter(name=user_name)
        if not query:
            res['status'] = False
            res['message'] = 'user does not exist'
            return JsonResponse(res)
        user_id = query.first().id
        userList = []
        if type == 0:
            # get user's follow list
            query = UserFollow.objects.filter(user_id=user_id)
            for item in query:
                target_user_id = item.follow_user_id
                tmp = getSingleUserInfo(user_id, target_user_id, root_url)
                userList.append(tmp)
        elif type == 1:
            # get user's fans list
            query = UserFollow.objects.filter(follow_user_id=user_id)
            for item in query:
                target_user_id = item.user_id
                tmp = getSingleUserInfo(user_id, target_user_id, root_url)
                userList.append(tmp)
        elif type == 2:
            # get user's hate list
            query = UserHate.objects.filter(user_id=user_id)
            for item in query:
                target_user_id = item.hate_user_id
                tmp = getSingleUserInfo(user_id, target_user_id, root_url)
                userList.append(tmp)
        res['user_list'] = userList
        res['status'] = True
        res['message'] = 'ok'
    except Exception as e:
        print(e)
        res['status'] = False
        res['message'] = 'unexpected parameters'
    return JsonResponse(res)

@api_view(['POST'])
def hateUser(request: HttpRequest):
    res = {}
    if request.method != "POST":
        res['status'] = False
        res['message'] = 'false method'
        return JsonResponse(res)
    try:
        # get parameters
        user_name = request.POST.get('user_name')
        target_user_name = request.POST.get('target_user_name')
        # check if user exists
        query = User.objects.filter(name=user_name)
        if not query:
            res['status'] = False
            res['message'] = 'user does not exist'
            return JsonResponse(res)
        user_id = query.first().id
        # check if target user exists
        query = User.objects.filter(name=target_user_name)
        if not query:
            res['status'] = False
            res['message'] = 'target user does not exist'
            return JsonResponse(res)
        target_user_id = query.first().id
        # check if user has hated target user
        query = UserHate.objects.filter(user_id=user_id, hate_user_id=target_user_id)
        if query:
            # cancel hate
            query.delete()
            res['result'] = 0
        else:
            # add hate
            hate = UserHate(user_id=user_id, hate_user_id=target_user_id)
            hate.save()
            res['result'] = 1
        res['status'] = True
        res['message'] = 'ok'
    except Exception as e:
        print(e)
        res['status'] = False
        res['message'] = 'unexpected parameters'
    return JsonResponse(res)

@api_view(['POST'])
def modifyUserName(request: HttpRequest):
    res = {}
    if request.method != "POST":
        res['status'] = False
        res['message'] = 'false method'
        return JsonResponse(res)
    try:
        # get parameters
        origin_user_name = request.POST.get('original_user_name')
        new_user_name = request.POST.get('new_user_name')
        # check if user exists
        query = User.objects.filter(name=origin_user_name)
        if not query:
            res['status'] = False
            res['message'] = 'user does not exist'
            return JsonResponse(res)
        user_id = query.first().id
        # modify user name
        user = query.first()
        user.name = new_user_name
        user.save()
        res['status'] = True
        res['message'] = 'ok'
    except Exception as e:
        print(e)
        res['status'] = False
        res['message'] = 'unexpected parameters'
    return JsonResponse(res)

@api_view(['POST'])
def modifyUserDescription(request: HttpRequest):
    res = {}
    if request.method != "POST":
        res['status'] = False
        res['message'] = 'false method'
        return JsonResponse(res)
    try:
        # get parameters
        user_name = request.POST.get('user_name')
        new_description = request.POST.get('new_description')
        # check if user exists
        query = User.objects.filter(name=user_name)
        if not query:
            res['status'] = False
            res['message'] = 'user does not exist'
            return JsonResponse(res)
        user_id = query.first().id
        # modify user info
        query = UserInfo.objects.filter(id=user_id)
        if not query:
            res['status'] = False
            res['message'] = 'user info does not exist'
            return JsonResponse(res)
        userInfo = query.first()
        userInfo.description = new_description
        userInfo.save()
        res['status'] = True
        res['message'] = 'ok'
    except Exception as e:
        print(e)
        res['status'] = False
        res['message'] = 'unexpected parameters'
    return JsonResponse(res)

@api_view(['POST'])
def modifyUserImage(request: HttpRequest):
    res = {}
    if request.method != "POST":
        res['status'] = False
        res['message'] = 'false method'
        return JsonResponse(res)
    try:
        # get parameters
        user_name = request.POST.get('user_name')
        file = request.FILES.get('image')
        # check if user exists
        query = User.objects.filter(name=user_name)
        if not query:
            res['status'] = False
            res['message'] = 'user does not exist'
            return JsonResponse(res)
        user_id = query.first().id
        # find user info
        query = UserInfo.objects.filter(id=user_id)
        user_info = query.first()
        if not query:
            res['status'] = False
            res['message'] = 'user info does not exist'
            return JsonResponse(res)
        # save image
        file_dir = './media/userImage/'
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        file_name =  str(int(time())) + '.' + file.name.split('.')[-1]
        file_path = file_dir + file_name
        if file.name.split('.')[-1] not in ['jpeg','jpg','png']:
            res['status'] = False
            res['message'] = 'file error'
            return JsonResponse(res)
        with open(file_path,'wb+') as f:
            f.write(file.read())
        # add image to database
        user_info.image = file_name
        user_info.save()
        res['status'] = True
        res['message'] = 'ok'
    except Exception as e:
        print(e)
        res['status'] = False
        res['message'] = 'unexpected parameters'
    return JsonResponse(res)

@api_view(['POST'])
def modifyUserPassword(request: HttpRequest):
    res = {}
    if request.method != "POST":
        res['status'] = False
        res['message'] = 'false method'
        return JsonResponse(res)
    try:
        # get parameters
        user_name = request.POST.get('user_name')
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        # check if user name match password
        query = User.objects.filter(name=user_name, password=old_password)
        if not query:
            res['status'] = False
            res['message'] = 'user name does not match password'
            return JsonResponse(res)
        # modify password
        user = query.first()
        user.password = new_password
        user.save()
        res['status'] = True
        res['message'] = 'ok'
    except Exception as e:
        print(e)
        res['status'] = False
        res['message'] = 'unexpected parameters'
    return JsonResponse(res)