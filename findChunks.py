"""@brief Find new chunk files.

@author W. Focke <focke@slac.stanford.edu>
"""

# If this module crashes on import, locks will not be cleand up!

import os
import sys

if __name__ == "__main__":
    print >> sys.stderr, "This module is not supported as main script"
    sys.exit(1)

import config

import GPLinit

import acqQuery
import chunkTester
import ingestChunks
import fileNames
import finders
import lockFile
import pipeline
import runner


def cleanup(status, idArgs, **extra):
    if not status: return status
    myStatus = 0
    
    dlId, runId = idArgs[:2]
    runDir = fileNames.fileName(None, *idArgs)
    lockFile.unlockDir(runDir, runId, dlId)

    action = os.environ.get('l1LockAction', 'LockDirOnly')    
    if "Throttle" in action: lockFile.unlockThrottle(dlId, runId)

    return myStatus


def findChunks(idArgs, **extra):
    status = 0

    dlId, runId = idArgs[:2]

    realChunkList = fileNames.fileName('chunkList', *idArgs)

    # check that the chunks aren't crazy
    chunks = finders.findAndReadChunkLists(runId)
    chunkHeaders = [chunkData['headerData'] for chunkId, chunkData in chunks]
    testResult = chunkTester.verifyList(chunkHeaders)
    if not testResult:
        print >> sys.stderr, 'Run %s has bad crazy chunks.' % runId
        status |= 1
        return status
    tStart, tStop = testResult

    subTask = config.chunkSubTask[os.environ['DATASOURCE']]

    chunkListData = fileNames.readList(realChunkList)

    runNumber = int(os.environ['runNumber'])

    pipeline.setVariable('tStart', '%.17g' % tStart)
    pipeline.setVariable('tStop', '%.17g' % tStop)

    mootKey, mootAlias = acqQuery.query([runNumber], ['moot_key', 'moot_alias'])[runNumber]
    pipeline.setVariable('mootKey', mootKey)
    pipeline.setVariable('mootAlias', mootAlias)

    # set up a subStream for each chunk
    for chunkId, chunkData in chunkListData.items():
        stream = chunkId[1:]
        header = chunkData['headerData']
        chunkStart = header['begSec']
        chunkStop = header['endSec'] + 1 # values in header are truncated
        args = 'CHUNK_ID=%(chunkId)s,tStart=%(chunkStart).17g,tStop=%(chunkStop).17g' % locals()
        pipeline.createSubStream(subTask, stream, args)
        continue

    # ingest event files
    dlRawDir = os.environ.get('DOWNLINK_RAWDIR')
    hpRunDir = '%s/%s' % (dlRawDir, runId)
    ingestChunks.ingestChunks(hpRunDir, idArgs)

    return status
