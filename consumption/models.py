from django.db import models
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point, fromstr
from django.contrib.gis.measure import D # alias for Distance
from django.utils.timezone import utc
import random, datetime
from shop.models import *
# Create your models here.

class Consumption(models.Model):
    name = models.CharField(max_length=5000)
    city = models.CharField(max_length=20)
    address = models.CharField(max_length=5000)
    abstract = models.CharField(max_length=5000)
    description = models.CharField(max_length=50000)
    url = models.CharField(max_length=1000)
    begin = models.DateTimeField()
    end = models.DateTimeField()
    point = models.PointField()
    objects = models.GeoManager()

class EduConsumption(models.Model):
    pass

class EntertainConsumption(models.Model):
    pass

class ConsumptionComment(models.Model):
    consumptionid = models.ForeignKey(Consumption)
    comment = models.CharField(max_length=500)


# def get_consumption_nearby(latitude, longitude, number=1, distance = 5000):
#     point = fromstr("POINT(%s %s)" % (longitude, latitude))
#     timenow = datetime.datetime.utcnow().replace(tzinfo=utc)
#     nearby = Consumption.objects.filter(point__distance_lt=(point, D(km=int(distance)/1000)), end__gt=timenow)
#     count = nearby.count()
#     if number >= count:
#         print('consumption nearby %f,%f is not enough' % (latitude, longitude))
#         return list(Consumption.objects.all()[:number])
#     else:
#         return random.sample(list(nearby), number)
#     
# def get_consumption_city(city, number=1, distance = 5000):
#     citystr = city.replace('市', '')
#     timenow = datetime.datetime.utcnow().replace(tzinfo=utc)
#     samecity = Consumption.objects.filter(city__exact=citystr)
#     count = samecity.count()
#     if number >= count:
#         print('consumption in city %s is not enough' % (citystr))
#         return list(Consumption.objects.all()[:number])
#     else:
#         return random.sample(list(samecity), number)
# 
# def get_consumption_random(number=1):
#     all = Consumption.objects.all()
#     count = all.count()
#     if number >= count:
#         print('consumption random  is not enough')
#         return list(all[:count])
#     else:
#         return random.sample(list(all), number)


def get_commercial_nearby(homepoint, number=1, distance = 5000):
    point = homepoint
    nearbym = Merchant.objects.using('ywbwebdb').filter(point__distance_lt=(point, D(km=int(distance)/1000)))
    count = nearbym.count()
    if number >= count:
        print('Merchant nearby is not enough' )
        merchants = Merchant.objects.using('ywbwebdb').all()[:number-1]
        commercials = []
        for merchant in merchants:
            commercial_set = Commercial.objects.using('ywbwebdb').filter(merchant = merchant)
            if len(commercial_set) >= 1:
                commercials.append(commercial_set[0])
        return commercials
    else:
        merchants = Merchant.objects.using('ywbwebdb').all()[:number-1]
        merchants = random.sample(list(merchants), number)
        commercials = []
        for merchant in merchants:
            commercial_set = Commercial.objects.using('ywbwebdb').filter(merchant = merchant)
            if len(commercial_set) >= 1:
                commercials.append(commercial_set[0])
        return commercials

def get_commercial_random(number=1):
    all = Commercial.objects.using('ywbwebdb').all()
    count = all.count()
    if number >= count:
        print('commercial random  is not enough')
        return list(all[:count])
    else:
        return random.sample(list(all), number)
    
    
    
