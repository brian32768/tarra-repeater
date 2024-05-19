#!/bin/bash
#
#  Sets firewall to accept or block calls from unknown locations
#    phonewall.sh 0  means block calls
#    phonewall.sh 1  means accept calls
#

# Check that we can run
sudo /sbin/iptables -L INPUT -n > /dev/null
if [ "$?" != "0" ]; then
    echo "having a permissions problem"
    exit 255
fi

function chaintest {
    sudo /sbin/iptables -L $1 -n | grep ACCEPT | grep '0.0.0.0/0.*0.0.0.0/0' > /dev/null
    # 0 means "found rule"
    # not 0 means "did not find rule"
    return $?
}

function drop {
  list=$1
  chaintest $list
  if [ "$?" == "0" ]; then
      sudo /sbin/iptables -D $list -j ACCEPT
      if [ "$?" != "0" ]; then
	  echo "rule delete failed"
	  exit 1
      fi
  fi
}

function accept {
  list=$1
  chaintest $list
  if [ "$?" == "1" ]; then
      sudo /sbin/iptables -I $list -j ACCEPT
      if [ "$?" != "0" ]; then
	  echo "rule add failed"
	  exit 1
      fi
  fi
}

if [ "$1" == "0" ]; then
    drop sip_whitelist
    drop media_whitelist
fi

if [ "$1" == "1" ]; then
    accept sip_whitelist 
    accept media_whitelist
fi

chaintest sip_whitelist
if [ $? == "0" ]; then
    echo "accepting calls"
else
    echo "refusing calls"
fi

exit 0
