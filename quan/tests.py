"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

# from django.test import TestCase
# 
# 
# class SimpleTest(TestCase):
#     def test_basic_addition(self):
#         """
#         Tests that 1 + 1 always equals 2.
#         """
#         self.assertEqual(1 + 1, 2)

from django.utils import http
import requests

def test_post_topic():
    username = 'shentest2'
    password = 'shentest2'
    username = http.urlsafe_base64_encode(username.encode()).decode()
    password = http.urlsafe_base64_encode(password.encode()).decode()
    content = '呵呵，测试一下在圈子里发帖aaa。'
    url = 'http://localhost:8000/quan/posttopic/'
    headers = {'content-Type': 'application/x-www-form-urlencoded'}
    payload = {'username': username, 'password': password, 'content': content}
    r = requests.post(url, data=payload, headers = headers)
    fp = open("test.html",'w')
    fp.write(r.text)
    fp.close()

def test_add_comment():
    username = 'shentest1'
    password = 'shentest1'
    topicid = 6
    username = http.urlsafe_base64_encode(username.encode()).decode()
    password = http.urlsafe_base64_encode(password.encode()).decode()
    comment = '呵呵，测试一下在圈子里发个评论呗aaa。'
    url = 'http://localhost:8000/quan/addcomment/'
    headers = {'content-Type': 'application/x-www-form-urlencoded'}
    payload = {'username': username, 'password': password, 'topicid':topicid, 'comment':comment}
    r = requests.post(url, data=payload, headers = headers)
    fp = open("test.html",'w')
    fp.write(r.text)
    fp.close()

def test_get_topic():
    username = 'shentest1'
    password = 'shentest1'
    username = http.urlsafe_base64_encode(username.encode()).decode()
    password = http.urlsafe_base64_encode(password.encode()).decode()
    url = 'http://localhost:8000/quan/getcircletopic/'
    headers = {'content-Type': 'application/x-www-form-urlencoded'}
    payload = {'username': username, 'password': password}
    r = requests.post(url, data=payload, headers = headers)
    print(r.text)
    fp = open("test_gettopic.html",'w')
    fp.write(r.text)
    fp.close()
    
def test_get_topic_webview():
    username = 'shentest2'
    password = 'shentest2'
    username = http.urlsafe_base64_encode(username.encode()).decode()
    password = http.urlsafe_base64_encode(password.encode()).decode()
    url = 'http://localhost:8000/quan/gettopicwebview/14/'
    headers = {'content-Type': 'application/x-www-form-urlencoded'}
    payload = {'username': username, 'password': password}
    r = requests.get(url)
    fp = open("test_gettopic.html",'w')
    fp.write(r.text)
    fp.close()

#print(test_post_topic())
#print(test_add_comment())
print(test_get_topic())
#print(test_get_topic_webview())
