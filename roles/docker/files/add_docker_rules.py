#!/usr/bin/env python
#
#  Fix up the firewall rules to allow Docker to work.
#
from __future__ import print_function

# Use those functions to enumerate all interfaces available on the
# system using Python.
# Found at <http://code.activestate.com/recipes/439093/#c1>

import socket
import fcntl
import struct
import array
import iptc

def all_interfaces():
    max_possible = 128  # arbitrary. raise if needed.
    bytes = max_possible * 32
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    names = array.array('B', '\0' * bytes)
    outbytes = struct.unpack('iL', fcntl.ioctl(
        s.fileno(),
        0x8912,  # SIOCGIFCONF
        struct.pack('iL', bytes, names.buffer_info()[0])
    ))[0]
    namestr = names.tostring()
    lst = []
    for i in range(0, outbytes, 40):
        name = namestr[i:i+16].split('\0', 1)[0]
        ip   = namestr[i+20:i+24]
        lst.append((name, ip))
    return lst

def format_ip(addr):
    return str(ord(addr[0])) + '.' + \
           str(ord(addr[1])) + '.' + \
           str(ord(addr[2])) + '.' + \
           str(ord(addr[3]))

def show_rules():
    table = iptc.Table(iptc.Table.FILTER)
    for chain in table.chains:
        print("=======================")
        print("Chain ", chain.name)
        for rule in chain.rules:
            print("Rule", "proto:", rule.protocol, "src:", rule.src, "dst:", \
               rule.dst, "in:", rule.in_interface, "out:", rule.out_interface,)
            print("Matches:",)
            for match in rule.matches:
                print(match.name,)
                print("Target:",)
                print(rule.target.name)
        print("=======================")

def add_rules():
    # Enable masquerading
    print("iptables -t nat -A POSTROUTING -s 172.17.0.0/16 ! -o docker0 -j MASQUERADE")
    # Allow connections to containers
    print("iptables -t filter -A FORWARD -o docker0 -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT")
    # Allow internal and external container communication
    print("iptables -t filter -A FORWARD -i docker0 ! -o docker0 -j ACCEPT")
    print("iptables -t filter -A FORWARD -i docker0 -o docker0 -j ACCEPT")

if __name__ == "__main__":

    # Test policy: if we're not running a restrictive firewall, stop now.

    show_rules()
    
    # Find out if we have a docker interface
    ifs = all_interfaces()
    for i in ifs:
        print("%12s   %s" % (i[0], format_ip(i[1])))

    add_rules()

