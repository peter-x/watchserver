#!/usr/bin/env python

import requests
import time
import datetime
import json
import sys

import keys

print 'Content-type: text/json; charset=utf-8'
print 'Access-Control-Allow-Origin: *'
print

def retrieveData(origin, destination):
    return requests.post('https://demo.hafas.de/openapi/vbb-proxy/trip',
        data={
            'format': 'json',
            'accessId': keys.vbbapikey,
            'originCoordLat': origin['lat'],
            'originCoordLong': origin['long'],
            'destCoordLat': destination['lat'],
            'destCoordLong': destination['long']
        }
    ).json()

def parseLegEnd(end):
    return {
        'name': end['name'],
        'dateTime': end['date'] + ' ' + end['time']
    }

def parseLeg(leg):
    ret = {}
    if leg['type'] == 'WALK':
        ret['name'] = 'walk'
        ret['direction'] = ''
    else:
        ret['name'] = leg['name'].strip()
        ret['direction'] = leg['direction']
    ret['origin'] = parseLegEnd(leg['Origin'])
    ret['destination'] = parseLegEnd(leg['Destination'])
    return ret

def parseTrip(trip):
    legs = [parseLeg(leg) for leg in tr['LegList']['Leg']]
    return {
        'legs': legs,
        'arrival': legs[-1]['destination']['dateTime']
    }

input = json.loads(sys.stdin.read())
origin = {
    'lat': input['olat'],
    'long': input['olong']
}
destination = {
    'lat': input['dlat'],
    'long': input['dlong']
}
data = retrieveData(origin, destination)
trip = sorted(
    [parseTrip(tr) for tr in data['Trip']],
    key=lambda tr: datetime.datetime.strptime(tr['arrival'], '%Y-%m-%d %H:%M:%S')
)[0]
print json.dumps(trip)