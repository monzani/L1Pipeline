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

dataRuns = set()
runDirs = {}
for candidate in maybeIds:
    maybeDir = os.path.join(dlRawDir, candidate)
    if os.path.isdir(maybeDir):
        dataRuns.add(candidate)
        runDirs[candidate] = maybeDir
        pass
    continue
runStatuses = dict.fromkeys(dataRuns, 'WAITING')

# the name of this file is a contract with the halfpipe
retireFile = os.path.join(dlRawDir, 'retired_runs.txt')
retireeStatus = dict([line.split() for line in open(retireFile)])
retirees = set(retireeStatus.keys())

runStatuses.update(retireeStatus)

oldRuns = retirees - dataRuns

# create up a subStream for each data run
for stream, runId in enumerate(dataRuns):
    runDir = runDirs[runId]
    runStatus = runStatuses[runId]
    args = "RUNID=%(runId)s,RUN_RAWDIR=%(runDir)s,RUNSTATUS=%(runStatus)s,DOWNLINK_ID=%(dlId)s" % locals()
    pipeline.createSubStream("doRun", stream, args)
    stream += 1
    continue

# and for each old run
for stream, runId in enumerate(oldRuns):
    runStatus = runStatuses[runId]
    args = "RUNID=%(runId)s,RUNSTATUS=%(runStatus)s" % locals()
    pipeline.createSubStream("cleanupIncompleteRun", stream, args)
    stream += 1
    continue
