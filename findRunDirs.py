#!/afs/slac/g/glast/isoc/flightOps/rhel5_gcc41/ISOC_PROD/bin/shisoc --add-env=flightops python2.6

"""@brief Find new run directories.

@author W. Focke <focke@slac.stanford.edu>
"""

import os
import re
import sys
import time

import config

import GPLinit

import chunkTester
import fileNames
import finders
import glastTime
import lsf
import pipeline
import runner
import stageFiles


dlRawDir = os.environ['DOWNLINK_RAWDIR']

# VERYBAD!  Or maybe not.  Embrace it.
head, dlId = os.path.split(os.environ['DOWNLINK_RAWDIR'])
if not dlId: head, dlId = os.path.split(head)

staged = stageFiles.StageSet(excludeIn=config.excludeIn)

runDirs = finders.findRunDirs(dlRawDir)
dataRuns = set(runDirs)
print >> sys.stderr, "Presumed runs:[%s]" % dataRuns

print >> sys.stderr, 'Reading evt headers ...'
startTs = time.time()
chunkKeys = []
chunkLists = {}
for runId, runData in runDirs.items():
    print >> sys.stderr, runId
    hpRunDir = runData['runDir']
    chunkListData = finders.findChunkFiles(hpRunDir)
    print >> sys.stderr, chunkListData
    for chunk in chunkListData.values():
        print >> sys.stderr, chunk
        chunk['headerData'] = chunkTester.readHeader(chunk['chunkFile'])
        continue
    chunkKeys.extend((runId, chunkId) for chunkId in chunkListData)
    chunkLists[runId] = chunkListData
    continue
stopTs = time.time()
delta = stopTs - startTs
print >> sys.stderr, '%s s' % delta

for runId, chunkListData in chunkLists.items():
    realChunkList = fileNames.fileName('chunkList', dlId, runId)
    # temporarily mangle chunk list name to get around JIRA LONE-67    
    # mangledChunkList = fileNames.mangleChunkList(realChunkList)
    # stagedChunkList = staged.stageOut(mangledChunkList)
    stagedChunkList = staged.stageOut(realChunkList)
    fileNames.writeList(chunkListData, stagedChunkList)
    continue

runStatuses = dict.fromkeys(dataRuns, config.defaultRunStatus)

# the name of this file is a contract with the halfpipe
retireFile = os.path.join(dlRawDir, 'retired_runs_%s.txt' % dlId)
try:
    retireeStatus = dict(line.split() for line in open(retireFile))
except IOError:
    print >> sys.stderr, "Couldn't open run status file %s, all runs will have default status %s" % (retireFile, config.defaultRunStatus)
    retireeStatus = {}
    pass
retirees = set(retireeStatus)

print >> sys.stderr, "Retiring runs:[%s]" % retirees

runStatuses.update(retireeStatus)

oldRuns = retirees - dataRuns

print >> sys.stderr, "Old runs:[%s]" % oldRuns

# parse run type
deliveredEvents = {}
heldBackEvents = {}
dataSource = {}
# the name of this file is a contract with the halfpipe
deliveredFile = os.path.join(dlRawDir, 'delivered_events_%s.txt' % dlId)
try:
    dfp = open(deliveredFile)
    for line in dfp:
        runId, delivered, heldBack, source = line.split()
        deliveredEvents[runId] = int(delivered)
        heldBackEvents[runId] = int(heldBack)
        dataSource[runId] = source
        continue
    dfp.close()
except IOError:
    print >> sys.stderr, "Couldn't open delivered event file %s, all runs will have default dataSource %s" % (deliveredFile, config.defaultDataSource)
    pass

runNumRe = re.compile('([0-9]+)')
# create up a subStream for each run
for runId in dataRuns | oldRuns:
    source = dataSource.get(runId, config.defaultDataSource)

    mop = runNumRe.search(runId)
    if mop:
        nStr = mop.group(1)
    else:
        print >> sys.stderr, 'runId %s is malformed.' % runId
        nStr = runId[1:]
        pass
    runNumber = '%d' % int(nStr)
    stream = runNumber

    l1RunDir = fileNames.fileName(None, None, runId)

    runStatus = runStatuses[runId]
    if runStatus == "INCOMPLETE" and runId in dataRuns:
        newStatus = "WAITING"
        print >> sys.stderr, "%s has data, but status is %s, changing it to %s" % (runId, runStatus, newStatus)
        runStatus = newStatus
        pass
    
    subTask = config.runSubTask[runStatus][source]

    args = "RUNID=%(runId)s,runNumber=%(runNumber)s,RUNSTATUS=%(runStatus)s,DATASOURCE=%(source)s,runDir=%(l1RunDir)s" % locals()
    print >> sys.stderr, \
          "Creating stream [%s] of subtask [%s] with args [%s]" % \
          (stream, subTask, args)
    pipeline.createSubStream(subTask, stream, args)
    continue

staged.finish()
