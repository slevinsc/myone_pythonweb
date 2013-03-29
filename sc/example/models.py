from django.db import models
import MySQLdb
import MySQLdb.cursors
def db(user,pass1):
     host = "192.168.0.25"
     user = "sc"
     passwd = "000000"
     db = "test"
     conn = MySQLdb.connect (host,user,passwd ,db,cursorclass = MySQLdb.cursors.DictCursor)
     two=conn.cursor () 
#two.execute ("insert into username(username,passwd) values('sc','000000')") 
     sql="select username,passwd from username where username=%s and passwd=%s " 
     two.execute(sql,[user,pass1])
     row=two.fetchall()
     result=row[0]
     return result


class Publisher(models.Model):
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=60)
    state_province = models.CharField(max_length=30)
    country = models.CharField(max_length=50)
    website = models.URLField()    

class Product_name(models.Model):
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=50)


#print db("sc","000000")
