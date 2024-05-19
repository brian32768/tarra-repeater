
#
# Dump the databases
#
function databases()
{

    $MYDUMP -E mysql > $BACKUPDIR/mysql.sql

    # Now I back up all the others (at the moment "all" means "both".)
    for db in $DATABASES; do 
       $MYDUMP $db > $BACKUPDIR/$db.sql
    done

    # If TAR succeeds then delete the SQL files right now
    # so they don't get shipped to the backups server by rsync later.
    
    cd $BACKUPDIR && \
	tar -czf $BACKUPDIR/mysql_backups.tar.gz *.sql && \
	find $BACKUPHOME -name '*.sql' -print -exec rm {} \;
}


Get the file/folder names from ENVIRONMENT
Put everything into one tarfile
#
# Make a voicemail tar file - ignore Deleted and tmp files.
#
function voicemail()
{
    cd /var/spool/asterisk/voicemail && \
    tar -czf $BACKUPDIR/voicemail.tar.gz --exclude='*/tmp/*' --exclude='*/Deleted/*' default
}

#
# Make an Asterisk config (etc) tar file
#
function astconfig()
{
    cd /etc && \
    tar czf $BACKUPDIR/astconfig.tar.gz --exclude=SAMPLE asterisk
}

#
#  Copy to remote server
#  and delete local files on success
#
function remotecopy()
{
    cd $BACKUPHOME && rsync -av $DATESTAMP $REMOTESERVER  || { echo "Rsync failed"; exit 1; }
}

########################################################################

echo Delete old backups from local server
find $BACKUPHOME -mtime 5 -name '*.gz' -print -exec rm {} \;
rm -rf $BACKUPDIR

exit 0
