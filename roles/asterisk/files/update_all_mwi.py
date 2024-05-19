#!/usr/bin/python
#
#   LEDSON
#   Count messages in every existing INBOX
#   and send MWI updates to turn on or off every MWI light
#
import sys,os,time
import logging
import logging.handlers
import shutil
import re

mb_context = 'default'
mailboxdir = os.path.join('/var/spool/asterisk/voicemail', mb_context)
outgoingdir = '/var/spool/asterisk/outgoing'

sip = """Channel:%s
CallerID: %s<%s>
MaxRetries: 0
Extension: %s
WaitTime: 4
Priority: 1
"""
re_remove_context = re.compile(r'(\d+)@\w+')

logger = logging.getLogger(__name__)

# Not sure how to make syslog work yet.
#ch = logging.handlers.SysLogHandler()
#ch.setLevel(logging.DEBUG)
#logger.addHandler(ch)
logging.basicConfig(filename='/tmp/new_message.log',level=logging.DEBUG)

os.chdir(mailboxdir)
for mailbox in os.listdir('.'):
    if not os.path.isdir(mailbox): continue
    inboxdir = os.path.join(mailbox, 'INBOX')
    if not os.path.exists(inboxdir): continue

    msgcnt = 0
    for infile in os.listdir(inboxdir):
        if infile.startswith('msg') and infile.endswith('.wav'):
            msgcnt += 1

    # Make an outbound call
    callfile=os.path.join('/tmp',mailbox)

    outfile = os.path.join(outgoingdir,mailbox)
    pause_that_refreshes = 5
    while pause_that_refreshes and os.path.exists(outfile):
        pause_that_refreshes -= 1
        time.sleep(1)

    with open(callfile,'w') as fp:
        dest_context = 'mwi_state'
        if msgcnt == 0:
            mb = '#3'
        else:
            mb = '*3'
        mb += mailbox
        channel = "SIP/one-stage/" + mb
        msg = sip % (channel, mb_context, mb, dest_context)
        fp.write(msg)
        fp.close()
    shutil.move(callfile,outgoingdir) # FIRE!

    time.sleep(4)

exit(0)
