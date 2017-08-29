#!/usr/bin/python
#-*- encoding: utf-8 -*- 
import re
from suds.client import Client
from suds import client
from suds.plugin import MessagePlugin

url = 'http://172.24.63.21:7001/webservices/10/2/Integrity/?wsdl'

class ItemIDNS(MessagePlugin):
    def marshalled(self, context):
        body = context.envelope.getChild('Body')
        if "arg0" in body[0][0].name:
            for i in body[0][0].attributes:
                i.prefix = "ns2"
            #body[0][0].attributes[1].prefix="ns2"
    

client = Client(url, plugins=[ItemIDNS(),])


#arg0 = client.factory.create('ns5:GetItemType')


arg0 = client.factory.create('ns5:EditItemType')
#arg0 = client.factory.create('ns5:CustomQuery')
arg0.Username = "administrator"
arg0.Password = "password"
arg0._ItemId = 117
#del arg0.DateFormat
#del arg0.ImpersonatedUser
arg1 = client.factory.create('ns5:ItemFieldBase')
arg2 = client.factory.create('ns5:NullableString')
arg2.value = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaabbbbbbbbbbbbbbbbbbbbbbbbbbbbb"
arg1._Name = 'description'
arg1.shorttext = arg2
arg0.ItemField = [arg1,]
x = client.service.editItem(arg0)

