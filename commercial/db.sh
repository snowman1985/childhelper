#!/bin/bash
export PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin
source /etc/profile
today=`date +%Y%m%d`
python3 /home/shengeng/workspace/ywbserver/utils/import_cons_db.py > /var/log/ywblog/consdb_${today}.log
