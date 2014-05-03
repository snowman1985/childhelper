from django.contrib.auth.models import User
from baby.models import *
from .models import *
from users.models import *

#处理微信用户订阅
def handle_subscribe(msg):
    new_openid = msg['FromUserName']
    user = User.objects.create_user(username = new_openid, password = new_openid)
    baby = Baby()
    baby.type = 2    ###标记用户来自微信
    user.baby = baby
    user.save()
    baby.save()
    new_user = WeixinUser(openid = new_openid)
    new_user.save()
    return msg

#处理微信用户取消订阅
def handle_unsubscribe(msg):
    del_openid = msg['FromUserName']
    del_user = WeixinUser.objects.get(openid = del_openid)
    if del_user:
        del_user.delete()
        print('weixin user %s unsubscribe' % del_openid)
        remove_circle(del_user.id, 2)
    user = User.objects.get(id = del_openid)
    if user:
        baby = user.baby
        if baby:
            baby.delete()
        user.delete()
    return msg





