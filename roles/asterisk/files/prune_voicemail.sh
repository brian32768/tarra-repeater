#!/bin/bash
#
#  Remove any Deleted voicemail more than 30 days old.
#  FIXME we should eventually sunset all old voicemails too.
#  FIXME or at least report on them.
#

# Find "Deleted" folders (which currently only exist on Ledson.)

VOICEMAILSPOOL="/var/spool/asterisk/voicemail"
if [ -e "$VOICEMAILSPOOL" ]; then 

  for m in `find $VOICEMAILSPOOL -type d -name Deleted`
  do
    # Find old message files in the 'Deleted' folders.
    find $m -type f -mtime +30 -name 'msg*' -exec rm {} \;
  done

fi
