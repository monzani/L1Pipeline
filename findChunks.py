#!/afs/slac/g/glast/isoc/flightOps/rhel3_gcc32/ISOC_PROD/bin/shisoc --add-env=oracle11 python2.5

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

staged = stageFiles.StageSet()
finishOption = config.finishOption

realChunkList = fileNames.fileName('chunkList', dlId, runId)
# unmangle chunk list name to get around JIRA LONE-67
mangledChunkList = fileNames.mangleChunkList(realChunkList)
cmd = 'mv %s %s' % (mangledChunkList, realChunkList)
runner.run(cmd)
stagedChunkList = staged.stageIn(realChunkList)

subTask = config.chunkSubTask[os.environ['DATASOURCE']]

chunkListData = fileNames.readList(stagedChunkList)

# get current tStart, tStop to override the bogus values set by findRunDirs
runNumber = int(os.environ['runNumber'])
tStart, tStop = acqQuery.runTimes(runNumber)
pipeline.setVariable('tStart', tStart)
pipeline.setVariable('tStop', tStop)

# set up a subStream for each chunk
for chunkId, chunkData in chunkListData.items():
    chunkFile = chunkData['chunkFile']
    hostList = chunkData['hostList']
    stream = chunkId[1:]
    args = 'EVTFILE=%(chunkFile)s,CHUNK_ID=%(chunkId)s,HOSTLIST="%(hostList)s",tStart=%(tStart).17g,tStop=%(tStop).17g' % locals()
    pipeline.createSubStream(subTask, stream, args)
    continue

if status: finishOption = 'wipe'
status |= staged.finish(finishOption)

sys.exit(status)
