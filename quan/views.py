# Create your views here.
'''
Created on 2014.5.3

@author: shengeng
'''

from django.http import *
from baby.models import Baby
from django.contrib import auth
from django.contrib.auth.models import User
from django.utils import http
from django.contrib.gis.geos import Point, fromstr
from django.contrib.gis.measure import D # alias for Distance
from django.views.decorators.csrf import csrf_exempt
from .models import *
from datetime import *
from .utils import *
from users.utils import *
import json, base64, traceback, random
import datetime,time

@csrf_exempt   ###保证对此接口的访问不需要csrf
def post_topic(request):
    (authed, username, password, user) = auth_user(request)
    if not authed or not user:
        return HttpResponse('AUTH_FAILED')
    content = request.POST.get('content')
    if not content:
        return HttpResponse('CONTENT_NULL')
    timenow = datetime.datetime.now()
    topic = Topic(from_user = user,
                 content =  content,
                 create_time = timenow,
                 update_time = timenow)
    ret = topic.save()
    topic_id = topic.id
    circle = user.circle
    if topic_id and circle:
        circle.add_topic(topic)
        return HttpResponse('True')
    else:
        return HttpResponse('POST_TOPIC_ERROR')
        

    
    
    
    
    
    