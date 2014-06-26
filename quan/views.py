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
from photos.models import *
import json, base64, traceback, random
import datetime,time


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


def get_topic_webview(request, uid):
    userid = int(uid)
    user = User.objects.get(id=userid)
    if not user:
        print("##invalid user")
        return HttpResponse('INVALID_USER')
    timenow = datetime.datetime.utcnow().replace(tzinfo=utc)
    try:
      circle = user.circle
    except Exception as e:
      print("##get user circle exception:", e)
      return HttpResponse("请填写您所在位置，我们会为您创建圈子")
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


#根据topicid显示一个topic的详细信息webview
def get_topicbyid_webview(request, userid, topicid):
    try:
        topic = Topic.objects.get(id = topicid)
        if not topic:
            return HttpResponse("INVALID_TOPICID")
    except Exception as e:
        return HttpResponse("INVALID_TOPICID")
    try:
        user = User.objects.get(id=userid)
        if not topic:
            return HttpResponse("INVALID_USERID")
    except Exception as e:
            return HttpResponse("INVALID_USERID")
    context = {}
    context['headurl'] = getheadurl(topic.from_user)
    context['topic'] = topic
    context['current_uid'] = userid
    t = get_template("quan/topic_webview.html")
    return HttpResponse(t.render(Context(context)))


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
    return HttpResponseRedirect('/quan/gettopicbyidwebview/%s/%s/' % (current_uid, topicid))



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
        return HttpResponse('OK')
    else:
        return HttpResponse('POST_TOPIC_ERROR')


@csrf_exempt
def add_comment(request):
    (authed, username, password, user) = auth_user(request)
    timenow = datetime.datetime.utcnow().replace(tzinfo=utc)
    circle = user.circle
    if not circle:
        return HttpResponse('CIRCLE_NOT_FOUND_ERROR')
    circle.last_access = timenow # update the last-access time.
    circle.save()
    topicid = request.POST.get('topicid')
    if not topicid:
        return HttpResponse('TOPICID_NULL_ERROR')
    topic = Topic.objects.get(id=int(topicid))
    if not topic:
        return HttpResponse('TOPIC_NOT_FOUND_ERROR')
    comment = Comment(from_user = user, topic=topic, content=request.POST['comment'], create_time=timenow)
    comment.save()
    if comment:
        return HttpResponse('OK')
    else:
        return HttpResponse('ADD_COMMENT_ERROR')


def comments_encode(comments):
    rets = []
    number = len(list(comments))
    for i in range(0, number):
        comment = comments[i]
        c = {}
        c['from_user'] = comment.from_user.username
        c['content'] = comment.content
        c['create_time'] = comment.create_time.strftime('%Y-%m-%d %H:%M:%S' )
        print(c)
        rets.append(c)
    return rets


def circletopiclist_encode(topics):
    rets = []
    number = len(list(topics))
    for i in range(0, number):
        topic = topics[i]
        t = {}
        t['topicid'] = topic.id
        t['from_user'] = topic.from_user.username
        t['headurl'] = getheadurl(topic.from_user)
        t['content'] = topic.content
        t['comments_num'] = len(Comment.objects.filter(topic = topic))
        t['create_time'] = topic.create_time.strftime('%Y-%m-%d %H:%M:%S' )
        t['update_time'] = topic.update_time.strftime('%Y-%m-%d %H:%M:%S' )
        rets.append(t)
    return json.dumps(rets, ensure_ascii=False)


def circletopic_encode(topics):
    rets = []
    number = len(list(topics))
    for i in range(0, number):
        topic = topics[i]
        t = {}
        t['topicid'] = topic.id
        t['from_user'] = topic.from_user.username
        t['content'] = topic.content
        t['create_time'] = topic.create_time.strftime('%Y-%m-%d %H:%M:%S' )
        t['update_time'] = topic.update_time.strftime('%Y-%m-%d %H:%M:%S' )
        t['comments'] = comments_encode(Comment.objects.filter(topic = topic))
        print(t)
        rets.append(t)
    return json.dumps(rets, ensure_ascii=False)


@csrf_exempt       
def get_circletopiclist(request):
    (authed, username, password, user) = auth_user(request)
    if not authed or not user:
        return HttpResponse('AUTH_FAILED')
    timenow = datetime.datetime.utcnow().replace(tzinfo=utc)
    circle = user.circle
    if not circle:
        return HttpResponse('CIRCLE_NOT_EXIST')
    circle.last_access = timenow # update the last-access time.
    circle.save()
    topicids = circle.topic_ids
    circletopics = []
    for topicid in reversed(topicids):
        topic = Topic.objects.get(id = topicid)
        circletopics.append(topic)
    return HttpResponse(circletopiclist_encode(circletopics))


@csrf_exempt       
def get_circletopic(request):
    (authed, username, password, user) = auth_user(request)
    if not authed or not user:
        return HttpResponse('AUTH_FAILED')
    timenow = datetime.datetime.utcnow().replace(tzinfo=utc)
    circle = user.circle
    if not circle:
        return HttpResponse('CIRCLE_NOT_EXIST')
    circle.last_access = timenow # update the last-access time.
    circle.save()
    topicids = circle.topic_ids
    circletopics = []
    for topicid in reversed(topicids):
        topic = Topic.objects.get(id = topicid)
        circletopics.append(topic)
    return HttpResponse(circletopic_encode(circletopics))

