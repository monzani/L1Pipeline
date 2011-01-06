
import sys

import config

import GPLinit

import fileNames
import fileOps
import finders

defOutFileType = 'event'

def ingestChunk(inFile, idArgs, outFileType=None):
    if outFileType is None: outFileType = defOutFileType
    outFile = fileNames.fileName(outFileType, *idArgs)
    rc = fileOps.copy(inFile, outFile)
    if rc:
        print >> sys.stderr, "Copy didn't work, removing target file %s" % outFile
        fileOps.remove(outFile)
    else:
        print >> sys.stderr, "Copy worked, removing source file %s" % inFile
        fileOps.remove(inFile)
    return rc

def ingestChunks(hpRunDir, idArgs):
    dlId, runId = idArgs[:2]
    chunkListData = finders.findChunkFiles(hpRunDir)
    for chunkId, chunk in chunkListData.items():
        chunkArgs = (dlId, runId, chunkId, None)
        chunkFile = chunk['chunkFile']
        ingestChunk(chunkFile, chunkArgs)
        continue
    return
