#!/bin/bash

export RSYNC_AUTH_USER="vmpbx"
export RSYNC_PASSWORD="58jhifwaw0i9fjnvsdbjh&^TGHHVB"
export RSYNC_MODULE="testonly"
export RSYNC_SERVER="backups.wildsong.biz"
export DATABASES="asterisk"
export TARFILES="/etc/hosts"
export RSYNC_PORT="8773"

# 0 = run in test-only mode
NIGHTLY_BACKUP="0"

./backup.py vmpbx



