#!/bin/echo "This script should not be directly executable"
#
# ***           CHANGES WILL BE LOST               ***
# *** Installed from fogg-ansible dhcp-server role ***
#
#  Send a REST update to a server I have not written yet.
#  This is called from dnsmasq when a DHCP change happens.
#  Arguments (from dnsmasq):
#      add | del | old  'old' messages happen on restarts of dnsmasq daemon
#      MAC number
#      ip address
#      hostname (optional)
#
from __future__ import print_function
import sys, syslog, re
import json
from rest import *

ACTION_ADD = "add"
ACTION_DEL = "del"
ACTION_OLD = "old"

re_ipaddr = re.compile(r'\d+\.\d+\.\d+\.\d+')

def send_update(action, mac, ipaddr, hostname):
    """ Send an update via REST to the fabled service. """
    payload = { "action " : action,
                "mac "    : mac,
                "ipaddr"  : ipaddr,
                "hostname": hostname }
    json.dumps(payload)  # serialize the dictionary
    return send(payload)

if __name__ == '__main__':

    syslog.openlog(logoption=syslog.LOG_ERR,facility=syslog.LOG_DAEMON)

    try:
        action = sys.argv[1]
        mac    = sys.argv[2]
        ipaddr = sys.argv[3]
    except IndexError:
        syslog.syslog(syslog.LOG_ERR, "Could not read arguments. (add|del mac ip [hostname])")
        exit(-1)

    if not re_ipaddr.search(ipaddr):
        syslog.syslog(syslog.LOG_ERR, "ERROR: Badly formed ipaddr %s" % ipaddr)
        exit(-1)
        
    try:
        hostname = sys.argv[4]
    except IndexError:
        # We have no name so Turn our IP into a name
        hostname = ipaddr.replace('.','_')

    syslog.syslog("%s %s %s %s" % (action,mac,ipaddr,hostname))

    try:
        send_update(action,mac,ipaddr,hostname)
    except Exception as e:
        syslog.syslog(syslog.LOG_ERR, "ERROR %s" % e)
        exit(-1)

    exit(0)

# -- 30 --
