#!/afs/slac/g/glast/isoc/flightOps/rhel3_gcc32/ISOC_PROD/bin/shisoc python2.5

"""@brief Find new run directories.

@author W. Focke <focke@slac.stanford.edu>
"""

import os
import re
import sys

import config

import fileNames
import glastTime
import pipeline
import runner


dlId = os.environ['DOWNLINK_ID']
dlRawDir = os.environ['DOWNLINK_RAWDIR']

# VERYBAD!
head, downlink = os.path.split(os.environ['DOWNLINK_RAWDIR'])
if not downlink: head, downlink = os.path.split(head)

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
runStatuses = dict.fromkeys(dataRuns, config.defaultRunStatus)

print >> sys.stderr, "Presumed runs:[%s]" % dataRuns

# the name of this file is a contract with the halfpipe
retireFile = os.path.join(dlRawDir, 'retired_runs_%s.txt' % downlink)
try:
    retireeStatus = dict(line.split() for line in open(retireFile))
except IOError:
    print >> sys.stderr, "Couldn't open run status file %s, all runs will have default status %s" % (retireFile, config.defaultRunStatus)
    retireeStatus = {}
    pass
retirees = set(retireeStatus.keys())

print >> sys.stderr, "Retiring runs:[%s]" % retirees

runStatuses.update(retireeStatus)

oldRuns = retirees - dataRuns

print >> sys.stderr, "Old runs:[%s]" % oldRuns

# bogus placeholder start and stop times
# Should get from acqsummary DB table
tStartDef = 100000001.0
tStopDef = 300000001.0
start = {}
stop = {}
boundaryFile = os.path.join(dlRawDir, 'event_times_%s.txt' % downlink)
try:
    lines = open(boundaryFile)
except IOError:
    print >> sys.stderr, "Couldn't open run bouncray file %s" % boundaryFile
    lines = []
    pass
for line in lines:
    runId, tStart, tStop = line.strip().split()
    start[runId] = glastTime.met(float(tStart))
    stop[runId] = glastTime.met(float(tStop))
    continue

runNumRe = re.compile('([0-9]+)')

# create up a subStream for each data run
subTask = "doRun"
for runId in dataRuns:
    mop = runNumRe.search(runId)
    if mop:
        nStr = mop.group(1)
    else:
        print >> sys.stderr, 'runId %s is malformed.' % runId
        nStr = runId[1:]
        pass
    runNumber = '%d' % int(nStr)
    stream = runNumber
    runDir = runDirs[runId]
    runStatus = runStatuses[runId]
    try:
        tStart = start[runId]
        tStop = stop[runId]
    except KeyError:
        tStart = tStartDef
        tStop = tStopDef
        print >> sys.stderr, "Couldn't get tStart, tStop for run %s, using bogus values" % runId
        pass
    args = "RUNID=%(runId)s,runNumber=%(runNumber)s,RUN_RAWDIR=%(runDir)s,RUNSTATUS=%(runStatus)s,DOWNLINK_ID=%(dlId)s,tStart=%(tStart).17g,tStop=%(tStop).17g" % locals()
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
