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
    username = 'shentest1'
    password = 'shentest1'
    username = http.urlsafe_base64_encode(username.encode()).decode()
    password = http.urlsafe_base64_encode(password.encode()).decode()
    content = '我说，爱丫丫'
    url = 'http://localhost:8000/quan/posttopic/'
    headers = {'content-Type': 'application/x-www-form-urlencoded'}
    payload = {'username': username, 'password': password, 'content': content}
    r = requests.post(url, data=payload, headers = headers)
    fp = open("test.html",'w')
    fp.write(r.text)
    fp.close()
    

print(test_post_topic())

