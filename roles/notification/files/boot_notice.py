#!/usr/bin/env python
#
#  TODO -- add additional means to determine outside address,
#  for example by asking our router.
#
import sys,os
import subprocess
import locale
import re
import urllib.request
from send_notification import send_notification

re_inet    = re.compile(r'addr:([\d\.]+)') # This is the Linux version. 
re_address = re.compile(r'Current IP Address: ([\d\.]+)')
encoding   = locale.getdefaultlocale()[1]

def find_ip_addresses():
    """ Find inside ip address(es) using 'ifconfig' """
    addresses = []
    cmd = ['/sbin/ifconfig']
    out = subprocess.check_output(cmd)
    inside = ""
    for line in out.decode(encoding).split("\n"):
        mo = re_inet.search(line)
        # Ignore localhost
        if mo and mo.group(1)!='127.0.0.1':
            addresses.append(mo.group(1))
    return addresses

def find_public_ip():
    """ Return public ip address for this machine. """
    outside_ip = None
    try:
        with urllib.request.urlopen('http://checkip.dyndns.org') as f:
            out = f.read().decode(encoding)
        mo = re_address.search(out)
        if mo:
            outside_ip = mo.group(1) # pull ip out of html return
    except:
        pass
    return outside_ip

if __name__ == "__main__":

    hostname = sys.argv[1]

    # To test, you can use the local file 'test.list' on the command line
    # or just use the default 'admin.list'.
    recipients = 'admin.list'
    try:
        recipients = sys.argv[2]
    except:
        pass

    addresses = "\n".join(find_ip_addresses())
    public_ip = find_public_ip()

    message = "%s\nhttps://%s/\n%s" % (hostname, public_ip, addresses)

    # If I am running on a development machine like the Mac, I can set
    # MAILHOST to something usable like "bellman".
    mymailhost = "localhost"
    try:
        mymailhost = os.environ['MAILHOST']
    except:
        pass

    send_notification(recipients, message, 
                      "Host %s started." % hostname, 
                      message, 
                      mailhost = mymailhost)

    exit(0)

