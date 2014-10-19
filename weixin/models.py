from django.db import models

# Create your models here.

class WeixinUser(models.Model):
    openid = models.CharField(max_length=100)
    baby_birthday = models.DateTimeField(null=True)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    precision = models.FloatField(null=True)
