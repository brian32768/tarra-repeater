#!/usr/bin/env python
#
#  Change the status of a custom device state in Asterisk
#  Called from Asterisk via voicemail.conf externnotify
#
import sys
import subprocess

vm_context = sys.argv[1]
exten      = sys.argv[2]
vm_count   = sys.argv[3]

res = 0

# Get rid of the context (usually 'default')
try:
    (ext, cnt) = exten.split('@')
except:
    ext = exten

# Only works for shared mailboxes
if ext=='201' or ext=='202' or ext=='203' or ext=='204' or ext=='205':
    try:
        vc = int(vm_count)
    except:
        vc = 0
    if vc == 0:
        grp = 'groupmwi-off'
    else:
        grp = 'groupmwi-blink'

    cmd = ["/usr/sbin/asterisk", "-rx originate Local/" + ext + '@' + grp + " extension 4"]
    res = subprocess.call(cmd)

exit(res)
