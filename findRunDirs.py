#!/afs/slac/g/glast/isoc/flightOps/rhel3_gcc32/ISOC_PROD/bin/shisoc python2.5

"""@brief Find new run directories.

@author W. Focke <focke@slac.stanford.edu>
"""

import os
import sys

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

print >> sys.stderr, "Possible runs:[%s]" % maybeIds

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

print >> sys.stderr, "Presumed runs:[%s]" % dataRuns

# the name of this file is a contract with the halfpipe
retireFile = os.path.join(dlRawDir, 'retired_runs.txt')
try:
    retireeStatus = dict([line.split() for line in open(retireFile)])
except IOError:
    retireeStatus = {}
    pass
retirees = set(retireeStatus.keys())

print >> sys.stderr, "Retiring runs:[%s]" % retirees

runStatuses.update(retireeStatus)

oldRuns = retirees - dataRuns

print >> sys.stderr, "Old runs:[%s]" % oldRuns

# create up a subStream for each data run
subTask = "doRun"
for runId in dataRuns:
    stream = runId[1:]
    runDir = runDirs[runId]
    runStatus = runStatuses[runId]
    args = "RUNID=%(runId)s,RUN_RAWDIR=%(runDir)s,RUNSTATUS=%(runStatus)s,DOWNLINK_ID=%(dlId)s" % locals()
    print >> sys.stderr, \
          "Creating stream [%s] of subtask [%s] with args [%s]" % \
          (stream, subTask, args)
    pipeline.createSubStream(subTask, stream, args)
    continue

# and for each old run
subTask = "cleanupIncompleteRun"
for runId in oldRuns:
    stream = runId[1:]
    runStatus = runStatuses[runId]
    args = "RUNID=%(runId)s,RUNSTATUS=%(runStatus)s" % locals()
    print >> sys.stderr, \
          "Creating stream [%s] of subtask [%s] with args [%s]" % \
          (stream, subTask, args)
    pipeline.createSubStream(subTask, stream, args)
    continue
