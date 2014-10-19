import sys, json
import requests

def get_baidu_address(latitude, longitude, detail = True):
    ak = 'GLbmnUGjCe4B62dqW6l695fL'
    url = 'http://api.map.baidu.com/geocoder/v2/?ak=%s&callback=renderReverse&location=%s,%s&output=json&pois=1'%(ak, latitude, longitude)
    resp = requests.get(url)
    content = resp.text
    addr = json.loads((content[29:-1]))
    if detail:
        return addr['result']['formatted_address']
    else:
        return addr['result']['addressComponent']['city']

def get_baidu_city(latitude, longitude, detail = True):
    ak = 'GLbmnUGjCe4B62dqW6l695fL'
    url = 'http://api.map.baidu.com/geocoder/v2/?ak=%s&callback=renderReverse&location=%s,%s&output=json&pois=1'%(ak, latitude, longitude)
    resp = requests.get(url)
    content = resp.text
    addr = json.loads((content[29:-1]))
    return addr['result']['addressComponent']['city']


def get_baidu_location(address):
    ak = 'GLbmnUGjCe4B62dqW6l695fL'
    url = 'http://api.map.baidu.com/geocoder/v2/?ak=%s&callback=showLocation&address=%s&output=json'%(ak, address)
    resp = requests.get(url)
    content = resp.text
    response = json.loads((content[27:-1]))
    return response

def convert_baidu_location(latitude, longitude):
    ak = 'GLbmnUGjCe4B62dqW6l695fL'
    url = 'http://api.map.baidu.com/geoconv/v1/?coords=%s,%s&from=1&to=5&ak=%s&output=json'%(longitude, latitude, ak)
    resp = requests.get(url)
    content = resp.text
    response = json.loads((content))#[27:-1]))
    return response['result'][0]['y'], response['result'][0]['x']

#print(sys.getdefaultencoding())
#print(get_baidu_location('xxx')['result'])

#print(get_baidu_city('39.971353229973','116.30799772131'))
#

