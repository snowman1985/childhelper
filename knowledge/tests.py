from django.utils import http
import requests

def testcollect():
    username = 'shentest1'
    password = 'shentest1'
    username = http.urlsafe_base64_encode(username.encode()).decode()
    password = http.urlsafe_base64_encode(password.encode()).decode()
    loginurl = 'http://localhost:8000/user/login/'
    headers = {'content-Type': 'application/x-www-form-urlencoded'}
    payload = {'username': username, 'password': password}
    r = requests.post(loginurl, data=payload, headers = headers)
    cookies = r.cookies
    url = 'http://localhost:8000/knowledge/collect/'
    headers = {'content-Type': 'application/x-www-form-urlencoded'}
    payload = {'id': 2}
    r = requests.post(url, data=payload, headers = headers, cookies = cookies)
    fp = open("test.html",'w')
    fp.write(r.text)
    fp.close()
    return r.text

def testgetcollect():
    username = 'shentest1'
    password = 'shentest1'
    username = http.urlsafe_base64_encode(username.encode()).decode()
    password = http.urlsafe_base64_encode(password.encode()).decode()
    loginurl = 'http://localhost:8000/user/login/'
    headers = {'content-Type': 'application/x-www-form-urlencoded'}
    payload = {'username': username, 'password': password}
    r = requests.post(loginurl, data=payload, headers = headers)
    cookies = r.cookies
    url = 'http://localhost:8000/knowledge/listcollect/?number=5&page=1'
    headers = {'content-Type': 'application/x-www-form-urlencoded'}
    payload = {}
    r = requests.get(url, data=payload, headers = headers, cookies = cookies)
    fp = open("test.html",'w')
    fp.write(r.text)
    fp.close()
    return r.text

def testgetknowledges():
    username = 'sg1'
    password = 'sg1'
    username = http.urlsafe_base64_encode(username.encode()).decode()
    password = http.urlsafe_base64_encode(password.encode()).decode()
    loginurl = 'http://localhost:8000/user/login/'
    headers = {'content-Type': 'application/x-www-form-urlencoded'}
    payload = {'username': username, 'password': password}
    r = requests.post(loginurl, data=payload, headers = headers)
    cookies = r.cookies
    url = 'http://localhost:8000/knowledge/list/?number=15'
    headers = {'content-Type': 'application/x-www-form-urlencoded'}
    payload = {'number': 15}
    #r = requests.get(url, data=payload, headers = headers, cookies = cookies)
    r = requests.get(url, headers = headers)
    fp = open("test.html",'w')
    fp.write(r.text)
    fp.close()
    return r.text

#print(testgetdata())
#print(testgetknowledges())
#print(testcollect())
print(testgetcollect())


