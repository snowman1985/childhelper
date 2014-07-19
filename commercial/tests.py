from django.utils import http
import requests
# Create your tests here.

def testgetcommerciallist():
    username = 'shentest11'
    password = 'shentest1'
    username = http.urlsafe_base64_encode(username.encode()).decode()
    password = http.urlsafe_base64_encode(password.encode()).decode()
    loginurl = 'http://localhost:8000/user/login/'
    headers = {'content-Type': 'application/x-www-form-urlencoded'}
    payload = {'username': username, 'password': password}
    r = requests.post(loginurl, data=payload, headers = headers)
    cookies = r.cookies
    url = 'http://localhost:8000/appcommercial/list/?number=1'
    headers = {'content-Type': 'application/x-www-form-urlencoded'}
    payload = {'number': 5}
    r = requests.get(url, data=payload, headers = headers, cookies = cookies)
    fp = open("test.html",'w')
    fp.write(r.text)
    fp.close()
    return r.text


print(testgetcommerciallist())


