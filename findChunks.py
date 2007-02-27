#!/usr/bin/env python

"""@brief Find new chunk files.

@author W. Focke <focke@slac.stanford.edu>
"""

import glob
import os

import config
import fileNames
import pipeline


dlId = os.environ['DOWNLINK_ID']
runId = os.environ['RUNID']
runDir = os.environ['RUN_RAWDIR']

files = fileNames.setup(dlId, runId)

rootDir = files['dirs']['run']

## Find chunk files
chunkPattern = os.path.join(runDir, '*.evt')
chunkFiles = glob.glob(chunkPattern)

# set up a subStream for each run
argList = []
for iChunk, chunkFile in enumerate(chunkFiles):

    chunkId = os.path.basename(chunkFile).split('_')[1]
    args = "EVTFILE=%(chunkFile)s,CHUNK_ID=%(chunkId)s" % locals()
    argList.append(args)
    continue


# Will this work?  Can't set variables that contain commas
# or colons?
allArgs = config.joiner.join(argList) 
#pipeline.setVariable('chunkList', allArgs)
