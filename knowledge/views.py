from django.shortcuts import render
from django.http import *
from baby.models import Baby
from knowledge.models import *
from django.contrib import auth
from django.contrib.auth.models import User
from django.utils import http
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView, TemplateView, CreateView
from datetime import *
from users.utils import *
import base64, json, random, math

from django.template.loader import get_template
from django.template import Context
from .forms import *
# Create your views here.

def web_view(request, kid):
    try:
        kid = int(kid)
        k = Knowledge.objects.get(id = kid)
        content = k.content
        html = content
        adaptorstr = '''<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,minimum-scale=1" />'''
        imagestyle = '''<style type="text/css"> div img { display:none } </style>'''
        split1 = html.split('<head>')
        html = ('%s <head> %s %s %s') % (split1[0], adaptorstr, imagestyle, split1[1])

        imagestart = html.find('<img')
        if imagestart < 0:
           print("##no image")
           picindex = random.randint(0,9)
           imgstr = '''
<p style=\"text-align: center\">
  <img src=\"%s\" style=\"width: 300px; height: 241px, display:inline\"/>
</p>
''' % ('http://wjbb.cloudapp.net:8001/pic/'+str(picindex)+'.jpg')
           htmlsplit = html.split('<body>')
           html = ('%s <body> %s %s')%(htmlsplit[0], imgstr, htmlsplit[1])

        else:
            print("image")
            srcstart = html.find("src", imagestart)
            srcend = html.find("\"", srcstart + 5)
            imageurl = html[srcstart+5:srcend]
            imgstr = '''
<p style=\"text-align: center\">
  <img src=\"%s\" style=\"width: 300px; height: 241px, display:inline\"/>
</p>
''' % (imageurl)
            htmlsplit = html.split('<body>')
            html = ('%s <body> %s %s')%(htmlsplit[0], imgstr, htmlsplit[1])
        print(html)
        return HttpResponse(html)
    except ValueError:
        raise Http404()

@csrf_exempt
def collectknowl(request):
    (authed, username, password, user) = auth_user(request)
    if not authed or not user:
        return HttpResponse('AUTH_FAILED')
    knowlid = request.POST.get('id')
    if knowlid == None or knowlid =="":
        return HttpResponse('NULL_ID')
    try:
        collection_record = KnowledgeCollection.objects.get(user_id = user.id)
    except KnowledgeCollection.DoesNotExist:
        new_collection_record = KnowledgeCollection.objects.create()
        new_collection_record.user_id = user.id
        new_collection_record.collection_list = '|%s|' % knowlid
        new_collection_record.save()
        return HttpResponse('True')
    else:
        collection_list = collection_record.collection_list
        if collection_list.find('|%s|'%knowlid) < 0:
            collection_record.collection_list = '%s%s|'%(collection_list,knowlid)
            collection_record.save()
        return HttpResponse('True')


class KnowledgeFormView(CreateView):
    template_name = 'knowledge/knowledgeform.html'
    form_class = KnowledgeForm
    model = Knowledge
