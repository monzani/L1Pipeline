#!/afs/slac/g/glast/isoc/flightOps/rhel3_gcc32/ISOC_PROD/bin/shisoc python2.5

"""@brief Make sure we are done processing a run/downlink.

@author W. Focke <focke@slac.stanford.edu>
"""

import os
import sys
import time

import fileNames
import lockFile
import pipeline

dlId = os.environ['DOWNLINK_ID']
runId = os.environ['RUNID']

files = fileNames.setup(dlId, runId)

rootDir = files['dirs']['run']

print >> sys.stderr, \
      "Attempting to remove lock from [%s] at [%s]" % (rootDir, time.ctime())
lockFile.unlockDir(rootDir, runId, dlId)

# Here we need to check that all the chunk locks (created by the halfpipe,
# removed by checkChunk) are gone,
# AND
# that some database somewhere says that the run is as complete as it will get
# before launching cleanup and updating run status in the data catalog.
#
# Details of how this will work have not been hashed out yet.

readyToRetire = True

if readyToRetire:
    stream = 0
    args = ''
    pipeline.createSubStream("cleanupCompleteRun", stream, args)
    pass

