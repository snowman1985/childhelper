# Create your views here.
'''
Created on Nov 2, 2013

@author: shengeng
'''

from django.http import *
from django.contrib import auth
from django.contrib.auth.models import User
from django.utils import http
from django.contrib.gis.geos import Point, fromstr
from django.contrib.gis.measure import D # alias for Distance
from django.views.decorators.csrf import csrf_exempt
from .models import *
from datetime import *
from .utils import *
import json, base64, traceback, random
import datetime,time
from utils.baidumap import *
from baby.models import Baby
from quan.models import *

@csrf_exempt   ###保证对此接口的访问不需要csrf
def check_user_name(username):
    if User.objects.filter(username=username).exists():
        return "exist"
    else:
        return "available"

@csrf_exempt
def register(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    username = http.urlsafe_base64_decode(username)
    password = http.urlsafe_base64_decode(password)
    username = username.decode()
    password = password.decode()
    
    if check_user_name(username) == "exist":
        return HttpResponse("DuplicateName")
    print('user register, ' + username + password)
    baby = Baby()
    baby_name = request.POST.get('babyname')
    baby_height = request.POST.get('babyheight')
    baby_weight = request.POST.get('babyweight')
    baby_birthday = request.POST.get('birthday')
    baby_sex = request.POST.get('babysex')
    baby_homeaddr = request.POST.get('homeaddr')
    baby_schooladdr = request.POST.get('schooladdr')
    
    baby.name = baby_name
    baby.height = baby_height
    baby.weight = baby_weight
    baby.birthday = datetime.datetime.fromtimestamp(time.mktime(time.strptime(baby_birthday,"%Y-%m-%d")))
    baby.sex = baby_sex
    baby.homeaddr = baby_homeaddr
    baby.type = 1   ###这个注册用户来自app
    
    #get latitude and longitude from baidumap.and save as a geo point.
    need_circle = False
    if(baby_homeaddr):
        baiduresp = get_baidu_location(baby_homeaddr)
        if baiduresp['result']['location']['lng'] and baiduresp['result']['location']['lat']:
            lng = baiduresp['result']['location']['lng']
            lat = baiduresp['result']['location']['lat']
            baby.homepoint = fromstr("POINT(%s %s)" % (lng, lat))
            need_circle = True
        else:
            baby.homepoint = None
    else:
        baby.homepoint = None
    baby.schooladdr = baby_schooladdr
    print('user register, add a new baby %s, birthday: %s' % (baby.name, baby.birthday.strftime("%Y-%m-%d")))
# 产生一个新用户:
    user = User.objects.create_user(username = username, password = password)
    user.baby = baby
    user.save()
    baby.save()
    if need_circle:
        create_circle(user, 1, baby.homepoint)
    response = 'False'
    if baby is None:
        response = 'False'
    else:
        response = 'True'
    return HttpResponse(response)

@csrf_exempt
def update(request):
    (authed, username, password, user) = auth_user(request)
    if not authed or not user:
        return HttpResponse('AUTH_FAILED')
    baby_height = request.POST.get('babyheight')
    baby_weight = request.POST.get('babyweight')
    baby_birthday = request.POST.get('birthday')
    baby_sex = request.POST.get('babysex')
    baby_name = request.POST.get('babyname')
    baby_homeaddr = request.POST.get('homeaddr')
    baby_schooladdr = request.POST.get('schooladdr')
    print(user)
    baby = User.objects.get(id=user.id).baby
    print(baby)
    if not baby:
        response = 'Can not found your baby in db.'
        return HttpResponse(response)
    if baby_weight:
        baby.weight = float(baby_weight)
    if baby_height:
        baby.height = float(baby_height)
    if baby_birthday:
        baby.birthday = datetime.datetime.fromtimestamp(time.mktime(time.strptime(baby_birthday,"%Y-%m-%d")))
    print('user update, update baby info %s, birthday: %s' % (baby.name, baby_birthday))
    if baby_sex:
        baby.sex = baby_sex
    if baby_name:
        baby.name = baby_name
    if baby_homeaddr:
        baby.homeaddr = baby_homeaddr
        #get latitude and longitude from baidumap.and save as a geo point.
        baiduresp = get_baidu_location(baby_homeaddr)
        if baiduresp['result']['location']['lng'] and baiduresp['result']['location']['lat']:
            lng = baiduresp['result']['location']['lng']
            lat = baiduresp['result']['location']['lat']
            baby.homepoint = fromstr("POINT(%s %s)" % (lng, lat))
        else:
            baby.homepoint = None
    else:
        baby.homepoint = None
    if baby_schooladdr:
        baby.schooladdr = baby_schooladdr
    print('user update info: ')
    print(request.POST)
    baby.save()
    response = 'False'
    if baby is None:
        response = 'False'
    else:
        response = 'True'
    return HttpResponse(response)

def data_encode(*data_array):
    rets =''
    for (data) in data_array:
      rets = ('%s%s') % (rets, data)
    return json.dumps(rets, ensure_ascii=False)

@csrf_exempt
def informationcheck(request):
    try:
        (authed, username, password, user) = auth_user(request)
        if not user:
            return HttpResponse('False')
        else:
            return HttpResponse('True')
    except Exception as e:
        print(e)
        return HttpResponse(e)

@csrf_exempt
def getinfo(request):
    try:
        (authed, username, password, user) = auth_user(request)
        if not user:
            return HttpResponse('AUTH_FAILED')
        else:
            resp = {}
            resp['username'] = user.username
            resp['userid'] = user.id
            return HttpResponse(data_encode(resp))
    except Exception as e:
        print(e)
        return HttpResponse(e)

def gethomepic(request):
    try:
        (authed, username, password, user) = auth_user(request)
        if not user:
            return HttpResponse('AUTH_FAILED')
        else:
            piclink = "http://wjbb.cloudapp.net/homepic/%d.jpg"%random.randint(0,9)
            print(request.get_host())
            return HttpResponse(piclink)
    except Exception as e:
        print(e)
        return HttpResponse(e)
