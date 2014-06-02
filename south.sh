python manage.py syncdb  #syncdb已经被South更改，用来创建south_migrationhistory表   
  
python manage.py convert_to_south youappname #在youappname目录下面创建migrations目录以及第一次迁移需


#python manage.py schemamigration youappname --auto     #检测对models的更改   
  
#python manage.py migrate youappnam  #将更改反应到数据库
