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

def consumption_web_view(request, oid):
    try:
        oid = int(oid)
        o = Consumption.objects.get(id = oid)
        t = get_template('consumption/consumption.html')
        c = {}
        c['consumption_consumptionid'] = o.id
        c['consumption_title'] = o.name
        c['consumption_content'] = o.description
        c['consumption_address'] = o.address
        c['consumption_url'] = o.url
        picindex = random.randint(0,9)
        c['pic'] = 'http://wjbb.cloudapp.net:8001/pic/'+str(picindex)+'.jpg'
        c['comments'] = ConsumptionComment.objects.filter(consumptionid=o)
        c['comments_size'] = len(c['comments'])
        html = t.render(Context(c))
        return HttpResponse(html)
    except ValueError:
        raise Http404()

@csrf_exempt
def addconsumptioncomment(request, consumptionid):
    consumption = Consumption.objects.get(id=int(consumptionid))
    consumptioncomment = ConsumptionComment(consumptionid=consumption, comment=request.POST['consumptioncomment'])
    consumptioncomment.save()
    return consumption_web_view(request, consumptionid)
    
class consumptionFormView(FormView):
    template_name = 'consumption/consumptionform.html'
    form_class = consumptionForm
    def get_context_data(self, **kwargs):
        context = super(consumptionFormView, self).get_context_data(**kwargs)
        return context
    
    def form_valid(self, form):
        address = form.cleaned_data['address']
        baidu_resp = get_baidu_location(address)
        if not baidu_resp['result']:
            baidu_resp = get_baidu_location('百度大厦')
            address = '百度大厦'
        longitude = baidu_resp['result']['location']['lng']
        latitude = baidu_resp['result']['location']['lat']
        point = fromstr("POINT(%s %s)" % (longitude, latitude))
        consumption = Consumption()
        consumption.name = form.cleaned_data['name']
        consumption.city = form.cleaned_data['city']
        consumption.address = form.cleaned_data['address']
        consumption.url = form.cleaned_data['url']
        consumption.description = form.cleaned_data['description']
        consumption.point = point
        consumption.begin = datetime.now()
        consumption.end = datetime.now()
        consumption.save()
        return super(consumptionFormView, self).form_valid(form)
