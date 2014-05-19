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
from django.utils.timezone import utc
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
    timenow = datetime.datetime.utcnow().replace(tzinfo=utc)
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

@csrf_exempt   ###保证对此接口的访问不需要csrf
def post_topic_webview(request, current_uid):
    userid = int(current_uid)
    user = User.objects.get(id=userid)
    if not user:
        return HttpResponse('INVALID_USER')
    content = request.POST.get('topic_content')
    if not content:
        return HttpResponseRedirect('/quan/gettopicwebview/%s/' % current_uid)
    timenow = datetime.datetime.utcnow().replace(tzinfo=utc)
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
        return HttpResponseRedirect('/quan/gettopicwebview/%s/' % current_uid)
    else:
        return HttpResponse('POST_TOPIC_ERROR')

def circletopic_encode(topics):
    rets = []
    number = len(list(topics))
    for i in range(0, number):
        topic = topics[i]
        t = {}
        t['from_user'] = topic.from_user
        t['content'] = topic.content
        t['create_time'] = topic.create_time
        t['update_time'] = topic.update_time
        c = []
        t['comments'] = c
        rets.append(t)
    return rets

@csrf_exempt       
def get_circletopic(request):
    (authed, username, password, user) = auth_user(request)
    if not authed or not user:
        return HttpResponse('AUTH_FAILED')
    timenow = datetime.datetime.utcnow().replace(tzinfo=utc)
    circle = user.circle
    circle.last_access = timenow # update the last-access time.
    circle.save()
    topicids = circle.topic_ids
    print("##topicids:", topicids)
    circletopics = []
    for topicid in reversed(topicids):
        topic = Topic.objects.get(id = topicid)
        circletopics.append(topic)
    print("##circletopics:", circletopics)
    return HttpResponse(circletopic_encode(circletopics))

def get_topic_webview(request, uid):
    userid = int(uid)
    user = User.objects.get(id=userid)
    if not user:
        return HttpResponse('INVALID_USER')
    timenow = datetime.datetime.utcnow().replace(tzinfo=utc)
    circle = user.circle
    circle.last_access = timenow # update the last-access time.
    circle.save()
    topicids = circle.topic_ids
    circletopics = []
    for topicid in reversed(topicids):
        topic = Topic.objects.get(id = topicid)
        circletopics.append(topic)
    context = {}
    context['topics'] = circletopics
    context['current_uid'] = uid
    t = get_template("quan/topics_webview.html") 
    #return t.render(Context(context))
    return HttpResponse(t.render(Context(context)))

@csrf_exempt
def addtopiccomment(request, topicid):
    (authed, username, password, user) = auth_user(request)
    timenow = datetime.datetime.utcnow().replace(tzinfo=utc)
    circle = user.circle
    circle.last_access = timenow # update the last-access time.
    circle.save()
    topic = Topic.objects.get(id=int(topicid))
    comment = Comment(from_user = user.id, topic=topic, content=request.POST['comment'], create_time=timenow)
    comment.save()
    return get_circletopic(request)
        

@csrf_exempt
def addcommentwebview(request, current_uid, topicid):
    userid = int(current_uid)
    user = User.objects.get(id=userid)
    if not user:
        return HttpResponse('INVALID_USER')
    topic = Topic.objects.get(id=int(topicid))
    timenow = datetime.datetime.utcnow().replace(tzinfo=utc)
    comment = Comment(from_user = user, topic=topic, content=request.POST['comment'], create_time=timenow)
    comment.save()
    return HttpResponseRedirect('/quan/gettopicwebview/%s/' % current_uid)


