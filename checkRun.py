#!/afs/slac/g/glast/isoc/flightOps/rhel3_gcc32/ISOC_PROD/bin/shisoc python2.5

"""@brief Make sure we are done processing a run/downlink.

@author W. Focke <focke@slac.stanford.edu>
"""

import os
import sys
import time

import config
import fileNames
import lockFile
import pipeline

head, dlId = os.path.split(os.environ['DOWNLINK_RAWDIR'])
if not dlId: head, dlId = os.path.split(head)
runId = os.environ['RUNID']

rootDir = os.path.dirname(fileNames.fileName('chunkList', dlId, runId)) #bleh

print >> sys.stderr, \
      "Attempting to remove lock from [%s] at [%s]" % (rootDir, time.ctime())
lockFile.unlockDir(rootDir, runId, dlId)

# Here we need to check that all the chunk locks (created by the halfpipe,
# removed by this script before now) are gone, AND that some database
# somewhere (GLAST_ISOC.ACQSUMMARY) says that the run is as complete as it
# will get, before launching cleanup and updating run status in the data
# catalog.
#
# but for now we punt
readyToRetire = False

subTask = config.cleanupSubTask[os.environ['DATASOURCE']]

if readyToRetire:
    stream = 0
    args = ''
    pipeline.createSubStream(subTask, stream, args)
    pass

