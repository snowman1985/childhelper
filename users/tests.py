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

def testregister():
    username = 'shentest13'
    password = 'shentest13'
    username = http.urlsafe_base64_encode(username.encode()).decode()
    password = http.urlsafe_base64_encode(password.encode()).decode()
    babyname = 'ruyi01'
    babyheight = 1.4
    babyweight = 34
    birthday = '2013-05-05'
    babysex = 'girl'
    homeaddr = '湖南省长沙市'
    schooladdr = 'xxx'
    url = 'http://localhost:8000/user/register/'
    headers = {'content-Type': 'application/x-www-form-urlencoded'}
    #payload = {'username': username, 'password': password, 'babyname': babyname,
    #           'babyheight':babyheight, 'babyweight':babyweight, 'birthday':birthday,
    #         'babysex':babysex, 'homeaddr':homeaddr, 'schooladdr':schooladdr}
    payload = {'username': username, 'password': password, 'babyname': babyname,
               'birthday':birthday, 'homeaddr':homeaddr, 'schooladdr':schooladdr}
    r = requests.post(url, data=payload, headers = headers)
    fp = open("test.html",'w')
    fp.write(r.text)
    fp.close()
    
def testupdate():
    username = 'shentest12'
    password = 'shentest12'
    username = http.urlsafe_base64_encode(username.encode()).decode()
    password = http.urlsafe_base64_encode(password.encode()).decode()
    babyname = 'shenruyi2'
    babyheight = 1.4
    babyweight = 34
    birthday = '2012-08-08'
    babysex = 'girl'
    #homeaddr = '湖南省长沙市黄兴南路'
    homeaddr = '北京市朝阳区'
    schooladdr = '北京市万泉河路小学'
    url = 'http://localhost:8000/user/update/'
    headers = {'content-Type': 'application/x-www-form-urlencoded'}
    payload = {'username': username, 'password': password, 'babyname': babyname,
               'babyheight':babyheight, 'babyweight':babyweight, 'birthday':birthday,
               'babysex':babysex, 'homeaddr':homeaddr, 'schooladdr':schooladdr}
    r = requests.post(url, data=payload, headers = headers)
    fp = open("test.html",'w')
    fp.write(r.text)
    fp.close()
    
def testinformationcheck():
    username = 'hujun'
    password = '123'
    username = http.urlsafe_base64_encode(username.encode()).decode()
    password = http.urlsafe_base64_encode(password.encode()).decode()
    babyname = 'shenruyi'
    babyheight = 1.4
    babyweight = 34
    birthday = '2012-08-08'
    babysex = 'girl'
    homeaddr = '北京市海淀区紫金庄园'
    schooladdr = '北京市万泉河路小学'
    url = 'http://www.yangwabao.com/user/informationcheck/'
    headers = {'content-Type': 'application/x-www-form-urlencoded'}
    payload = {'username': username, 'password': password}
    r = requests.post(url, data=payload, headers = headers)
    fp = open("test.html",'w')
    fp.write(r.text)
    fp.close()
    return r.text
    
def testgetinfo():
    username = 'shentest1'
    password = 'shentest1'
    username = http.urlsafe_base64_encode(username.encode()).decode()
    password = http.urlsafe_base64_encode(password.encode()).decode()
    loginurl = 'http://localhost:8000/user/login/'
    url = 'http://localhost:8000/user/getinfo/'
    headers = {'content-Type': 'application/x-www-form-urlencoded'}
    payload = {'username': username, 'password': password}
    r = requests.post(loginurl, data=payload, headers = headers)
    print(r.text)
    cookies = r.cookies
    print(cookies)
    r = requests.post(url, data=payload, headers = headers, cookies=cookies)
    fp = open("test.html",'w')
    fp.write(r.text)
    fp.close()
    return r.text
    
print(testgetinfo())
#print(testupdate())
#print(testregister())
#print(testupdate())
#print(testinformationcheck())
#print(testregister())
