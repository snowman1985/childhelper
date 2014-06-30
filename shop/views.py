from django.shortcuts import render
from django.http import *
from django.utils import http
from datetime import *
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import get_template
from django.template import Context
from django.views.generic import FormView, TemplateView
from django.contrib.gis.geos import Point, fromstr
from django.contrib.gis.measure import D # alias for Distance
from django.utils.safestring import SafeString

from .models import *
from .forms import *
from weixin.baidumap import *
import hashlib, time, random
# Create your views here.

def web_view(request, oid):
    try:
        oid = int(oid)
        o = Merchant.objects.using('ywbwebdb').get(id = oid)
        t = get_template('shop/shop.html')
        c = {}
        c['shop_shopid'] = o.id
        c['shop_title'] = o.name
        c['shop_content'] = o.description
        c['shop_address'] = o.address
        c['shop_url'] = 'http://sj.yangwabao.com'
        picindex = random.randint(0,9)
        c['pic'] = 'http://wjbb.cloudapp.net:8001/pic/'+str(picindex)+'.jpg'
        #c['comments'] = ShopComment.objects.filter(shopid=o)
        c['comments'] = {}
        html = t.render(Context(c))
        return HttpResponse(html)
    except ValueError:
        raise Http404()

@csrf_exempt
def addshopcomment(request, shopid):
    shop = Shop.objects.get(id=int(shopid))
    shopcomment = ShopComment(shopid=shop, comment=request.POST['shopcomment'])
    shopcomment.save()
    return web_view(request, shopid)
    
class ShopFormView(FormView):
    template_name = 'shop/shopform.html'
    form_class = ShopForm
    def get_context_data(self, **kwargs):
        context = super(ShopFormView, self).get_context_data(**kwargs)
        return context
    
    def form_valid(self, form):
        address = form.cleaned_data['address']
        baidu_resp = get_baidu_location(address)
        if not baidu_resp['result']:
            baidu_resp = get_baidu_location('百度大厦')
            address = '百度大厦幼儿园'
        longitude = baidu_resp['result']['location']['lng']
        latitude = baidu_resp['result']['location']['lat']
        point = fromstr("POINT(%s %s)" % (longitude, latitude))
        shop = Shop()
        shop.name = form.cleaned_data['name']
        shop.city = form.cleaned_data['city']
        shop.address = form.cleaned_data['address']
        shop.url = form.cleaned_data['url']
        shop.description = form.cleaned_data['description']
        shop.longitude = longitude
        shop.latitude = latitude
        shop.point = point
        shop.save()
        return super(ShopFormView, self).form_valid(form)
