from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from LunchTime.models import *
from LunchTime.utils import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from time import time

root_url = "http://lunchtime.cqqqwq.com:8000"
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
            verify_email = query[0]
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
            verify_email = query[0]
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

@api_view(['POST'])
def getPostsByTime(request):
    res = {}
    if request.method != "POST":
        res['status'] = False
        res['message'] = 'false method'
        return JsonResponse(res)
    try:
        user_name = request.POST.get('user_name')
        # get all posts
        objects = Post.objects.all()
        posts = []
        for post in objects:
            tmp = {}
            query = User.objects.filter(id=post.user_id)
            user_name = query[0].name
            tmp['post_id'] = post.post_id
            tmp['user_name'] = user_name
            tmp['create_time'] = post.create_time
            tmp['tag'] = post.tag
            tmp['title'] = post.title
            tmp['content'] = post.content
            tmp['location'] = post.location
            tmp['love_count'] = post.love_count
            tmp['comment_count'] = post.comment_count
            tmp['save_count'] = post.save_count
            tmp['picture'] = []
            # get picture list
            queries = PostPicture.objects.filter(post_id=post.post_id)
            for q in queries:
                tmp['picture'].append(root_url + "/media/postImage/" + q.url)
            posts.append(tmp)
        res['status'] = True
        res['message'] = 'ok'
        res['posts'] = posts

    except Exception as e:
        print(e)
        res['status'] = False
        res['message'] = 'unexpected parameters'
    return JsonResponse(res)

@api_view(['POST'])
def getPostDetail(request):
    res = {}
    if request.method != "POST":
        res['status'] = False
        res['message'] = 'false method'
        return JsonResponse(res)
    try:
        user_name = request.POST.get('user_name')
        post_id = request.POST.get('post_id')
        # get post
        query = Post.objects.filter(post_id=post_id)
        if not query:
            res['status'] = False
            res['message'] = 'post does not exist'
            return JsonResponse(res)
        post = query[0]
        res['user_name'] = user_name
        res['post_id'] = post.post_id
        res['create_time'] = post.create_time
        res['tag'] = post.tag
        res['title'] = post.title
        res['content'] = post.content
        res['location'] = post.location
        res['love_count'] = post.love_count
        res['save_count'] = post.save_count
        res['comment_count'] = post.comment_count
        # add picture list
        res['picture'] = []
        queries = PostPicture.objects.filter(post_id=post_id)
        for q in queries:
            res['picture'].append(root_url + "/media/postImage/" + q.url)
        # add comment list
        res['comments'] = []
        queries = PostComment.objects.filter(post_id=post_id)
        for q in queries:
            tmp = {}
            query = User.objects.filter(id=q.user_id)
            tmp['user_name'] = query[0].name
            tmp['content'] = q.comment
            tmp['create_time'] = str(q.create_time)
            res['comments'].append(tmp)
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
        user_id = query[0].id
        # get current time
        create_time = timezone.now()
        create_time = timezone.localtime(create_time)
        create_time = create_time.strftime("%Y-%m-%d %H:%M:%S")
        # add new post to database
        post = Post(user_id=user_id, tag=tag, title=title, content=content, location=location, create_time=create_time,
            love_count=0, comment_count=0, save_count=0)
        post.save()

        # get picture list
        files = request.FILES.getlist('picture')
        print("files:", files)
        for index, file in enumerate(files):
            print("file:", file)
            file_name =  str(int(time())) + "_" + str(index) + '.' + file.name.split('.')[-1]
            file_path = './media/postImage/' + file_name
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