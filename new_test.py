import datetime
import time
import os
import sqlite3
data=2341324123

chrome = datetime.timedelta( seconds=13124512726369742/1000000- 11644473600)
cookie= datetime.datetime(1970,1,1)+chrome

cookie2=datetime.datetime(1970,1,1)+datetime.timedelta(seconds=1511256185)
#cookie=chrome+datetime.datetime(1970,1,1)

print(cookie2)

print('chrome:',chrome)
print('cookie:',cookie)
delta=datetime.datetime(1970,1,1)-datetime.datetime( 1601, 1, 1 )

print(delta)
print(datetime.datetime(1601,1,1)+datetime.timedelta(seconds=11644473600))