#!/usr/bin/env python

"""@brief Find new run directories.

@author W. Focke <focke@slac.stanford.edu>
"""

import os

import pipeline

import config
import fileNames
import runner


dlId = os.environ['DOWNLINK_ID']
dlRawDir = os.environ['DOWNLINK_RAWDIR']

# Figure out which runs have data in this dl
maybeIds = os.listdir(dlRawDir)
maybeDirs = [os.path.join(dlRawDir, xx) for xx in maybeIds]
goodOnes = [iDir for iDir, runDir in enumerate(maybeDirs) if os.path.isdir(runDir)]

#files = fileNames.setup(dlId)
#runList = files['dirs']['runList']

# set up a subStream for each run
# Launch a subStream for each run
argSets = []
for iStream, iDir in enumerate(goodOnes):
    runId = maybeIds[iDir]
    runDir = maybeDirs[iDir]
    files = fileNames.setup(dlId, runId)
    rootDir = files['dirs']['run']
    args = "RUNID=%(runId)s,RUN_RAWDIR=%(runDir)s,RUN_ROOTDIR=%(rootDir)s" % \
           locals()
    pipeline.createSubstream("doRun", iStream+1, args)
