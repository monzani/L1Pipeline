#!/usr/bin/env python

"""@brief This should run after everything else in a chunk is done.
It removes the chunk lockfile that was placed ??somewhere?? by the
halfpipe.

@author W. Focke <focke@slac.stanford.edu>
"""


import os

import config
import fileNames
import lockFile

dlId = os.environ['DOWNLINK_ID']
runId = os.environ['RUNID']
chunkId = os.environ['CHUNK_ID']
files = fileNames.setup(dlId, runId, chunkId)

runDir = files['dirs']['run']
lockFile.removeLock(runDir, chunkId)
