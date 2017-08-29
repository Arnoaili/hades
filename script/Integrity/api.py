import os
import sys
import suds
from suds.client import Client
from suds.plugin import MessagePlugin
from .Integrity import *

def print_error(*msg):
    RED="\033[0;31m"
    RESET = "\033[m"
    print >> sys.stderr, ''.join([RED]+list(msg)+[RESET])


class MKSException(Exception):
    pass


class _ItemId_NS_Plugin(MessagePlugin):
    # try to add namespace prefix before ItemId
    def marshalled(self, context):
        body = context.envelope.getChild('Body')
        if "arg0" in body[0][0].name:
            for i in body[0][0].attributes:
                if i.name == 'ItemId':
                    # just set it the same as the first child's prefix
                    i.prefix = body[0][0].children[0].prefix


def fields_valid(func):
    def decorated(*args, **kwargs):
        for field in kwargs['fields']:
            flag = False
            for FIELD in ITEM_FIELDS:
                if field.lower() == FIELD.lower():
                    flag = True
            if not flag:
                raise MKSException('field "%s" not in ALM'%field)
        return func(*args, **kwargs)
    return decorated


def filter_self(locals={}):
    d = locals.copy()
    d.pop('self')
    return d


class IntegrityClientBase:

    def __init__(self, wsdl, credential_username,
                 credential_password, **kwargs):
        if 'plugins' in kwargs.keys():
            kwargs['plugins'].append(_ItemId_NS_Plugin())
        else:
            kwargs['plugins'] = [_ItemId_NS_Plugin()]
        self._credential_username = credential_username
        self._credential_password = credential_password
        self._suds_client = Client(wsdl, **kwargs)

    def _param_with_ns(self, arg_type):
        sd = self._suds_client.sd
        types = sd[0].types
        for t in types:
            if (arg_type == sd[0].xlate(t[0]) or
                    arg_type == sd[0].xlate(t[0]).split(':')[1]):
                return sd[0].xlate(t[0])

    def _get_general_arg0(self, arg_type, **kwargs):
        "generate the arg0 here, reduce codes"
        factory_stuff = self._param_with_ns(arg_type)
        arg0 = self._suds_client.factory.create(factory_stuff)
        arg0._transactionId = kwargs.get('transaction_id', None)
        arg0.Username = self._credential_username
        arg0.Password = self._credential_password
        arg0.ImpersonatedUser = kwargs.get('impersonated_user', None)
        arg0.DateFormat = kwargs.get('date_format', None)
        arg0.DateTimeFormat = kwargs.get('datetime_format', None)
        if arg_type == 'ProjectRequest':
            arg0.FieldList = kwargs.get('fields', None)
        elif arg_type == 'CustomQuery':
            arg0.InputField = kwargs.get('fields', None)
            arg0.QueryDefinition = kwargs.get('query', None)
        elif arg_type == 'NamedQuery':
            arg0.InputField = kwargs.get('fields', None)
            arg0.QueryName = kwargs.get('name', None)
        elif arg_type == 'AttachmentRequest':
            arg0._AttachmentName = kwargs.get('attachment_name', None)
            arg0._FieldName = kwargs.get('field_name', None)
            arg0._ItemId = kwargs.get('item_id', None)
        elif arg_type == 'EditItemType':
            arg0._ItemId = kwargs.get('item_id', None)
        elif arg_type == 'GetItemsByIDsType':
            arg0.InputField = kwargs.get('fields', None)
            arg0.ItemId = kwargs.get('item_ids', None)
            arg0._Name = kwargs.get('name', None)
        return arg0

    def _build_items(self, resp_items):
        ret = []
        for item in resp_items:
            ret.append(self._build_item(item))
        return ret

    def _build_item(self, resp):
        iitem = IntegrityItem()
        iitem.id = resp._ItemId
        # itemfield
        for fields in resp:
            if fields[0] == 'ItemField':
                for ItemFieldResponse in resp.ItemField:
                    # _Name's type suds.sax.text.Text
                    #if ItemFieldResponse._Name == 'Branch':
                    iitem[ItemFieldResponse._Name] = ItemFieldResponse
            # fields[0] is a name, fields[1] is value,
            # it's a (fields[0], fields[1])
            if fields[0] == 'RelatedItem':
            # just to handle the Branch, the branch field is a
            # RelatedItem, i dunno whether there's any another
            # filed need to be handled like this
                for RelatedItem in resp.RelatedItem:
                    iitem[RelatedItem._FieldName] = RelatedItem
                    if RelatedItem._FieldName == 'Branch':
                        branch_id = RelatedItem.IBPL[0]
                        branch_fields = ['State', 'Project', 'Name']
                        branch = self.getItem(item_id=branch_id,
                                              fields=branch_fields)
                        iitem['Branch'] = branch

        #JUST deal with the cls defined in Integrity.py
        if iitem['Type'].type.replace(' ', '') in globals():
            cls = globals()[iitem['Type'].type.replace(' ', '')]
        else:
            print_error('"%s" not found in driver, add it yourself :)' % iitem['Type'].type)
            return None
        # just to make sure it is a class in this namespace
        if cls.type == iitem['Type'].type:
            return cls(iitem)
        else:
            raise MKSException('%s !=  %s' % (cls.type, iitem['Type'].type))

    def _build_project(self, project_fields):
        iitem = IntegrityItem()
        for field in project_fields.Field:
            iitem[field._Name] = field._Value
        return Project(iitem)

    def editItem(self, transaction_id=None,
                 item_id=None, impersonated_user=None,
                 date_format=None, datetime_format=None, **options):
        _locals = filter_self(locals())
        arg0 = self._get_general_arg0('EditItemType', **_locals)
        ItemField = []
        for key in options.keys():
            factory_stuff = self._param_with_ns('ItemFieldBase')
            arg1 = self._suds_client.factory.create(factory_stuff)
            arg1._Name = key
            factory_stuff = self._param_with_ns('NullableString')
            arg2 = self._suds_client.factory.create(factory_stuff)
            arg2.value = options[key]
            arg1.shorttext = arg2
            ItemField.append(arg1)

        arg0.ItemField = ItemField[:]
        try:
            resp = self._suds_client.service.editItem(arg0)
            return True if resp['return'] == 'success' else False
        except suds.WebFault, e:
            print_error(e.fault['detail']['MKSException'].value)
            return False

    @fields_valid
    def getItem(self, transaction_id=None,
                item_id=None, impersonated_user=None,
                date_format=None, datetime_format=None, fields=[]):
        fields = list(fields)
        fields.append('Branch')
        fields.append('singleBranch')
        query = "(field[ID]=%s)" % str(item_id)
        ret = self.getItemsByCustomQuery(transaction_id,
                                         impersonated_user,
                                         date_format,
                                         datetime_format,
                                         fields,
                                         query)
        return ret[0] if ret else None

    @fields_valid
    def getItemsByIDs(self, transaction_id=None, name=None,
                      item_ids=[], impersonated_user=None,
                      date_format=None, datetime_format=None,
                      fields=[]):
        '''
            I don't know what the name is used for,
            just use it if you know else don't touch it
        '''
        if not item_ids:
            return []
        fields = list(fields)
        fields.append('Branch')
        fields.append('singleBranch')
        if 'Type' not in fields:
            fields.append('Type')
        _locals = filter_self(locals())
        arg0 = self._get_general_arg0('GetItemsByIDsType', **_locals)
        try:
            resp = self._suds_client.service.getItemsByIDs(arg0)
        except suds.WebFault, e:
            print_error(e.fault['detail']['MKSException'].value)
            print_error("I am going to try getItem for each id")
            ret = []
            for id in item_ids:
                item = self.getItem(transaction_id=transaction_id,
                                    item_id=id,
                                    impersonated_user=impersonated_user,
                                    date_format=date_format,
                                    datetime_format=datetime_format,
                                    fields=fields)
                if item:
                    ret.append(item)
            return ret
        return self._build_items(resp.Item) if resp else []

    def getProjects(self, transaction_id=None,
                    impersonated_user=None,
                    date_format=None, datetime_format=None,
                    fields=[]):
        fields = list(fields)
        if 'Name' not in fields:   # the Name field is needed by service
            fields.append('Name')
        if 'id' not in fields:
            fields.append('id')
        _locals = filter_self(locals())
        arg0 = self._get_general_arg0('ProjectRequest', **_locals)
        resp = self._suds_client.service.getProjects(arg0)
        ret = []
        if resp[0] == 'success':
            for project in resp[1]:
                ret.append(self._build_project(project.Fields))
        else:
            raise MKSException("Get projects Error")
        return ret

    def getItemsByCustomQuery(self, transaction_id=None,
                              impersonated_user=None, date_format=None,
                              datetime_format=None, fields=[], query=None):
        fields = list(fields)
        fields.append('Branch')
        fields.append('singleBranch')
        if 'Type' not in fields:
            fields.append('Type')
        _locals = filter_self(locals())
        arg0 = self._get_general_arg0('CustomQuery', **_locals)
        try:
            resp = self._suds_client.service.getItemsByCustomQuery(arg0)
        except suds.WebFault, e:
            print_error(e.fault.faultstring, e.fault['detail']['MKSException'].value)
            return []
        return self._build_items(resp.Item) if resp else []

    @fields_valid
    def getItemsByNamedQuery(self, transaction_id=None,
                             impersonated_user=None, date_format=None,
                             datetime_format=None, name="", fields=[]):
        fields = list(fields)
        fields.append('Branch')
        fields.append('singleBranch')
        if 'Type' not in fields:
            fields.append('Type')
        _locals = filter_self(locals())
        arg0 = self._get_general_arg0('NamedQuery', **_locals)
        resp = self._suds_client.service.getItemsByNamedQuery(arg0)
        return self._build_items(resp.Item) if resp else []

    def getAttachmentDetails(self, transaction_id=None,
                             impersonated_user=None, date_format=None,
                             datetime_format=None, attachment_name="",
                             field_name="Attachments", item_id=""):
        _locals = filter_self(locals())
        arg0 = self._get_general_arg0('AttachmentRequest', **_locals)
        try:
            resp = self._suds_client.service.getAttachmentDetails(arg0)
            return resp
        except suds.WebFault, e:
            print_error(e.fault['detail']['MKSException'].value)
            return None

    def removeAttachment(self, transaction_id=None,
                         impersonated_user=None, date_format=None,
                         datetime_format=None, attachment_name="",
                         field_name="Attachments", item_id=""):
        _locals = filter_self(locals())
        arg0 = self._get_general_arg0('AttachmentRequest', **_locals)
        try:
            return self._suds_client.service.removeAttachment(arg0)
        except suds.WebFault, e:
            print_error(e.fault['detail']['MKSException'].value)
            return self.getAttachmentDetails(transaction_id,
                                             impersonated_user,
                                             date_format,
                                             datetime_format,
                                             attachment_name,
                                             field_name,
                                             item_id)

class IntegrityClient(IntegrityClientBase):

    def getProductsByName(self, transaction_id=None,
                          impersonated_user=None, date_format=None,
                          datetime_format=None, fields=[], name=""):
        # the Name in getProductsByName is summary of the product!!!
        # NOTE: products could have same summary
        fmt = '((field[Type]=Product) and (field[Summary] contains %s))'
        query = fmt % name
        return self.getItemsByCustomQuery(transaction_id,
                                          impersonated_user,
                                          date_format,
                                          datetime_format,
                                          fields,
                                          query)

    def getProjectsByProductID(self, transaction_id=None,
                               impersonated_user=None,
                               date_format=None, datetime_format=None,
                               fields=[], product_id=""):
        query = '((field[ID]= %s))' % (str(product_id))
        product = self.getItemsByCustomQuery(transaction_id,
                                             impersonated_user,
                                             date_format,
                                             datetime_format,
                                             fields=['ID'],
                                             query=query)[0]

        query = '((field[Product]= %s))' % (str(product.id))
        projects = self.getItemsByCustomQuery(transaction_id,
                                              impersonated_user,
                                              date_format,
                                              datetime_format,
                                              fields,
                                              query=query)
        return projects

    def getDefectsByProjectID(self, transaction_id=None,
                              impersonated_user=None,
                              date_format=None, datetime_format=None,
                              fields=[], project_id=""):
        query = '((field[ID]=%s))' % (str(project_id))
        project = self.getItemsByCustomQuery(transaction_id,
                                             impersonated_user,
                                             date_format,
                                             datetime_format,
                                             fields=['Project'],
                                             query=query)[0]
        fmt = '((field[Type]=Defect) and (field[Project]= %s))'
        query = fmt % (str(project.project))
        defects = self.getItemsByCustomQuery(transaction_id,
                                             impersonated_user,
                                             date_format,
                                             datetime_format,
                                             fields=fields,
                                             query=query)
        return defects

    def getItemsByProjectID(self, transaction_id=None,
                            impersonated_user=None,
                            date_format=None, datetime_format=None,
                            fields=[], project_id=""):
        query = '((field[ID]=%s))' % (str(project_id))
        project = self.getItemsByCustomQuery(transaction_id,
                                             impersonated_user,
                                             date_format,
                                             datetime_format,
                                             fields=['Project'],
                                             query=query)[0]

        query = '(field[Project]= %s)' % (str(project.project))
        items = self.getItemsByCustomQuery(transaction_id,
                                           impersonated_user,
                                           date_format,
                                           datetime_format,
                                           fields,
                                           query)
        return items

    def getItemsByProject(self, transaction_id=None,
                          impersonated_user=None,
                          date_format=None, datetime_format=None,
                          fields=[], project=""):
        query = '(field[Project]= "%s")' % (project)
        items = self.getItemsByCustomQuery(transaction_id,
                                           impersonated_user,
                                           date_format,
                                           datetime_format,
                                           fields,
                                           query)
        return items

    def getItemsByFieldValues(self, transaction_id=None,
                              impersonated_user=None,
                              date_format=None, datetime_format=None,
                              fields=[], **options):
        '''
        it is like getItemsByCustomedQuery(AND logic). but could only deal
        with '=' with field,
        it could not handle >, <, between, contains ... but just simple
        Field.
        eg: Project='/testProject', ID='117',
        Type='General System Requirement Document'...
        It does not mangle the keys, so the key in options must be in the
        ITEM_FIELDS,
        WATCH OUT:distinguish capital and small letter.
        '''
        and_q = 'and'.join(['(field[%s]="%s")' % \
                           (key, str(options[key])) for key in options])
        query = '(' + and_q + ')'
        items = self.getItemsByCustomQuery(transaction_id,
                                           impersonated_user,
                                           date_format,
                                           datetime_format,
                                           fields,
                                           query)
        return items

    def createReleaseNote(self, transaction_id=None,
                          impersonated_user=None,
                          date_format=None,
                          datetime_format=None,
                          State='',
                          Project='',
                          Branch='',
                          Version='',
                          RelateDefects=[]):
        singleBranch = Branch
        _locals = filter_self(locals())
        _locals['RN Relate Defect']=','.join(str(id) for id in RelateDefects)
        arg0 = self._get_general_arg0('CreateItemType', **_locals)
        ItemField = []
        # State, Project, Branch, Version
        for key in ('State', 'Project', 'singleBranch', 'Version', 'RN Relate Defect'):
            factory_stuff = self._param_with_ns('ItemFieldBase')
            arg1 = self._suds_client.factory.create(factory_stuff)
            arg1._Name = key
            factory_stuff = self._param_with_ns('NullableString')
            arg2 = self._suds_client.factory.create(factory_stuff)
            arg2.value = _locals[key]
            if key == 'RN Relate Defect':
                arg1.relationship = arg2
            else:
                arg1.shorttext = arg2

            ItemField.append(arg1)

        arg0.ItemField = ItemField
        arg0._Type = 'Release Note'
        try:
            resp = self._suds_client.service.createItem(arg0)
            if getattr(resp, 'return') == 'success':
                return getattr(resp, '_ItemId', False)
            return False
        except suds.WebFault, e:
            print_error(e.fault['detail']['MKSException'].value)
            # the return key sucks ! just to keep it the same
            # as the success
            return False
