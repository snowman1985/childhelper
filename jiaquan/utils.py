'''
Created on 2014年5月3日

@author: shengeng
'''

from django.http import *
from baby.models import Baby
from django.contrib import auth
from django.contrib.auth.models import User
from django.utils import http
from datetime import *
import json, base64

