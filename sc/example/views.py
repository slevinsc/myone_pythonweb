# coding=utf-8
import models,sys
sys.path.append('E:\\223\\sc\\sc')
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.contrib.sessions.models import Session

from form import ContactForm

#from example.form import ContactForm
from django.http import HttpResponseRedirect  
#import Session

now=['项目1','项目2','项目3','项目4']
login="登录"
def current_datetime(request):    
    #t = get_template('static.html')
   # html = t.render(Context({'item_list': now}))
    #return HttpResponse(html)
    
        #print "%s and %s" % (request.get['select'],request.get['Submit'])
      
    return render_to_response('static.html', {'item_list': now})

def jiujie(request):
    #if request.method == 'POST':
        #if not request.POST.get('select', ''):
            #print "MB 我错了"
        #else:
   # if request.method == 'POST':
        #if not request.POST.get('select', ''):
            #print "测试 POST"
        #else:
    return render_to_response("test5.html") 
    #if 'select' in request.POST:
         #return HttpResponse(request.POST['select'])

def login(request):
   # t = get_template('login.html')
   # html = t.render(Context({'login': login}))
   # return HttpResponse(html)
     #return render_to_response('login.html')
    #return HttpResponse(t)
    
    username = request.POST.get("username",None)
    if username:
        request.session["username"] = username
    username = request.session.get("username",None)
    #date=username.get_expiry_age()
    if username:
        #return render_to_response("login.html",{"username":username})
        return HttpResponse(username)
    else:
        return render_to_response("login.html") 
def action1(request):     
     username=request.POST.get("username",None)                  
     passwd = request.POST.get("password",None)             # if not passwd:               #  return render_to_response("login.html")
     userid=request.session.get("username",None)
     if not userid:          # return render_to_response('login.html', {'username': username}) 
          try:
             rel=models.db(username, passwd)
             #if rel['username'] and rel['passwd']:
             request.session['username']=username
             sid=request.session.get("username",None)
             request.session.save()
             
             return render_to_response('login.html', {'username': username})
          except:
             return render_to_response("login.html")       
     else:
         return render_to_response('login.html',{'username': userid})
 
def action(request):
    #sid=Session.objects.get()
      
    if request.method == 'POST':
        username=request.POST.get("username",None)   
        if not username:
          return render_to_response('login.html')
         #get_id= request.session.get("username",None):
        usersid = request.session.get("username",None)
        if usersid:
             return render_to_response('login.html', {'username': username})
        else:
             #passwd=request.POST['password']
             passwd = request.POST.get("password",None) 
             if not passwd:
                 return HttpResponse("shurumima")
             try:
                 rel=models.db(username, passwd)
             #if rel['username'] and rel['passwd']:
                 request.session["username"] = username
                 return render_to_response('login.html', {'username': username})
             except:
                 return HttpResponse("用户名和密码错误")
    else:
         return render_to_response("login.html")
       
def logout(request):
    try:
       del request.session['username']
    except:
        pass
    return HttpResponseRedirect("/action1/")
     
def test(request):
    if request.session.get('test',None):
       return HttpResponse('ok')
    else:
       request.session['test']='im test'
       return HttpResponse('fail')
   
def thanks_bak(request):
    if request.method == 'POST': # If the form has been submitted...
        form = ContactForm(request.POST) # A form bound to the POST
        if form.is_valid():
            base= request.POST.get('base',None)
            if base =='leve1':
                product=request.POST.get('product',None)
                oldpass=request.POST.get('oldpass',None)
                newpass=request.POST.get('newpass',None)
                secondpass=request.POST.get('secondpass',None)
                if newpass==secondpass:
                    list=(base,product,oldpass,newpass,secondpass)
                    return render_to_response('exanoke.html', {'list': list})
            else:                
                product=request.POST.get('product',None)
                ipaddr=request.POST.get('ipaddr',None)
                oldpass=request.POST.get('oldpass',None)
                newpass=request.POST.get('newpass',None)
                secondpass=request.POST.get('secondpass',None)
                if newpass==secondpass:
                    list=(base,product,ipaddr,oldpass,newpass,secondpass)
                    return render_to_response('exanoke.html', {'list': list})
                    
                #return HttpResponse('fail')
        else:
           return HttpResponse('fail') 
    else:
            #form = ContactForm({'base':'leve1','product':'leve1','ipaddr':'34.34.34.3','oldpass':'dffd','newpass':'fds','secondpass':'fdsfs'}) # An unbound form
            form = ContactForm({'base':'leve1','product':'leve1'})
            return render_to_response('exanoke.html', {'form': form,})
        
def thanks(request):
    if request.method == 'POST': # If the form has been submitted...
        form = ContactForm(request.POST) # A form bound to the POST
        if form.is_valid():               
                ipaddr=request.POST.get('ipaddr',None)
                oldpass=request.POST.get('oldpass',None)
                newpass=request.POST.get('newpass',None)
                secondpass=request.POST.get('secondpass',None)
                if newpass==secondpass:
                    list=(ipaddr,oldpass,newpass,secondpass)
                    return render_to_response('exanoke.html', {'list': list})
                    
                #return HttpResponse('fail')
        else:
           return HttpResponse('fail') 
    else:
            #form = ContactForm({'base':'leve1','product':'leve1','ipaddr':'34.34.34.3','oldpass':'dffd','newpass':'fds','secondpass':'fdsfs'}) # An unbound form
        form = ContactForm({'base':'leve1','product':'leve1'})
        return render_to_response('exanoke.html', {'form': form,})
 
