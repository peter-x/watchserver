#!/usr/bin/env python

import requests
import time
import cgi

import keys

print 'Content-type: text/json; charset=utf-8'
print 'Access-Control-Allow-Origin: *'
print

print requests.get('https://api.darksky.net/forecast/%s/%s/?units=si&nocache=%d' % (
    keys.darkskyapi,
    '52.5073036,13.4366898',
    time.time()
)).text.encode('utf-8')
