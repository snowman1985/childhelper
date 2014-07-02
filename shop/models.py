from django.db import models
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point, fromstr
from django.contrib.auth.models import User
from django.contrib.gis.measure import D # alias for Distance
import random

class Shop(models.Model):
    name = models.CharField(max_length=200)
    city = models.CharField(max_length=20)
    address = models.CharField(max_length=100)
    abstract = models.CharField(max_length=2000)
    description = models.CharField(max_length=5000)
    url = models.CharField(max_length=1000)
    longitude = models.FloatField(null=True)
    latitude = models.FloatField(null=True)
    point = models.PointField()
    objects = models.GeoManager()

class Merchant(models.Model):
    user = models.OneToOneField(User)
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=20)
    address = models.CharField(max_length=100)
    longitude = models.FloatField(null=True)
    latitude = models.FloatField(null=True)
    description = models.CharField(max_length=2000)
    point = models.PointField(null=True)
    objects = models.GeoManager()
    
    class Meta:
        app_label="merchant"

class Commercial(models.Model):
    merchant = models.ForeignKey(Merchant)
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=2000)
    photo = models.ImageField(upload_to='b_photos/%Y/%m/%d', max_length=10000000, blank=True, null=True, default='b_photos/default.jpg')
    
    class Meta:
        app_label="merchant"

class CommercialHistory(models.Model):
    commercial_id = models.IntegerField()
    merchant_id = models.IntegerField()
    baby_id = models.IntegerField()
   
    class Meta:
        app_label="merchant"

class EduShop(Shop):
    pass

class EntertainShop(Shop):
    pass

class ShopComment(models.Model):
    shopid = models.ForeignKey(Shop)
    comment = models.CharField(max_length=500)


def get_shop_nearby(latitude, longitude, number=1, distance = 50000):
    point = fromstr("POINT(%s %s)" % (longitude, latitude))
    nearby = Merchant.objects.using('ywbwebdb').filter(point__distance_lt=(point, D(km=int(distance)/1000)))
    count = nearby.count()
    if number >= count:
        print('shop nearby %f,%f is not enough' % (latitude, longitude))
        return list(Merchant.objects.using('ywbwebdb').all()[:number-1])
    else:
        return random.sample(list(nearby), number)

def get_shop_random(number=1):
    all = Merchant.objects.using('ywbwebdb').all()
    count = all.count()
    if number >= count:
        print('shop random  is not enough')
        return list(all[:count])
    else:
        return random.sample(list(all), number)
    
def store_commercial_history(commercialid, merchantid, babyid):
    commercialhistory = CommercialHistory(commercial_id=commercialid, merchant_id=merchantid, baby_id=babyid)
    commercialhistory.save(using="ywbwebdb") 
