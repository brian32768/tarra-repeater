#!/bin/echo "This script should not be directly executable"
#
# ***           CHANGES WILL BE LOST               ***
# *** Installed from fogg-ansible dhcp-server role ***
#
#  Watch for radios associating/disassociating in UniFi logs.
#
from __future__ import print_function
import sys, re
import json
from rest import *

re_association = re.compile(r'STA (.*) IEEE 802.11: (\w+)')

logfile = '/var/log/daemon.log'

# ---------------------------------------------------------------------------
# Sample:
#  Apr 13 13:39:29 elab-unifi.wildsong.biz ("U7LT,802aa890cd65,v3.7.17.5220") hostapd: ath0: STA a0:0b:ba:e8:c5:8a IEEE 802.11: associated
#  Apr 13 13:39:29 elab-unifi.wildsong.biz ("U7LT,802aa890cd65,v3.7.17.5220") hostapd: ath0: STA a0:0b:ba:e8:c5:8a RADIUS: starting accounting session 58EFE0DC-00000003
#  Apr 13 13:39:29 elab-unifi.wildsong.biz ("U7LT,802aa890cd65,v3.7.17.5220") hostapd: ath0: STA a0:0b:ba:e8:c5:8a WPA: pairwise k

def send_update(action, mac):
    """ Send an update via REST to the fabled service. """
    payload = { "action " : action,
                "mac "    : mac } 
    json.dumps(payload) # serialize the dictionary
    return send(payload)

# ------------------------------------------------------------------------

if __name__ == '__main__':

    with open(logfile,"r") as fp:
        # read to end of logfile then block and wait for more
        for line in fp.readlines():
            mo = re_association.search(line)
            try:
                mac = mo.group(1)
                action = mo.group(2)
                if action == 'associated' or action == 'disassociated':
                    send_update(action,mac)
            except:
                pass
    exit(0)

# -- 30 --
