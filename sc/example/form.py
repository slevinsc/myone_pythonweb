# coding=utf-8
from django import forms
TOPIC_CHOICES=(('leve1','动漫'),('leve2','红段子'),('leve3','动感社区'),('leve4','老乡网'),('leve5','关爱100'))
basename=(('leve1','基于项目'),('leve2','基于IP'))
class ContactForm(forms.Form):
       #base=forms.ChoiceField(widget=forms.RadioSelect(),choices=basename,label='')
      # product=forms.ChoiceField(choices=TOPIC_CHOICES,label='项目名称') 
       ipaddr=forms.IPAddressField(label='IP地址',required=False)
       oldpass=forms.CharField(widget=forms.PasswordInput(),label='旧密码',required=False)
       newpass=forms.CharField(widget=forms.PasswordInput(),label='新密码',required=False)
       secondpass=forms.CharField(widget=forms.PasswordInput(),label='确认密码',required=False)