#!/afs/slac/g/glast/isoc/flightOps/rhel3_gcc32/ISOC_PROD/bin/shisoc --add-env=oracle11 --add-env=flightops python2.5

"""@brief Find new chunk files.

@author W. Focke <focke@slac.stanford.edu>
"""

import sys
import glob
import os
import re

import config

import GPLinit

import acqQuery
import chunkTester
import fileNames
import finders
import lockFile
import pipeline
import runner
import stageFiles

status = 0

head, dlId = os.path.split(os.environ['DOWNLINK_RAWDIR'])
if not dlId: head, dlId = os.path.split(head)
runId = os.environ['RUNID']

realChunkList = fileNames.fileName('chunkList', dlId, runId)
# unmangle chunk list name to get around JIRA LONE-67
mangledChunkList = fileNames.mangleChunkList(realChunkList)
cmd = 'mv %s %s' % (mangledChunkList, realChunkList)
runner.run(cmd)

# check that the chunks aren't crazy
chunks = finders.findAndReadChunkLists(runId)
chunkHeaders = [chunkData['headerData'] for chunkId, chunkData in chunks]
if not chunkTester.verifyList(chunkHeaders):
    print >> sys.stderr, 'Run %s has bad crazy chunks.' % runId
    sys.exit(1)
    pass

staged = stageFiles.StageSet(excludeIn=config.excludeIn)
finishOption = config.finishOption

stagedChunkList = staged.stageIn(realChunkList)

subTask = config.chunkSubTask[os.environ['DATASOURCE']]

chunkListData = fileNames.readList(stagedChunkList)

# get current tStart, tStop to override the bogus values set by findRunDirs
runNumber = int(os.environ['runNumber'])
tStart, tStop = acqQuery.runTimes(runNumber)
pipeline.setVariable('tStart', '%.17g' % tStart)
pipeline.setVariable('tStop', '%.17g' % tStop)

mootKey, mootAlias = acqQuery.query([runNumber], ['moot_key', 'moot_alias'])[runNumber]
pipeline.setVariable('mootKey', mootKey)
pipeline.setVariable('mootAlias', mootAlias)

# set up a subStream for each chunk
for chunkId, chunkData in chunkListData.items():
    chunkFile = chunkData['chunkFile']
    hostList = chunkData['hostList']
    stream = chunkId[1:]
    header = chunkData['headerData']
    chunkStart = header['begSec']
    chunkStop = header['endSec']
    args = 'EVTFILE=%(chunkFile)s,CHUNK_ID=%(chunkId)s,HOSTLIST="%(hostList)s",tStart=%(chunkStart).17g,tStop=%(chunkStop).17g' % locals()
    pipeline.createSubStream(subTask, stream, args)
    continue

chunkIds = chunkListData.keys()
fileNames.preMakeDirs(chunkIds, dlId, runId)

if status: finishOption = 'wipe'
status |= staged.finish(finishOption)

sys.exit(status)
