from django.utils import http
import requests

def testcollect():
    username = 'shentest1'
    password = 'shentest1'
    username = http.urlsafe_base64_encode(username.encode()).decode()
    password = http.urlsafe_base64_encode(password.encode()).decode()
    url = 'http://localhost:8000/knowledge/collectknowl/'
    headers = {'content-Type': 'application/x-www-form-urlencoded'}
    payload = {'username': username, 'password': password, 'id': 1}
    r = requests.post(url, data=payload, headers = headers)
    fp = open("test.html",'w')
    fp.write(r.text)
    fp.close()
    return r.text


#print(testgetdata())
#print(testgetknowledges())
#print(testgetshops())
print(testcollect())


