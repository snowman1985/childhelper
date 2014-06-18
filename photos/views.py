from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import *
from django.contrib import auth
from django.contrib.auth.models import User
from django.utils import http
from django.contrib.sites.models import get_current_site
from users.utils import *
from .models import *

# Create your views here.

#need apt-get install libjpeg-dev
#need pip install -I pillow
#need  pip install django-imagekit

@csrf_exempt
def upload_head(request):
    try :
      (authed, username, password, user) = auth_user(request)
      if not authed or not user:
        return HttpResponse('AUTH_FAILED')
      if request.method == 'GET':
          return HttpResponse('HTTP_METHOD_ERR')
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
    
    
@csrf_exempt
def get_head(request):
    try :
      (authed, username, password, user) = auth_user(request)
      if not authed or not user:
        return HttpResponse('AUTH_FAILED')
      if request.method == 'GET':
          return HttpResponse('HTTP_METHOD_ERR')
      head = Head.objects.get(username = user.username)
      full_url = ''.join(['http://', request.META['HTTP_HOST'], head.head_thumbnail.url])
      print(full_url)
      return HttpResponse(full_url)
    except Exception as e:
      print('Exception:' + str(e))
      return HttpResponse('GET_HEAD_ERR')
