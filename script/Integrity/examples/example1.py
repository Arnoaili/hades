#!/usr/bin/python
#-*- encoding: utf-8 -*- 
from Integrity import IntegrityClient

wsdl = 'http://172.24.63.21:7001/webservices/10/2/Integrity/?wsdl'

client = IntegrityClient(wsdl, credential_username="administrator", credential_password="password")
""
#use x['Description'][1].value to get the Description, do not use x['Description'].longtext.value, it may be shortext

print 'client.getItem'
z = client.getItem(item_id=4, fields=['Summary','Description','Belongs to Product','Project', 'Created Date', 'Modified Date', 'Product'])
print z

print 'client.getItemsByIDs'
r = client.getItemsByIDs(item_ids=[4,5,6], fields=['Description','State', 'Assigned User'])
print r

print 'client.getProjects'
projects = client.getProjects(fields=['Description', 'Name',])
print projects

print 'client.getItemsByCustomQuery'
j = client.getItemsByCustomQuery(fields=['Description'], query="(field[Type]=Project)")
print j

print 'client.getItemsByNamedQuery'
x = client.getItemsByNamedQuery(name="All Defects", fields=['Type', 'Description'])
print x

print 'client.getAttachmentDetails'
x = client.getAttachmentDetails(attachment_name="x.py", field_name="Attachments", item_id=117) 
print x

print 'client.removeAttachment'
x = client.removeAttachment(attachment_name="test2.py", field_name="Attachments", item_id="117")
print x

print 'client.editItem'
x = client.editItem(item_id=4, **{'Description':"dddd"*1000})
print x

print 'client.getProductsByName'
x = client.getProductsByName(fields=['ID', 'Summary',], name='product1')
print x

print 'client.getDefectsByProjectID'
x = client.getDefectsByProjectID(fields=['ID', 'Summary',], project_id=3)
print x

print 'client.getItemsByProject'
x = client.getItemsByProject(fields=['Description'],project = "/DemoProject")
print x

print 'client.getItemsByProjectID'
x = client.getItemsByProjectID(fields=['ID', 'Summary',], project_id=3)
print x

print 'client.getItemsByFieldValues'
x = client.getItemsByFieldValues(fields=['ID', 'Summary',], Project='/DemoProject')
print x

print 'client.getItemsByFieldValues'
x = client.getItemsByFieldValues(fields=['ID', 'Summary',], Project='/DemoProject', Type='Defect')
print x

