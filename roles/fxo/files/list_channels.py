#!/usr/bin/env python
#
#  Read all sip channel data from Asterisk and return a list of active GS FXO lines.
#
sample="""
Success
Peer             User/ANR         Call ID          Format           Hold     Last Message    Expiry     Peer      
10.1.10.201      (None)           50d9f4711bf223c  (nothing)        No       Init: OPTIONS              gs-fxo-2  
10.1.10.12       150              1134338106-5017  (nothing)        No       Rx: BYE                    150       
10.1.10.12       150              707353ed2d2be4f  (ulaw)           No       Init: INVITE               150       
10.1.10.12       150              669278656-50179  (ulaw)           No       Rx: ACK                    150       
10.1.10.201      (None)           0ed37f410861ce8  (nothing)        No       Init: OPTIONS              gs-fxo-4  
5 active SIP dialogs
--END COMMAND--
"""
import asterisk.manager
import sys, re

re_find_gs = re.compile(r'gs-fxo-(\d)')

def find_lines(channeldata):
    """ Parse the channel data and return a list of gs fxo lines,
    integers representing the lines, 1..4] """
    
    lines = []
    if channeldata:
        for line in channeldata.split('\n'):
            mo = re_find_gs.search(line)
            if mo:
                lines.append(mo.group(1))
    return lines

def get_channels(host,username,password):
    """ Connect with AMI and get line data """
    manager = asterisk.manager.Manager()
    try:
        manager.connect(host)
        manager.login(username, password)
        response = manager.status()
        response = manager.command('sip show channels')
        manager.logoff()
    except asterisk.manager.ManagerSocketException as e:
        print("Error connecting to the manager: %s" % e)
        sys.exit(1)
    except asterisk.manager.ManagerAuthException as e:
        print("Error logging in to the manager: %s" % e)
        sys.exit(1)
    except asterisk.manager.ManagerException as e:
        print("Error: %s" % e)
        sys.exit(1)

    return find_lines(response.data)

if __name__ == '__main__':
    # unit test

    host = '127.0.0.1'
    username = 'admin'
    password = sys.argv[1]

    print("sample")
    lines = find_lines(sample)
    print(lines)

    print("real - errors unless you are root")
    lines = get_channels(host,username,password)
    print(lines)

    exit(0)


