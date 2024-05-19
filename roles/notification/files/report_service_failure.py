#!/usr/bin/env python
#
#  Send notification that a service has failed.
#  Rate limited to avoid hammering cell phones.
#
from __future__ import unicode_literals

import sys,os
import socket
import subprocess
import locale
import logging
from send_notification import send_notification
from boot_notice import find_public_ip

logger = logging.getLogger(__name__)

rate_limit = 1800 # Minimum seconds between runs = half hour

def get_unit_status(unit):
    # Read the status of the service unit on which we're reporting.
    encoding = locale.getdefaultlocale()[1]
    unitstatus = ""
    cmd = ["systemctl", "show", unit]
    out = None
    try:
        out = subprocess.check_output(cmd)
    except OSError as e:
        logger.error("%s not found; testing on the mac?" % cmd[0])

    if out:
        for line in out.decode(encoding).split():
            try:
                (k,v)=line.split('=')
                if k=='ActiveState':
                    unitstatus += "state: %s " % v
                elif k=='SubState':
                    unitstatus += "substate: %s " % v
            except:
                pass

    return unitstatus

def send_failure_notification(unit, hostname, recipient_file):

    unitstatus = get_unit_status(unit)

    message = "Unit \"%s\" on \"%s\": %s\n" % (unit, hostname, unitstatus)

    # Including public IP means we might be able to just click and go from our precious smartphones...
    public_ip = find_public_ip()
    if public_ip:
        message += "https://%s/\n" % public_ip

#    if machineid: message += " Machine Id: %s" % machineid
#    if bootid: message += " Boot Id: %s." % bootid

    email_subject = 'Service "%s" failed on %s' % (unit, hostname)
    count = send_notification(recipient_file, message, email_subject, message)
    logger.info('Notification sent to %d recipients.' % count)


########################################################################

if __name__ == "__main__":

    # defaults 
    hostname = socket.gethostname()
    unit="UNKNOWN"
    
    try:
        unit = sys.argv[1]
        hostname = sys.argv[2]
    except:
        logger.error("Bad arguments. Need unit and hostname.")
        exit(1)

    # You need to chdir to the folder containing admin.list before starting.
    recip_list = 'admin.list'
    try:
        recip_list = sys.argv[3]
    except:
        pass

#    # Don't send messages too often!
#    ht = HangTime(rate_limit)
#    if not ht.check():
#        logger.info("Rate limiting notifications!")
#        exit(0)

    send_failure_notification(unit, hostname, recip_list)

    exit(0)
