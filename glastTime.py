"""@brief Deal with GLAST-related concepts of time.

@todo Figure out time zones

@todo Figure out leap seconds

"""

import calendar
import time

tsFormat = 't%.10d'

met0 = calendar.timegm(time.strptime('Jan 1 00:00:00 2001 UTC', '%b %d %H:%M:%S %Y %Z'))

def met(unixTime=None):
    if unixTime is None: unixTime = time.time()
    rv = unixTime - met0
    return rv

def timeStamp(unixTime=None):
    val = int(met(unixTime))
    stamp = tsFormat % val
    return stamp

