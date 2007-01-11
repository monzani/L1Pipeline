"""@brief Run external programs.

@author W. Focke <focke@slac.stanford.edu>
"""

import os
import time

def run(cmd):
    print >> sys.stderr, time.localtime()
    print >> sys.stderr, "About to run [%s]" % cmd
    status = os.sytem(cmd)
    print >> sys.stderr, time.localtime()
    return status
