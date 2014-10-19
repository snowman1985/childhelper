import os,sys
sys.path.insert(0, os.path.join("/root","workspace","ywbserver"))
from django.core.management import *
from ywbserver import settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ywbserver.settings")
from commercial.models import *
from utils.baidumap import *
from django.contrib.gis.geos import fromstr
from django.utils.timezone import utc
import psycopg2
import datetime, time

dbaddr = settings.DATABASES['default']['HOST']
dbport = settings.DATABASES['default']['PORT']
dbname = 'wjbb_data'
dbuser = settings.DATABASES['default']['USER']
dbpassword = settings.DATABASES['default']['PASSWORD']

conn = psycopg2.connect(host=dbaddr, port=dbport, database=dbname, user=dbuser, password=dbpassword)
cur = conn.cursor()

today = datetime.date.today()
cur.execute("SELECT * from shangpin where updatetime >= \'%s\' " % today)

#cur.execute("""SELECT * from shangpin""")

rowcount = 0
for row in cur:
  rowcount += 1
  print(rowcount)
  try:
    print(row)
    name = str(row[10]).split(sep='##')[0]
    address = str(row[11]).split(sep='##')[0]
    abstract = "原价" + str(row[4]) + " / " + "现价" + str(row[5])
    description = row[3]
    url = row[0]
    addrjson = get_baidu_location(address)
    lat = addrjson['result']['location']['lat']
    lng = addrjson['result']['location']['lng']
    city = row[1]
    point = fromstr("POINT(%s %s)" % (lng, lat))
    begin = datetime.datetime.utcfromtimestamp(int(row[7])).replace(tzinfo=utc)
    end = datetime.datetime.utcfromtimestamp(int(row[8])).replace(tzinfo=utc)
    cons = Consumption(name=name,city=city,address=address,abstract=abstract,description=description,
                       url=url, begin=begin, end = end, point=point)
    cons.save()
    time.sleep(0.5)
  except Exception as e:
    print(e)
      #---------------------------------------------------------------------- pass

print("rowcount: ", rowcount)

