#!/usr/bin/python
#
#   Create any subchains that don't exist
#   Put the targets for the subchains into iptables in the right place.
#   The actual contents of the subchains are generated in update_whitelists.py
#   This script has to run first to create the empty subchains
#   and attach them to INPUT.
#
#   NB it removes any existing targets, so if the script dies at that moment
#   it leaves the firewall CLOSED (assuming INPUT default policy is DROP).
#
#   This script does not need any files,
#   it just processes embedded data and updates iptables.
#
import subprocess

dryrun = False
#dryrun = True # Don't really do the iptables commands, just print them.
verbose = False
#verbose = True # Show what iptables commands are executed

# Some target subchains are filtered and some are not.
# This list controls how the subchain targets are added to the INPUT chain.

#   (iptable subchain,   protos,        ports,      priority
subchains = [
    ("admin_whitelist",  [],            0,             0, ), # no filtering

    ("twilio_whitelist", ["tcp"],       "5060:5061",   1,  ), # filtered goes near start

    ("fail2ban-asterisk-udp", ["udp"],       "5060,5061",   10, ),
    ("fail2ban-asterisk-tcp", ["tcp"],       "5060,5061",   11, ),
    ("fail2ban-postfix",      ["tcp"],       "25,465",      12, ),
    ("fail2ban-ssh",          ["tcp"],       "22",          13, ),

    ("sip_whitelist",         ["tcp","udp"], "5060,5061",   20, ), # filtered goes after fail2ban
    ("media_whitelist",       ["udp"],       "5000:40000",  22, ), # filtered " 

    ("iax_whitelist",         ["udp"],       "4569",        30, ), # filtered "

    # logging subchain handled as special case since we don't turn it on by default
]

# ========================================================================

def call(cmd):
    """Do a system call, respecting the dryrun and verbose global flags."""

    if verbose: print ' '.join(cmd)
    if dryrun: return
    try:
        subprocess.call(cmd)
    except Exception as e:
        print e
    return
        
def get_targets():
    """Build a hash of chains that are already in INPUT as targets
and find the correct insertion point"""

    dtarget = {}
    cmd = ["iptables", "-L", "INPUT", "-n", "--line-numbers"]
    out = subprocess.check_output(cmd)
    for line in out.split("\n"):
        tokens = line.split()
        if not tokens: continue
        try:
            ln = int(tokens[0])
        except:
        # Skip any line that does not start with a line number
            continue
        dtarget[tokens[1]] = ln # Store the line number
    return dtarget

def get_subchains():
    """Build a hash of existing subchains"""

    dsubchains = {}
    cmd = ["iptables", "-L", "-n"]
    out = subprocess.check_output(cmd)
    for line in out.split("\n"):
        tokens = line.split()
        if not tokens: continue
        if tokens[0] == "Chain":
            # only interested in subchains that show up as "Chain chainname (N references)"
            try:
                n = tokens[2][1:]
                references = int(n)
                dsubchains[tokens[1]] = references
            except:
                #print "Not interested in ",line
                pass
    return dsubchains

# ========================================================================

if __name__ == "__main__":

    # Create subchains that don't already exist

    dsubchains = get_subchains()
    for tup in subchains:
        chain = tup[0]
        if not dsubchains.has_key(chain):
            cmd = ["iptables", "-N", chain]
            call(cmd)

    # Add logging subchain if it does not exist
    chain = 'logging'
    if not dsubchains.has_key(chain):
        cmd = ["iptables", "-N", chain]
        call(cmd)

    dtargets = get_targets()
    #print dtargets
    
    # Remove existing subchain targets
    # so they can be re-inserted in the correct places
    for tup in subchains:
        target = tup[0]
        while dtargets.has_key(target): # there can be more than one target (-p udp,tcp)
            cmd = ["iptables", "-D", "INPUT", str(dtargets[target])]
            call(cmd)
            del dtargets[target] # prevent infinite loop in dryrun
            if not dryrun:
                dtargets = get_targets() # Rule numbers might change after each deletion

    # Add target subchains to INPUT, in the correct places
    # and with filters set as needed.

    # Create a list of iptables commands
    
    newtargets = []
    for (chain, proto, ports, priority) in subchains:

        # Find target insertion point - either insert or append everything
        insertion_point = 0 # append
        dtargets = get_targets()
#        if dtargets.has_key(fail2ban):
#            insertion_point = dtargets[fail2ban] + 1
        #print "Insertion point will be %d" % insertion_point

        if insertion_point > 0 or priority < 2:
            if priority<2:
                # force high priority whitelists to the front of the line
                ip = "1"
            else:
                ip = str(insertion_point)
            # Add the new chain after the fail2ban chain
            basecmd = ["iptables", "-I", "INPUT", ip, "-j", chain]
        else:
            # Append the new chain
            basecmd = ["iptables", "-A", "INPUT", "-j", chain]
        
        if proto:
            # This is a filtered rule
            for p in proto:
                cmd = []
                cmd.extend(basecmd)

                options = ["-p", p]
                if ports.find(',')>=0:
                    # Multiple ports like "22,465"                                                                             
                    options.append("-m")
                    options.append("multiport")
                    options.append("--dports")
                    options.append(ports)
                else:
                    # Just one port or a range like "500:1000"                                                                 
                    options.append("--dport")
                    options.append(ports)
                cmd.extend(options)

                newtargets.append(cmd)
                call(cmd)
        else:
            # This is an unfiltered rule
            newtargets.insert(0,basecmd)
            call(basecmd)

# That's all!
