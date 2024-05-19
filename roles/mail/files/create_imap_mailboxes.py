#!/usr/bin/python
#
#   Create the mailboxes for each user in the voicemail database.
#
#   ./create_mailbox.py | cyradm --user admin --server localhost
#
import sys
import os
import MySQLdb
from pprint import pprint

boxlist = [ '', 'Sent', 'Drafts', 'Old', 'Trash', 'Greetings', 'Family', 'Work' ]

if __name__ == '__main__':

    db = MySQLdb.connect('localhost', 'asterisk', 'phoneme', 'asterisk')
    rows = db.cursor()

    rows.execute('SELECT imapuser, imappassword FROM voicemail')
    numrows = rows.rowcount
    for x in xrange(0,numrows):
        row = rows.fetchone()
        username = row[0]
        password = row[1]

        for box in boxlist:
            m = 'user/' + username
            if box:
                m += '/' + box
            print 'createmailbox %s' % m
            print 'setaclmailbox %s %s all' % (m, username)
            print 'setquota %s 500000' % m # I think that's 500MB

    rows.close()
    exit(0)


