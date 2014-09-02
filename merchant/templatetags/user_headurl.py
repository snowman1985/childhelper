from django import template
from photos.models import *

register = template.Library()

def getuserheadurl(value, headtype):
    print("$$$$yes, i'm custom filter")
    heads = Head.objects.filter(username = value)
    if len(heads) == 0:
        full_url = ''.join([settings.DOMAIN, '/media/head/default.jpg'])
    else:
        head = list(heads)[-1]
        if headtype == 'orig':
            full_url = ''.join([settings.DOMAIN, head.head_orig.url])
        elif headtype == 'thumbnail':
            full_url = ''.join([settings.DOMAIN, head.head_thumbnail.url])
    return full_url
    

register.filter("getuserheadurl", getuserheadurl) 
