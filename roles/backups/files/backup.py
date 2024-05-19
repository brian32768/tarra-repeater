#!/usr/bin/env python
#
#  Normally run as a systemd service once a day,
#  can also be invoked with 'systemctl start backup'.
#
#  1. Dump the MySQL databases to a datestamped tar file.
#  2. Make a datestamped tar file of critical files
#  3. Copy everything offsite.
#  4. Delete old backup files
#
# N.B. A router whitelist protects the rsync port.
#
import sys
import os, stat
import subprocess
from datetime import datetime

def back_up_files(home, source_list, tarball):
    """Take a list of files and/or directories and generate a compressed tarball.
Exclude backup user's home to avoid recursion. Returns True on success."""
    ok = True
    if len(source):
        cmd = ['tar', '-c', '-z']
        if home: cmd += ['--exclude', home]
        cmd += ['-f', tarball]
        cmd += source_list
        print(cmd)
        rval = subprocess.call(cmd)
        if rval: ok = False
    return ok

def back_up_databases(databases, user, password, tarball):
    """ For each listed database, use mysqldump to create a temporary dump (.sql) file
    and then wrap them all into a tarball. Delete the sql files. """
    ok = True
    dumper = '/usr/bin/mysqldump'
    if not os.path.exists(dumper): return ok
    sqlfiles = []
    for db in databases:
        sql = db + '.sql' # name of file to save in working directory
        cmd = [dumper, "--lock-tables", "-u" + user, "-p" + password, "-r", sql]
        if db == 'mysql': cmd.append('-E') # back up mysql event table
        cmd.append(db)
        #print("Cmd: %s\n" % cmd) # this puts secrets into the log file!!
        rval = subprocess.call(cmd)
        if rval: ok = False
        sqlfiles.append(sql)

    if len(sqlfiles):
        back_up_files(sqlfiles, tarball)
        for sql in sqlfiles:
            if os.path.exists(sql): os.unlink(sql)

    return ok

def remote_copy(source, rsync_dest):
    """ Ship a source folder tp a remote dest via rsync.
    Returns True if successful.  """
    ok = True
    cmd = ["rsync", "-av", source, rsync_dest]
    rval = subprocess.call(cmd)
    if rval: ok = False
    return ok

if __name__ == "__main__" :

    test_mode = True
    try:
        if os.environ["NIGHTLY_BACKUP"]=="1":
            test_mode = False
            print("Commencing full backup.")
    except KeyError:
        pass
    #test_mode = False # Back up all files regardless of setting

    remove_local_files = False
    try:
        if os.environ["REMOVE_LOCAL_FILES"]=="1":
            remove_local_files = True
    except KeyError:
        print("Will not remove local files.")
        pass

    # This is a generic script... if there is no DATABASE_USER defined
    # I assume you don't want to back up any MySQL databases.
    mysql_user = mysql_password = None
    try:
        mysql_user = os.environ["DATABASE_USER"]
        mysql_password = os.environ["DATABASE_PASSWORD"]
    except KeyError:
        # this writes secrets to the logfile so don't use on production machines
        #for item in os.environ: print("%s : %s" % (item, os.environ[item]))
        print("MySQL environment not defined, skipping MySQL backup.");

#    print(os.environ["RSYNC_AUTH_USER"])
#    print(os.environ["RSYNC_SERVER"])
#    print(os.environ["RSYNC_PORT"])
#    print(os.environ["RSYNC_MODULE"])

    try:
        rsync_dest = "rsync://%s@%s:%s/%s" % \
        (os.environ["RSYNC_AUTH_USER"],
         os.environ["RSYNC_SERVER"],
         os.environ["RSYNC_PORT"],    
         os.environ["RSYNC_MODULE"]) # "module" has to be in rsync file on backups host
    except KeyError:
        print("Missing environment settings. Quitting.")
        exit(0)

    datestamp = datetime.now().strftime("%Y-%m-%d")

    home = os.environ['HOME']
    voicemail = []
    
    if test_mode:
        print("**TESTING backup system.**")
        databases = ['mysql']
        testfile = '/tmp/backup_test'
        with open(testfile,'w') as fp:
            fp.write("%s\n" % datestamp)
        tarfiles = [testfile]
    else:
        databases = None;
        try:
            databases = os.environ['DATABASES'].split()
        except KeyError:
            print("DATABASES undefined, skipping MySQL backup.")
            pass
        try:
            tarfiles = os.environ['TARFILES'].split()
        except KeyError:
            print("TARFILES undefined. Quitting.")
            exit(-1)
        try:
            # Optional voicemail backup
            voicemail = os.environ['VOICEMAIL'].split()
        except KeyError:
            print("VOICEMAIL directory path undefined, skipping.")

    backup_dir = os.path.join(home, datestamp)
    if not os.path.exists(backup_dir):
        try:
            os.mkdir(backup_dir)
        except Exception as e:
            print("Can't create output directory \"%s\"; %s" % (backup_dir,str(e)))
            exit(1)
        os.chmod(backup_dir, stat.S_IRWXU|stat.S_IXGRP|stat.S_IRGRP)

    # Save current directory and go to backup output directory
    cwd = os.getcwd()
    os.chdir(backup_dir)

    tarballs = []

    # databases
    tarball = "databases.%s.tar.gz" % datestamp
    if databases and mysql_user and mysql_password: 
        ok = back_up_databases(databases, mysql_user, mysql_password, tarball)
        if ok: tarballs.append(tarball)

    # voicemail spool
    if len(voicemail):
        tarball = "voicemail.%s.tar.gz" % datestamp
        ok = back_up_files(voicemail, tarball)
        if ok: tarballs.append(voicemail)

    # other important files
    tarball = "files.%s.tar.gz" % datestamp
    ok = back_up_files(home, tarfiles, tarball)
    if ok: tarballs.append(tarball)

    ok = remote_copy(backup_dir, rsync_dest)
    # If the remote backup succeeds then remove the tar files.
    if ok and remove_local_files:
        for f in tarballs:
            os.unlink(f)

    os.chdir(cwd)
    # If the remote backup succeeds then remove the folder, too.
    if remove_local_files and os.path.exists(backup_dir):
        os.rmdir(backup_dir)

    exit(0)
