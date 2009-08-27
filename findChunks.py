#!/afs/slac/g/glast/isoc/flightOps/rhel3_gcc32/ISOC_PROD/bin/shisoc --add-env=oracle11 --add-env=flightops python2.5

"""@brief Find new chunk files.

@author W. Focke <focke@slac.stanford.edu>
"""

import os
import sys

import config

import GPLinit

import acqQuery
import chunkTester
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
    lockFile.unlockThrottle(dlId, runId)

    realChunkList = fileNames.fileName('chunkList', *idArgs)
    mangledChunkList = fileNames.mangleChunkList(realChunkList)
    cmd = 'mv %s %s' % (realChunkList, mangledChunkList)
    myStatus |= runner.run(cmd)
    
    return myStatus


def findChunks(idArgs, **extra):
    status = 0

    dlId, runId = idArgs[:2]

    realChunkList = fileNames.fileName('chunkList', *idArgs)
    # unmangle chunk list name to get around JIRA LONE-67
    mangledChunkList = fileNames.mangleChunkList(realChunkList)
    cmd = 'mv %s %s' % (mangledChunkList, realChunkList)
    status |= runner.run(cmd)

    # check that the chunks aren't crazy
    chunks = finders.findAndReadChunkLists(runId)
    chunkHeaders = [chunkData['headerData'] for chunkId, chunkData in chunks]
    if not chunkTester.verifyList(chunkHeaders):
        print >> sys.stderr, 'Run %s has bad crazy chunks.' % runId
        status |= 1
        cleanup(status, idArgs)
        sys.exit(status)
        pass

    subTask = config.chunkSubTask[os.environ['DATASOURCE']]

    chunkListData = fileNames.readList(realChunkList)

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
        stream = chunkId[1:]
        header = chunkData['headerData']
        chunkStart = header['begSec']
        chunkStop = header['endSec']
        args = 'EVTFILE=%(chunkFile)s,CHUNK_ID=%(chunkId)s,tStart=%(chunkStart).17g,tStop=%(chunkStop).17g' % locals()
        pipeline.createSubStream(subTask, stream, args)
        continue
    
    chunkIds = chunkListData.keys()
    fileNames.preMakeDirs(chunkIds, dlId, runId)

    return status
