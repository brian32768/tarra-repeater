#!/bin/bash
#
#  This script is run every time the system is booted, from rc.local
#
RECIPIENTS="brian@wildsong.biz"

# Runs at boot time, so give it some time to actually configure its network ports
#sleep 30

# Send inside address(es)
#ifconfig | mail -s "TARRA network" $RECIPIENTS 

# Send outside address
#wget -q -O - checkip.dyndns.org|sed -e 's/.*Current IP Address: //' -e 's/<.*$//' | mail -s "TARRA public ip address" $RECIPIENTS &

exit 0
