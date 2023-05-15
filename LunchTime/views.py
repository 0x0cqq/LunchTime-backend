from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
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
def index(request):
    return HttpResponse("Hello, world. You're at the LunchTime index.")

def register_without_verification(request):
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
def verify_email(request):
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
def register(request):
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
        res['status'] = True
        res['message'] = 'ok'
    except:
        res['status'] = False
        res['message'] = 'unexpected parameters'
    return JsonResponse(res)

@api_view(['POST'])
def login(request):
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
def getPosts(request):
    res = {}
    if request.method != "GET":
        res['status'] = False
        res['message'] = 'false method'
        return JsonResponse(res)
    try:
        user_name = request.POST.get('user_name')
        type = request.POST.get('type')
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
            tmp['post_id'] = post.post_id
            tmp['user_name'] = post_user_name
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
        if type == 1:
            sorted_posts = sorted(posts, key=lambda x: x["post_id"], reverse=True)
        elif type == 2:
            sorted_posts = sorted(posts, key=lambda x: x["popularity"], reverse=True)
        else:
            sorted_posts = sorted(posts, key=lambda x: x["post_id"], reverse=True)
            # TODO: filter by attention
        res['status'] = True
        res['message'] = 'ok'
        res['posts'] = sorted_posts

    except Exception as e:
        print(e)
        res['status'] = False
        res['message'] = 'unexpected parameters'
    return JsonResponse(res)


@api_view(['GET'])
def getPostDetail(request):
    res = {}
    if request.method != "GET":
        res['status'] = False
        res['message'] = 'false method'
        return JsonResponse(res)
    try:
        user_name = request.POST.get('user_name')
        post_id = request.POST.get('post_id')
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
def post(request):
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
        print("files:", files)
        for index, file in enumerate(files):
            print("file:", file)
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
def lovePost(request):
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
def commentPost(request):
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
def getNoticeLove(request):
    res = {}
    if request.method != "GET":
        res['status'] = False
        res['message'] = 'false method'
        return JsonResponse(res)
    try:
        # get parameters
        user_name = request.POST.get('user_name')
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
        # get user's love list
        loveList = []
        query = PostLove.objects.filter(post_id__in=post_ids)
        for item in query:
            tmp = {}
            tmp['post_id'] = item.post_id
            tmp['user_name'] = User.objects.filter(id=item.user_id).first().name
            tmp['create_time'] = item.create_time.timestamp().__floor__()
            loveList.append(tmp)
        res['notice_list'] = loveList
        res['status'] = True
        res['message'] = 'ok'
    except Exception as e:
        print(e)
        res['status'] = False
        res['message'] = 'unexpected parameters'
    return JsonResponse(res)

@api_view(['GET'])
def getNoticeComment(request):
    res = {}
    if request.method != "GET":
        res['status'] = False
        res['message'] = 'false method'
        return JsonResponse(res)
    try:
        # get parameters
        user_name = request.POST.get('user_name')
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
        # get user's comment list
        commentList = []
        query = PostComment.objects.filter(post_id__in=post_ids)
        for item in query:
            tmp = {}
            tmp['post_id'] = item.post_id
            tmp['user_name'] = User.objects.filter(id=item.user_id).first().name
            tmp['create_time'] = item.create_time.timestamp().__floor__()
            tmp['content'] = item.comment
            commentList.append(tmp)
        res['notice_list'] = commentList
        res['status'] = True
        res['message'] = 'ok'
    except Exception as e:
        print(e)
        res['status'] = False
        res['message'] = 'unexpected parameters'
    return JsonResponse(res)