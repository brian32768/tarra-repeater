#!/bin/bash
#
# Wrapper to call python virtualenv from dnsmasq,
# which apparently wants only a simple argument.
#
cd /var/lib/vastra/dns/
venv/bin/python dnsmasq.py $*
