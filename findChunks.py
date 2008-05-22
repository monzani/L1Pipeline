#!/afs/slac/g/glast/isoc/flightOps/rhel3_gcc32/ISOC_PROD/bin/shisoc python2.5

"""@brief Find new chunk files.

@author W. Focke <focke@slac.stanford.edu>
"""

import sys
import glob
import os
import re

import config

import GPLinit

import fileNames
import finders
import lockFile
import pipeline
import stageFiles

status = 0

head, dlId = os.path.split(os.environ['DOWNLINK_RAWDIR'])
if not dlId: head, dlId = os.path.split(head)
runId = os.environ['RUNID']

staged = stageFiles.StageSet()
finishOption = config.finishOption

realChunkList = fileNames.fileName('chunkList', dlId, runId)
stagedChunkList = staged.stageIn(realChunkList)

# Here we should put 'RUNNING' in Karen's run status table.

subTask = config.chunkSubTask[os.environ['DATASOURCE']]

chunkListData = fileNames.readList(stagedChunkList)

# set up a subStream for each chunk
for chunkId, chunkData in chunkListData.items():
    chunkFile = chunkData['chunkFile']
    hostList = chunkData['hostList']
    stream = chunkId[1:]
    args = 'EVTFILE=%(chunkFile)s,CHUNK_ID=%(chunkId)s,HOSTLIST="%(hostList)s"' % locals()
    pipeline.createSubStream(subTask, stream, args)
    continue

if status: finishOption = 'wipe'
status |= staged.finish(finishOption)

sys.exit(status)
