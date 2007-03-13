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
# we assume that any subdirectory of the downlink directory represents a run
# this is a contract with the halfpipe
maybeIds = os.listdir(dlRawDir)
maybeDirs = [os.path.join(dlRawDir, xx) for xx in maybeIds]
goodOnes = [iDir for iDir, runDir in enumerate(maybeDirs) if os.path.isdir(runDir)]

# files = fileNames.setup(dlId)

# set up a subStream for each run
for iRun, iDir in enumerate(goodOnes):
    runId = maybeIds[iDir]
    runDir = maybeDirs[iDir]
    args = "RUNID=%(runId)s,RUN_RAWDIR=%(runDir)s,DOWNLINK_ID=%(dlId)s" % \
           locals()
    pipeline.createSubStream("doRun",iRun,args)
    continue
