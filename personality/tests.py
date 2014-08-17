import requests
from django.utils import http

# Create your tests here.
def testpersondemands():
    username = 'shentest1'
    password = 'shentest1'
    username = http.urlsafe_base64_encode(username.encode()).decode()
    password = http.urlsafe_base64_encode(password.encode()).decode()
    loginurl = 'http://localhost:8000/user/login/'
    headers = {'content-Type': 'application/x-www-form-urlencoded'}
    payload = {'username': username, 'password': password}
    r = requests.post(loginurl, data=payload, headers = headers)
    cookies = r.cookies

    url = 'http://localhost:8000/personality/list_person_userdemand/'
    headers = {'content-Type': 'application/x-www-form-urlencoded'}
    payload = {'content':"测试移动端帮你找修改后"}
    r = requests.get(url, data=None, headers = None, cookies = cookies)
    fp = open("test.html",'w')
    fp.write(r.text)
    fp.close()
    return r.text

def testpersontopics():
    username = 'xzh'
    password = '111111'
    username = http.urlsafe_base64_encode(username.encode()).decode()
    password = http.urlsafe_base64_encode(password.encode()).decode()
    loginurl = 'http://localhost:8000/user/login/'
    headers = {'content-Type': 'application/x-www-form-urlencoded'}
    payload = {'username': username, 'password': password}
    r = requests.post(loginurl, data=payload, headers = headers)
    cookies = r.cookies

    url = 'http://localhost:8000/personality/list_person_topics/?page=10&number=6'
    headers = {'content-Type': 'application/x-www-form-urlencoded'}
    payload = {'content':"测试移动端帮你找修改后"}
    r = requests.get(url, data=None, headers = None, cookies = cookies)
    fp = open("test.html",'w')
    fp.write(r.text)
    fp.close()
    return r.text

def testpersoncomments():
    username = 'xzh'
    password = '111111'
    username = http.urlsafe_base64_encode(username.encode()).decode()
    password = http.urlsafe_base64_encode(password.encode()).decode()
    loginurl = 'http://localhost:8000/user/login/'
    headers = {'content-Type': 'application/x-www-form-urlencoded'}
    payload = {'username': username, 'password': password}
    r = requests.post(loginurl, data=payload, headers = headers)
    cookies = r.cookies

    url = 'http://localhost:8000/personality/list_person_comments/?page=1&number=5'
    headers = {'content-Type': 'application/x-www-form-urlencoded'}
    payload = {'content':"测试移动端帮你找修改后"}
    r = requests.get(url, data=None, headers = None, cookies = cookies)
    fp = open("test.html",'w')
    fp.write(r.text)
    fp.close()
    return r.text

print(testpersondemands())
print("=================")
print(testpersontopics())
print("=================")
print(testpersoncomments())
