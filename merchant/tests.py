from django.utils import http
import requests

def testpublishfindhelp():
    username = 'shentest1'
    password = 'shentest1'
    username = http.urlsafe_base64_encode(username.encode()).decode()
    password = http.urlsafe_base64_encode(password.encode()).decode()
    loginurl = 'http://localhost:8000/user/login/'
    headers = {'content-Type': 'application/x-www-form-urlencoded'}
    payload = {'username': username, 'password': password}
    r = requests.post(loginurl, data=payload, headers = headers)
    cookies = r.cookies

    url = 'http://localhost:8000/merchant/publish_findhelp/'
    headers = {'content-Type': 'application/x-www-form-urlencoded'}
    payload = {'content':"测试移动端帮你找"}
    r = requests.post(url, data=payload, headers = headers, cookies = cookies)
    fp = open("test.html",'w')
    fp.write(r.text)
    fp.close()
    return r.text

print(testpublishfindhelp())
# Create your tests here.
