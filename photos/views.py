from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import *
from django.contrib import auth
from django.contrib.auth.models import User
from django.utils import http
from django.contrib.sites.models import get_current_site
from .models import *

# Create your views here.

#need apt-get install libjpeg-dev
#need pip install -I pillow
#need  pip install django-imagekit

@csrf_exempt
def upload_head(request):
    try :
      if request.method == 'GET':
          return HttpResponse('HTTP_METHOD_ERR')
      print('request.META: ')
      print(request.META)
      print('request.POST: ')
      print(request.POST)
      print('request.FILES: ')
      print(request.FILES)
      head_data = request.FILES['head']
      photo = Photo()
      photo.name = request.POST['username']
      photo.head_orig = head_data
      photo.save()
      full_url = ''.join(['http://', request.META['HTTP_HOST'], photo.head_thumbnail.url])
      print(full_url)
      return HttpResponse(full_url)
    except Exception as e:
      print(str(e))
      return HttpResponse(str(e))
    
