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
from django.template.loader import get_template
from django.template import Context
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
    circle.last_access = timenow # update the last-access time.
    circle.save()
    if topic_id and circle:
        circle.add_topic(topic)
        return HttpResponse('True')
    else:
        return HttpResponse('POST_TOPIC_ERROR')

@csrf_exempt       
def get_circletopic(request):
    (authed, username, password, user) = auth_user(request)
    if not authed or not user:
        return HttpResponse('AUTH_FAILED')
    circle = user.circle
    circle.last_access = datetime.datetime.now() # update the last-access time.
    circle.save()
    topicids = circle.topic_ids
    print("##topicids:", topicids)
    circletopics = []
    for topicid in reversed(topicids):
        topic = Topic.objects.get(id = topicid)
        circletopics.append(topic)
    print("##circletopics:", circletopics)
    context = {}
    context['topics'] = circletopics
    t = get_template("quan/topics.html") 
    print("##get template:", t)
    return HttpResponse(t.render(Context(context)))

def get_topic_webview(request, uid):
    userid = int(uid)
    user = User.objects.get(id=userid)
    if not user:
        return HttpResponse('INVALID_UID')
    circle = user.circle
    circle.last_access = datetime.datetime.now() # update the last-access time.
    circle.save()
    topicids = circle.topic_ids
    circletopics = []
    for topicid in reversed(topicids):
        topic = Topic.objects.get(id = topicid)
        circletopics.append(topic)
    context = {}
    context['topics'] = circletopics
    t = get_template("quan/topics_webview.html") 
    #return t.render(Context(context))
    return HttpResponse(t.render(Context(context)))

@csrf_exempt
def addtopiccomment(request, topicid):
    (authed, username, password, user) = auth_user(request)
    circle = user.circle
    circle.last_access = datetime.datetime.now() # update the last-access time.
    circle.save()
    topic = Topic.objects.get(id=int(topicid))
    comment = Comment(from_user = user.id, topic=topic, content=request.POST['comment'], create_time=datetime.datetime.now())
    comment.save()
    return get_circletopic(request)
        

@csrf_exempt
def addcommentwebview(request, topicid):
    topic = Topic.objects.get(id=int(topicid))
    comment = Comment(from_user = 10, topic=topic, content=request.POST['comment'], create_time=datetime.datetime.now())
    comment.save()
    return get_topic_webview(request, topic.from_user.id)


