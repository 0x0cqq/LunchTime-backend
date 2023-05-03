from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from LunchTime.models import *
from LunchTime.utils import *

# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the LunchTime index.")

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
        