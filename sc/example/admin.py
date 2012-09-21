# coding: utf-8

from django.contrib import admin
from example.models import Publisher,Product_name

class MyModelAdmin( admin.ModelAdmin ):
    pass

admin.site.register( Publisher, MyModelAdmin )
admin.site.register( Product_name, MyModelAdmin )