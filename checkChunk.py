#!/afs/slac/g/glast/isoc/flightOps/rhel3_gcc32/ISOC_PROD/bin/shisoc python2.5

"""@brief This should run after everything else in a chunk is done.
It removes the chunk lockfile that was placed ??somewhere?? by the
halfpipe.

@author W. Focke <focke@slac.stanford.edu>
"""


import os
import sys

import config
import fileNames
import lockFile

status = 0

head, dlId = os.path.split(os.environ['DOWNLINK_RAWDIR'])
if not dlId: head, dlId = os.path.split(head)
runId = os.environ['RUNID']
chunkId = os.environ['CHUNK_ID']


# # This is probably not the right location for these locks.
# # They need to be put in a run-level (independent of downlink)
# # directory by the halfpipe.
# # The location has not yet been determined.
# # When it is, it will affect this process and checkRun
# runDir = files['dirs']['run']
# # This ain't the right code, either.
# lockFile.removeLock(runDir, chunkId)

# Remove event file? - No, that happens in cleanupDl.


token = fileNames.chunkToken(head, runId, chunkId)

if not os.path.exists(token):
    print >> sys.stderr, "Chunk token %s does not exist.  This is odd, but not necessarily fatal.  We'll continue." % token
    sys.exit(0)
    pass

print >> sys.stderr, 'Removing chunk token %s.' % token
try:
    os.unlink(token)
except OSError:
    print >> sys.stderr, "Can't remove chunk token %s.  Fail." % token
    status = 1
    pass

sys.exit(status)
