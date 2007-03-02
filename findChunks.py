#!/usr/bin/env python

"""@brief Find new chunk files.

@author W. Focke <focke@slac.stanford.edu>
"""

import glob
from os import path, environ

import config
import fileNames
import pipeline

dlId = environ['DOWNLINK_ID']
runId = environ['RUNID']
runDir = environ['RUN_RAWDIR']

glastExt=config.glastExt
LATCalibRoot=config.LATCalibRoot

files = fileNames.setup(dlId, runId)

rootDir = files['dirs']['run']

## Find chunk files
chunkPattern = path.join(runDir, '*.evt')
chunkFiles = glob.glob(chunkPattern)

# set up a subStream for each run
argList = []
for iChunk, chunkFile in enumerate(chunkFiles):

    chunkId = path.basename(chunkFile).split('_')[1]
    args = "EVTFILE=%(chunkFile)s,CHUNK_ID=%(chunkId)s,GLAST_EXT=%(glastExt)s,LATCalibRoot=%(LATCalibRoot)s" % locals()
    argList.append(args)
    continue


# Will this work?  Can't set variables that contain commas
# or colons?
allArgs = config.joiner.join(argList) 
pipeline.setVariable('chunkList', allArgs)
