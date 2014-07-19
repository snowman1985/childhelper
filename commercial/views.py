from django.shortcuts import render
from django.http import *
from django.utils import http
from django.contrib import auth
from django.contrib.auth.models import User
from datetime import *
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import get_template
from django.template import Context
from django.views.generic import  TemplateView
from .models import *
from baby.models import *
from users.utils import *
import hashlib, time, random, json
# Create your views here.


def web_view(request):
    try:
        if request.method != 'GET':
            return HttpResponse('HTTP_METHOD_ERR')
        cid = request.GET.get('id')
        if cid == None or cid =="":
            return HttpResponseNotFound("Not Found")
        cid = int(cid)
        try:
            o = Commercial.objects.using("ywbwebdb").get(id = cid)
        except Commercial.DoesNotExist:
            return HttpResponseNotFound("Not Found")
        t = get_template('commercial/commercial.html')
        c = {}
        c['commercial_commercialid'] = o.id
        c['commercial_title'] = o.title
        c['commercial_content'] = o.content
        c['commercial_address'] = o.merchant.address
        c['commercial_url'] = "www.yangwabao.com"
        picindex = random.randint(0,9)
        c['pic'] = o.photo.url
        c['comments'] = CommercialComment.objects.filter(commercialid=o)
        c['comments_size'] = len(c['comments'])
        html = t.render(Context(c))
        return HttpResponse(html)
    except ValueError:
        raise Http404()


def list_commercial(request):
    try:
        if request.method != 'GET':
            return HttpResponse('HTTP_METHOD_ERR')
        cnumber = int(request.GET.get('number'))
        if  cnumber == None:
            cnumber = 2
        else:
            cnumber = int(cnumber)
        (authed, username, password, user) = auth_user(request)
        if not authed or not user:
            commercials = getcommerciallist_anonymous(request, cnumber)
            return HttpResponse(json.dumps(commercials, ensure_ascii=False))
        else:
            try:
                baby = Baby.objects.get(user=user)
                commercials = getcommerciallist(baby, cnumber)
                return HttpResponse(json.dumps(commercials, ensure_ascii=False))
            except Baby.DoesNotExist:
                return HttpResponse('BABY_NULL')
    except Exception as e:
        print('Exception:' + str(e))
        return HttpResponse('EXCEPTION')


@csrf_exempt
def addcomment(request, commercialid):
    try:
        if request.method != 'POST':
            return HttpResponse('HTTP_METHOD_ERR')
        commercial = Commercial.objects.using("ywbwebdb").get(id=int(commercialid))
        commercialcomment = CommercialComment(commercialid=commercial, comment=request.POST['commercialcomment'])
        commercialcomment.save()
        return web_view(request)
    except Exception as e:
        print('Exception:' + str(e))
        return HttpResponse('EXCEPTION')
