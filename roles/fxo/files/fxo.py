#!/usr/bin/env python
#
#  Find stuck lines on the Grandstream and
#  optionally hang them up.
#
#  ref: "Foundations of Python Network Programming"
#       for information about the http code here
#
from verbose_http import VerboseHTTPHandler
from urllib.request import build_opener, HTTPCookieProcessor
import cookielib
from HTMLParser import HTMLParser
import sys,os,re
from ConfigParser import ConfigParser
import time

from list_channels import get_channels

astdir = '/etc/asterisk'
manager_file = 'manager.conf'
sip_file = 'sip-fxo-gateway.conf'

# Read configuration for GrandStream access

astconfig = ConfigParser()
astconfig.read(os.path.join(astdir,sip_file))
try:
    host=astconfig.get('gs-fxo','host')
    gs_password=astconfig.get('gs-fxo','webpass')
except Exception as e:
    print("Could not get host/webpass")
    exit(1)

astconfig.read(os.path.join(astdir,manager_file))
try:
    ami_host = 'localhost'
    ami_user = 'admin'
    ami_secret = astconfig.get(ami_user,'secret')
except Exception as e:
    print("Could not read AMI credentials")
    exit(1)

re_linestate = re.compile(r'^\s*Line\s(\d):\s+(.*)$')
re_busy = re.compile(r'^busy,\s+(.*)$')

cookies = cookielib.CookieJar()
cookie_opener = build_opener(VerboseHTTPHandler, HTTPCookieProcessor(cookies))

def usage():
    print("""fxo {status|all|linenumbers...}

"fxo status" shows status of each line and exits
"fxo all" attempts to clear all lines
"fxo" followed by line number(s) clears those lines
""")
    return


class MyHTMLParser(HTMLParser):
              
    linestatus = [-1,-1,-1,-1]
    
    def handle_starttag(self, tag, attrs):
        #print("Encountered a start tag:", tag)
        return

    def handle_endtag(self, tag):
        #print("Encountered an end tag :", tag)
        return

    def handle_data(self, data):
        #print("Encountered some data  :", data)

        mo = re_linestate.search(data)
        if mo:
            try:
                linenum = int(mo.group(1))-1
                status = mo.group(2).strip()
                #print(status)
                mo = re_busy.search(status)
                if mo:
                    status = 1
                else:
                    if status == 'Connected, idle.':
                        status = 0
                    else:
                        status = '?? ' + status
                self.linestatus[linenum] = status
            except Exception as e:
                print("Trouble in parser", e)
        return

class GXW(object) :
    """ A class that talks to a Grandstream GXW4104 """

    def __init__(self, host, password):
        self.baseurl = 'http://%s/' % host
        self.password = password
        return
    
    def login(self) :
        """ Log into the GXW and get a session cookie.
            Return True on success. """
        form = urllib.urlencode({'P2': self.password, 'gnkey':'0b82', 'Login':'Login'})
        response = cookie_opener.open(self.baseurl + 'dologin.htm', form)
        print(response)
        return (response.code == 200)

    def get_status(self):
        """ Get a list of lines, 0 is off and 1 is busy """
        status_page = self.baseurl + 'index_net.htm'
        response = cookie_opener.open(status_page)
        if (response.code == 200):
            parser = MyHTMLParser()
            parser.feed(response.read())
            return parser.linestatus
        return None

    def send_hangup(self,linenum) :
        """ Send hangup command to a line """
        print("sendhangup(%d)" % linenum)

        cmd = self.baseurl + 'command_send_300%d' % linenum
        response = cookie_opener.open(cmd)
        return (response.code == 200)

def validate_lines(lines):
    for line in lines:
        n = int(line)
        if n < 1 or n > 4: raise ValueError
        lines_to_clear = [linenum]



if __name__ == '__main__':

    try:
        command = sys.argv[1]
        if command == "status":
            show_status()
        elif command == "all":
            lines = [1,2,3,4]
        else:
            lines = sys.argv[1:]
            command = ""
    except:
        usage()
        exit(1)

    try:
        validate_lines(lines)
    except ValueError:
        usage()
        exit(-1)

    linestatus = None
    gxw = GXW(host, gs_password)
    if not gxw.login():
        print("log in failed")
    else:
        linestatus = gxw.get_status()

    if not linestatus:
        print("get_status failed")
        exit(-1)

    print("FXO line status:", linestatus)

    active_channel_list = get_channels(ami_host, ami_user, ami_secret)
    print("Channels active:", active_channel_list)

    # If this is a simple status request then we're done.
    if command=='status': exit(0)

    # Attempt to clear stuck lines and then report results.

    disconnected = 0
    failed = 0
    linescleared = []

    # I can't tell which line is connected to which channel
    # so if there are ANY active channels, do NOT clear ANY line.

    if len(active_channel_list) == 0:
        for line in lines:
            if line in linestatus and gxw.sendhangup(line):
                linescleared.append(line)
                print("Disconnected %d." % line)
            else:
                print("Disconnect %d failed." % disconnected)
        time.sleep(3)

    linestatus = gxw.get_status()
    active_channel_list = get_active_channels()

    # Show status

    busy = 0
    for line in [0,1,2,3]:
        if linestatus[line]:
            print("%d: **BUSY**" % (line+1))
            busy += 1

    if not busy:
        print("All lines CLEAR")

    sys.exit(busy)
