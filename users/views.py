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
from django.contrib.auth import authenticate,login,logout  
from .models import *
from datetime import *
from .utils import *
import json, base64, traceback, random
import datetime, time, logging
from utils.baidumap import *
from baby.models import Baby
from jiaquan.models import *
from photos.models import *

log=logging.getLogger('customapp')

@csrf_exempt   ###保证对此接口的访问不需要csrf
def check_user_name(username):
    if User.objects.filter(username=username).exists():
        return "exist"
    else:
        return "available"

@csrf_exempt
def user_login(request):
    try:
        if request.method == "GET":
            return HttpResponse('HTTP_METHOD_ERR')
        username = request.POST.get('username')
        password = request.POST.get('password')
        print("user login username base64 is :" + username)
        username = http.urlsafe_base64_decode(username)
        password = http.urlsafe_base64_decode(password)
        username = username.decode()
        password = password.decode()
        user = authenticate(username=username, password=password)
        if user is not None:  
            login(request, user)
            return HttpResponse('OK')
        else:  
            return HttpResponse('AUTH_FAILED')
    except Exception as e:
        log.error(e)
        return HttpResponse('EXCEPTION')
  
@csrf_exempt
def user_logout(request):
    try:
        if request.method == "GET":
            return HttpResponse('HTTP_METHOD_ERR')
        (authed, username, password, user) = auth_user(request)
        if not user or not authed:
             return HttpResponse('AUTH_FAILED')
        logout(request)
        return HttpResponse('OK')
    except Exception as e:
        log.error(e)
        return HttpResponse('EXCEPTION')

@csrf_exempt
def register(request):
    try:
        if request.method == "GET":
            return HttpResponse('HTTP_METHOD_ERR')
        username = request.POST.get('username')
        password = request.POST.get('password')
        username = http.urlsafe_base64_decode(username)
        password = http.urlsafe_base64_decode(password)
        username = username.decode()
        password = password.decode()
        if check_user_name(username) == "exist":
            return HttpResponse("DUMPLICATE_NAME")
        log.debug('user register %s  %s ' , username, password)
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
        try:
            baby.birthday = datetime.datetime.fromtimestamp(time.mktime(time.strptime(baby_birthday,"%Y-%m-%d")))
        except Exception as e:
            log.error(e)
            return HttpResponse('BIRTHDAY_FORMAT_ERR')
        baby.sex = baby_sex
        baby.type = 1   ###这个注册用户来自app
        #get latitude and longitude from baidumap.and save as a geo point.
        need_circle = False
        try:
            if(baby_homeaddr):
                baiduresp = get_baidu_location(baby_homeaddr)
                if baiduresp['result']['location']['lng'] and baiduresp['result']['location']['lat']:
                    lng = baiduresp['result']['location']['lng']
                    lat = baiduresp['result']['location']['lat']
                    baby.homepoint = fromstr("POINT(%s %s)" % (lng, lat))
                    baby.city = get_baidu_city(lat, lng)
                    baby.homeaddr = baby_homeaddr
                    need_circle = True
                else:
                    baby.homepoint = None
                    baby.city = None
                    baby.homeaddr = None
            else:
                baby.homepoint = None
                baby.city = None
                baby.homeaddr = None
        except Exception as e:
            baby.homepoint = None
            baby.city = None
            baby.homeaddr = None
            log.error(e)
            return HttpResponse('HOMEADDR_FORMAT_ERR')
        ##try to save the school address
        try:
            if(baby_schooladdr):
                baiduresp = get_baidu_location(baby_schooladdr)
                if baiduresp['result']['location']['lng'] and baiduresp['result']['location']['lat']:
                    lng = baiduresp['result']['location']['lng']
                    lat = baiduresp['result']['location']['lat']
                    baby.schooladdr = fromstr("POINT(%s %s)" % (lng, lat))
                    baby.schooladdr = baby_schooladdr
                    need_circle = True
                else:
                    baby.schooladdr = None
                    baby.schooladdr = None
            else:
                baby.schooladdr = None
                baby.schooladdr = None
        except Exception as e:
            baby.schooladdr = None
            baby.schooladdr = None
            log.error(e)
            return HttpResponse('SCHOOLADDR_FORMAT_ERR')
        log.info('user register, add a new baby %s, birthday: %s' % (baby.name, baby.birthday.strftime("%Y-%m-%d")))
    # 产生一个新用户:
        user = User.objects.create_user(username = username, password = password)
        user.baby = baby
        user.save()
        baby.save()
        if baby is None:
            return HttpResponse("EXCEPTION")
        else:
            if need_circle:
                print("##create circle for user " + user.username)
                create_circle(user, 1, baby.homepoint)
            return HttpResponse("OK")
    except Exception as e:
        return HttpResponse("EXCEPTION")

@csrf_exempt
def update(request):
    try:
        if request.method == "GET":
            return HttpResponse('HTTP_METHOD_ERR')
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
        baby = User.objects.get(id=user.id).baby
        if not baby:
            response = 'BABY_INFO_NULL'
            return HttpResponse(response)
        if baby_weight:
            baby.weight = float(baby_weight)
        if baby_height:
            baby.height = float(baby_height)
        try:
            if baby_birthday:
                baby.birthday = datetime.datetime.fromtimestamp(time.mktime(time.strptime(baby_birthday,"%Y-%m-%d")))
        except Exception as e:
            print(e)
            return HttpResponse('BIRTHDAY_FORMAT_ERR')
        print('user update, update baby info %s, birthday: %s' % (baby.name, baby_birthday))
        if baby_sex:
            baby.sex = baby_sex
        if baby_name:
            baby.name = baby_name
        try:
            if(baby_homeaddr):
                baiduresp = get_baidu_location(baby_homeaddr)
                if baiduresp['result']['location']['lng'] and baiduresp['result']['location']['lat']:
                    lng = baiduresp['result']['location']['lng']
                    lat = baiduresp['result']['location']['lat']
                    baby.homepoint = fromstr("POINT(%s %s)" % (lng, lat))
                    baby.city = get_baidu_city(lat, lng)
                    baby.homeaddr = baby_homeaddr
                    print("##delete old circle")
                    if remove_circle(user, 1) != 'OK':
                        return HttpResponse('UPDATE_CIRCLE_ERR')
                    print("##re-create circle")
                    if create_circle(user, 1, baby.homepoint) != 'OK':
                        return HttpResponse('CREATE_CIRCLE_ERR')
                else:
                    return HttpResponse('HOMEADDR_FORMAT_ERR')
        except Exception as e:
            print(e)
            return HttpResponse('HOMEADDR_FORMAT_EXCEPTION')
        if baby_schooladdr:
            baby.schooladdr = baby_schooladdr
        baby.save()
        response = 'False'
        if baby is None:
            return HttpResponse('EXCEPTION')
        else:
            return HttpResponse('OK')
    except Exception as e:
        print(e)
        return HttpResponse('EXCEPTION')

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
            print("##user not pass")
            return HttpResponse('False')
        else:
            print("##user check pass")
            return HttpResponse('True')
    except Exception as e:
        print(e)
        return HttpResponse(e)

@csrf_exempt
def getinfo(request):
    try:
        if request.method == "POST":
            return HttpResponse('HTTP_METHOD_ERR')
        (authed, username, password, user) = auth_user(request)
        if not user:
             return HttpResponse('AUTH_FAILED')
        else:
            baby = user.baby
            resp = {}
            resp['username'] = user.username
            resp['userid'] = user.id
            resp['babyname'] = baby.name
            resp['birthday'] = baby.birthday.strftime("%Y-%m-%d")
            resp['sex'] = baby.sex
            resp['weight'] = baby.weight
            resp['height'] = baby.height
            resp['city'] = baby.city
            resp['homeaddr'] = baby.homeaddr
            resp['schooladdr'] = baby.schooladdr
            return HttpResponse(json.dumps(resp, ensure_ascii=False))
    except Exception as e:
        print(e)
        return HttpResponse(e)


@csrf_exempt
def upload_head(request):
    try :
        if request.method == 'GET':
            return HttpResponse('HTTP_METHOD_ERR')
        (authed, username, password, user) = auth_user(request)
        if not authed or not user:
            return HttpResponse('AUTH_FAILED')
        head_data = request.FILES['head']
        head = Head()
        head.username = user.username
        head.head_orig = head_data
        head.save()
        full_url = ''.join(['http://', request.META['HTTP_HOST'], head.head_thumbnail.url])
        print(full_url)
        return HttpResponse(full_url)
    except Exception as e:
        print('Exception:' + str(e))
        return HttpResponse('UPLOAD_ERR')
    
    
def get_head(request):
    try :
        if request.method == 'POST':
            return HttpResponse('HTTP_METHOD_ERR')
        (authed, username, password, user) = auth_user(request)
        if not authed or not user:
            return HttpResponse('AUTH_FAILED')
        full_url = getheadurl(user)
        print(full_url)
        return HttpResponse(full_url)
    except Exception as e:
        print('Exception:' + str(e))
        return HttpResponse('GET_HEAD_ERR')


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
