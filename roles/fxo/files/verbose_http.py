#!/usr/bin/env python
# Foundations of Python Network Programming - Chapter 9 - verbose_handler.py
# HTTP request handler for urllib2 that prints requests and responses.
from io import StringIO

from httplib import HTTPResponse, HTTPConnection
import urllib.request

verbose = False
#verbose=True

class VerboseHTTPResponse(HTTPResponse):

    def _read_status(self):
        s = self.fp.read()
        if verbose:
            print('-' * 20, 'Response', '-' * 20)
            print(s.split('\r\n\r\n')[0])
        self.fp = StringIO.StringIO(s)
        return HTTPResponse._read_status(self)

class VerboseHTTPConnection(HTTPConnection):

    response_class = VerboseHTTPResponse
    def send(self, s):
        if verbose:
            print('-' * 50)
            print(s.strip())
        HTTPConnection.send(self, s)

class VerboseHTTPHandler(urllib2.HTTPHandler):
    def http_open(self, req):
        return self.do_open(VerboseHTTPConnection, req)

