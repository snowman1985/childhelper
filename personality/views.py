from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib import auth
from django.http import *
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET
from django.core.paginator import Paginator, EmptyPage
from tlquan.models import TlTopic
from jiaquan.models import JiaTopic 

# Create your views here.

@login_required
@require_GET
def list_person_topics(request):
    try:
        (authed, username, password, user) = auth_user(request)
        if not authed or not user:
            return HttpResponse("AUTH_FAILED")
        tltopics = TlTopic.objects.filter(from_user=request.user)
        jiaquantopics = JiaTopic.objects.filter(from_user=request.user)
    
        page = request.Get.get('page')
        if not page:
            page = 1
        else:
            page = int(page)

        number = request.GET.get('number')
        if not number:
            number = 5
        else:
            number = int(number)

        topics_list = list(tltopics)+list(jiaquantopics)
        topics_list.sort(key=lambda topic:topic.update_time, reverse=True)
        paginator = Paginator(topics_list, number)
        try:
            return HttpResponse(json_serialize(status='OK', result={'topics':circletopiclist_encode(paginator.page(page))}))
        except EmptyPage:
            return HttpResponse(json_serialize(status='OK', result={'topics':circletopiclist_encode(paginator.page(paginator.num_pages))}))
    except Exception as e:
        return HttpResponse(json_serialize(status='EXCEPTION'))

    

    
     
