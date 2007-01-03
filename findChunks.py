#!/usr/bin/env python

"""@brief Find new chunk files.

@author W. Focke <focke@slac.stanford.edu>
"""

import glob
import os

import pipeline

import config


dlId = os.environ['DOWNLINK_ID']
runId = os.environ['RUNID']
runDir = os.environ['RUN_RAWDIR']
rootDir = os.environ['RUN_ROOTDIR']

# Find chunk files
chunkPattern = os.path.join(runDir, '*.evt')
chunkFiles = glob.glob(chunkPattern)

# Launch a subStream for each run
for iChunk, chunkFile in enumerate(chunkFiles):
    args = "EVTFILE=%(chunkFile)s" % locals()
    pipeline.createSubstream("doChunk", iChunk+1, args)
