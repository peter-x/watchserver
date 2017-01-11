#!/usr/bin/env python

import caldav
from datetime import datetime, timedelta
import json
import math
import sys
import cgi

import keys

print 'Content-type: text/plain; charset=utf-8'
print 'Access-Control-Allow-Origin: *'
print

encryptedCred = keys.caldavCred

key = sys.stdin.read().strip().decode('base64')
cred = ''.join(chr(ord(x) ^ ord(y)) for (x, y) in zip(key, encryptedCred.decode('base64')))

try:
    credentials = json.loads(cred)
except:
    pass

if len(credentials) == 0:
    print '"Invalid credentials."'
    sys.exit(1)

output = []
for (username, password) in credentials:
    client = caldav.DAVClient(
        "http://localhost/owncloud/remote.php/dav",
        username = username,
        password = password,
        )
    for calendar in client.principal().calendars():
        for event in calendar.date_search(datetime.now(), datetime.now() + timedelta(hours=12)):
            if hasattr(event.instance, 'vcalendar'):
                events_ = event.instance.components()
            elif hasattr(event.instance, 'vevent'):
                events_ = [ event.instance.vevent ]
            else:
                raise Exception("Panic - invalid format")
            for event in events_:
                    dtstart = event.dtstart.value if hasattr(event, 'dtstart') else datetime.now()
                    if not isinstance(dtstart, datetime):
                        dtstart = datetime(dtstart.year, dtstart.month, dtstart.day)
                    summary = event.summary.value if hasattr(event, 'summary') else '-----'
                    duration = timedelta(hours = 24)
                    if hasattr(event, 'duration'):
                        duration = event.duration.value
                    elif hasattr(event, 'dtend'):
                        duration = event.dtend.value - event.dtstart.value
                    durationMinutes = max(1, int(math.ceil(duration.total_seconds() / 60)))
                    output.append([dtstart.isoformat(), durationMinutes])
json.dump(output, sys.stdout)
