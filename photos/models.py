from django.db import models
from imagekit.models import ImageSpecField
from pilkit.processors import ResizeToFill

# Create your models here.

class Photo(models.Model):
    name = models.TextField(max_length=100,null=True)
    head_orig = models.ImageField(upload_to='head',null=True,blank=True)
    head_thumbnail = ImageSpecField(source='head_orig',
                                      processors=[ResizeToFill(100, 100)],
                                      format='JPEG',
                                      options={'quality': 60})
