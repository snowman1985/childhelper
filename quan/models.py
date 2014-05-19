from django.db import models
from django.contrib.auth.models import User
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point, fromstr
from django.contrib.gis.measure import D
import dbarray
import datetime
from django.utils.timezone import utc
# Create your models here.

class Circle(models.Model):
    #user_id = models.IntegerField()
    user_source = models.IntegerField() # 1 is app user, 2 is weixinuser
    circle_users = dbarray.IntegerArrayField()
    point = models.PointField()
    objects = models.GeoManager()
    user = models.OneToOneField(User)
    topic_ids = dbarray.IntegerArrayField()
    last_access = models.DateTimeField(default=datetime.datetime.utcnow().replace(tzinfo=utc)) # recorde the last-access datatime
    not_deleted = models.BooleanField() # mark if this circle should be computed
    
    def add_topic(self, topic):
        self.topic_ids.append(topic.id)
        for notice_user_id in self.circle_users:
            notice_user = User.objects.get(id = notice_user_id)
            if not notice_user.circle.not_deleted:
                continue
            notice_user.circle.topic_ids.append(topic.id)
            notice_user.circle.save()
        self.save()
            
    def get_topics(self):
        return None


def create_circle(user, source, curpoint, distance=5000):
    samecircles = Circle.objects.filter(point__distance_lt=(curpoint, D(km=int(distance)/1000)))
    newcircleinfo = []
    for circle in samecircles:
        circle.circle_users.append(user.id)
        circle.save()
        newcircleinfo.append(circle.user.id)
    newcircle = Circle(user=user, user_source=source, circle_users=newcircleinfo, point=curpoint, not_deleted = True, topic_ids = [])
    newcircle.save()

def create_circle_from_position(user, source, longitude, latitude, distance=5000):
    point = fromstr("POINT(%s %s)" % (longitude, latitude))
    create_circle(user, source, point, distance)

def remove_circle(user, source):
    del_circle = Circle.objects.get(user = user)
    if del_circle:
        del_circle.not_deleted = False
        for circle in Circle.objects.all():
            circle.circle_users.remove(del_circle.user.id)
        

class Topic(models.Model):
    from_user = models.ForeignKey(User)
    content = models.TextField()
    comments = dbarray.IntegerArrayField(null=True)
    create_time = models.DateTimeField(default=datetime.datetime.utcnow().replace(tzinfo=utc))
    update_time = models.DateTimeField(default=datetime.datetime.utcnow().replace(tzinfo=utc))


class Comment(models.Model):
    from_user = models.ForeignKey(User)
    content = models.TextField()
    topic = models.ForeignKey(Topic)
    create_time = models.DateTimeField(default=datetime.datetime.utcnow().replace(tzinfo=utc))
    
    
    
    
