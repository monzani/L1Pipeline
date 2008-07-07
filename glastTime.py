"""@brief Deal with GLAST-related concepts of time.

@todo Figure out time zones

@todo Figure out leap seconds

"""

import calendar
import datetime
import time

tsFormat = 't%.10d'

met0 = calendar.timegm(time.strptime('Jan 1 00:00:00 2001 UTC', '%b %d %H:%M:%S %Y %Z')) # unix time at MET 0


iso8860Fmt = '%Y-%m-%d %H:%M:%S'

dtMet0 = datetime.datetime(2001, 1, 1, 0, 0, 0, 0) # datetime for MET 0

def met(unixTime=None):
    if unixTime is None: unixTime = time.time()
    rv = unixTime - met0
    return rv

def timeStamp(unixTime=None):
    val = int(met(unixTime))
    stamp = tsFormat % val
    return stamp

def dt2Met(dtIn):
    delta = dtIn - dtMet0
    met = delta.microseconds / 1e6 + delta.seconds + delta.days * 86400
    return met

def met2Iso8860(met):
    unixTime = met + met0
    st = time.gmtime(unixTime)
    iso = time.strftime(iso8860Fmt, st)
    return iso
