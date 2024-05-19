#!/usr/bin/env python
#
#  The phonewall status notifier
#
import sys,os
import subprocess
import locale
from send_notification import send_notification

encoding   = locale.getdefaultlocale()[1]

def find_phonewall_status():
    rval = subprocess.Popen('/usr/local/sbin/phonewall.sh', stdout=subprocess.PIPE).communicate()[0]
    return rval.splitlines()[0].decode(encoding)

if __name__ == "__main__":

    hostname = sys.argv[1]
    message = "%s %s" % (hostname, find_phonewall_status())

    # To test, you can use the local file 'test.list' on the command line
    # or just use the default 'admin.list'.
    recipients = 'admin.list'
    try:
        recipients = sys.argv[2]
    except:
        pass

    # If I am running on a development machine like the Mac, I can set
    # MAILHOST to something usable like "bellman".
    mymailhost = "localhost"
    try:
        mymailhost = os.environ['MAILHOST']
    except:
        pass

    send_notification(recipients, message, 
                      "%s phonewall status" % hostname, 
                      message, 
                      mailhost = mymailhost)
    exit(0)

