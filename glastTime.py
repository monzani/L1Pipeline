"""@brief Deal with GLAST-related concepts of time.

@todo Figure out time zones

@todo Figure out leap seconds

"""

import time

met0 = time.mktime(time.strptime('Jan 1 00:00:00 2001', '%b %d %H:%M:%S %Y'))

def met(unixTime=None):
    if unixTime is None: unixTime = time.time()
    rv = unixTime - met0
    return rv

