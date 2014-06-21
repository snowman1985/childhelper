import os,sys
sys.path.insert(0, os.path.join("/root","workspace","ywbserver"))
from django.core.management import *
from ywbserver import settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ywbserver.settings")

from django.test import TestCase
from django.utils import http
import requests

def testuploadhead():
    username = 'shentest04'
    password = 'shentest04'
    username = http.urlsafe_base64_encode(username.encode()).decode()
    password = http.urlsafe_base64_encode(password.encode()).decode()
    head = open('head.jpg', 'rb')
    files = {'head' : head}
    url = 'http://localhost:8000/photos/uploadhead/'
    headers = {'content-Type': 'application/octet-stream'}
    #===========================================================================
    # payload = {'username': username, 'password': password, 'babyname': babyname,
    #            'babyheight':babyheight, 'babyweight':babyweight, 'birthday':birthday,
    #            'babysex':babysex, 'homeaddr':homeaddr, 'schooladdr':schooladdr}
    #===========================================================================
    payload = {'username': username, 'password': password}
    r = requests.post(url, data = payload, files = files)
    fp = open("test.html",'w')
    fp.write(r.text)
    fp.close()
    
def testgethead():
    username = 'shentest04'
    password = 'shentest04'
    username = http.urlsafe_base64_encode(username.encode()).decode()
    password = http.urlsafe_base64_encode(password.encode()).decode()
    url = 'http://localhost:8000/photos/gethead/'
    payload = {'username': username, 'password': password}
    r = requests.post(url, data = payload)
    fp = open("test.html",'w')
    fp.write(r.text)
    fp.close()
    
#testuploadhead()
testgethead()
