import pymysql
import os

curdir = os.curdir + "/"
path = curdir + "../home/greg/Documents/django_projects/carpricing"
cos = os.defpath
db = pymysql.connect("localhost", "root")
cursor = db.cursor()
cursor.execute("SELECT VERSION()")
data = cursor.fetchone()
print("my database version is", data)
