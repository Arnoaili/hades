#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ldap
import sys
import re


def get_ladp_connect():
    uri = 'ldap://172.26.32.57:3268'
    who = 'CN=gcquery,CN=Users,DC=cd,DC=ta-mp,DC=com'
    cred = 'Gc123456'
    try:
        l = ldap.initialize(uri)
        l.simple_bind_s(who, cred)
    except ldap.INVALID_CREDENTIALS:
        print "Wrong ldap user or password."
        sys.exit(1)
    return l


def search(filter, attr=''):
    try:
        l = get_ladp_connect()
        #check bug for out-source login to compile black
        #base = 'DC=cd,DC=ta-mp,DC=com'
        base = 'DC=ta-mp,DC=com'
        scope = ldap.SCOPE_SUBTREE
        if attr:
            res = l.search_ext_s(base, scope, filter, [attr])
        else:
            res = l.search_ext_s(base, scope, filter)
    finally:
        l.unbind_ext_s()
    result = parse_search_result(res)
    # show_result(result)
    #add for time_out.py get the user email
    if len(result) == 1:
        return result.values()[0][0]


def search_ldap(key, attr=''):
    if re.match('.*@.*', key):
        filter = '(&(objectClass=person)(mail=%s))' % key
    else:
        filter = '(&(objectClass=person)(sAMAccountName=%s))' % key
    result = search(filter, attr)
    if result:
        return result


def parse_search_result(search_result):
    result = {}
    for n in range(len(search_result)):
        for attr in search_result[n][1].keys():
            for i in range(len(search_result[n][1][attr])):
                result[attr] = search_result[n][1][attr]
    return result


def usage():
    print "Usage: %s key [attr]" % sys.argv[0]
    sys.exit(1)


def show_result(result):
    print "Search result:"
    print "=" * 80
    for key, value in result.items():
        print "%s = %s" % (key, value)


if __name__ == '__main__':
    to_mail = search_ldap('dpwang', 'mail')
    print to_mail
    """
    key = ''
    attr = ''
    if len(sys.argv) == 2:
        key = sys.argv[1]
    elif len(sys.argv) == 3:
        key, attr = sys.argv[1:]
    else:
        usage()

    print "Key: %s\nAttr: %s\n" % (key, attr)
    search_ldap(key, attr)
    """