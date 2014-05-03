from django.db import models
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point, fromstr
from django.contrib.gis.measure import D
import dbarray

# Create your models here.

class Circle(models.Model):
    user_id = models.IntegerField()
    user_source = models.IntegerField() # 1 is app user, 2 is weixinuser
    circle_info = dbarray.IntegerArrayField()
    point = models.PointField()
    objects = models.GeoManager() 

def create_circle(user_id, source, curpoint, distance=5000):
    samecircles = Circle.objects.filter(point__distance_lt=(curpoint, D(km=int(distance)/1000)))
    newcircleinfo = []
    if source == 2:
        circle_user_id = -user_id
    for circle in samecircles:
        circle.circle_info.append(user_id)
        circle.save()
        if circle.user_source == 2:
            newcircleinfo.append(-circle.user_id)
        else:
            newcircleinfo.append(circle.user_id)

    newcircle = Circle(user_id=user_id, user_source=source, circle_info=newcircleinfo, point=curpoint)
    newcircle.save()

def create_circle_from_position(user_id, source, longitude, latitude, distance=5000):
    point = fromstr("POINT(%s %s)" % (longitude, latitude))
    create_circle(user_id, source, point, distance)

def remove_circle(user_id, source):
    del_user = Circle.objects.get(user_id)
    if del_user:
        del_user.delete()

    if source == 2:
        circle_user_id = -user_id
    for circle in Circle.objects.all():
        circle.circle_info.remove(circle_user_id)
        
