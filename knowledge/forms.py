'''
Created on 2013年12月31日

@author: shengeng
'''

from django import forms
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User 
from .models import *

class KnowledgeForm(forms.ModelForm):
#     title = models.CharField()
#     keyword = models.CharField()
#     abstract = models.TextField()
#     content = models.TextField()
#     min = models.IntegerField()
#     max = models.IntegerField()
#     url = models.CharField()
    class Meta:
        model = Knowledge


    