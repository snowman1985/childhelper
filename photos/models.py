from django.db import models
from imagekit.models import ImageSpecField
from pilkit.processors import ResizeToFill
from ywbserver import settings

# Create your models here.

class Photo(models.Model):
    name = models.TextField(max_length=100,null=True)
    head_orig = models.ImageField(upload_to='head',null=True,blank=True)
    head_thumbnail = ImageSpecField(source='head_orig',
                                      processors=[ResizeToFill(100, 100)],
                                      format='JPEG',
                                      options={'quality': 60})

class Head(models.Model):
    username = models.TextField(max_length=100,null=True)
    head_orig = models.ImageField(upload_to='head',null=True,blank=True)
    head_thumbnail = ImageSpecField(source='head_orig',
                                      processors=[ResizeToFill(100, 100)],
                                      format='JPEG',
                                      options={'quality': 60})




def getheadurl(user):
    if not user:
        full_url = ''.join([settings.DOMAIN, '/media/head/default.jpg'])
    heads = Head.objects.filter(username = user.username)
    if len(heads) == 0:
        full_url = ''.join([settings.DOMAIN, '/media/head/default.jpg'])
    else:
        head = list(heads)[-1]
        full_url = ''.join([settings.DOMAIN, head.head_thumbnail.url])
    return full_url


