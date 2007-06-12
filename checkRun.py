#!/usr/bin/env python

"""@brief Make sure we are done processing a run/downlink.

@author W. Focke <focke@slac.stanford.edu>
"""

import os

import fileNames
import lockFile
import pipeline

dlId = environ['DOWNLINK_ID']
runId = environ['RUNID']

files = fileNames.setup(dlId, runId)

rootDir = files['dirs']['run']

lockFile.unlockDir(rootDir, runId, dlId)

# Here we need to check that all the chunk locks (created by the halfpipe,
# removed by checkChunk) are gone,
# AND
# that some database somewhere says that the run is as complete as it will get
# before launching cleanup and updating run status in the data catalog.
#
# Details of how this will work have not been hashed out yet.

readyToRetire = False

if readyToRetire:
    stream = 0
    args = ''
    pipeline.createSubStream("cleanupCompleteRun", stream, args)
    pass

