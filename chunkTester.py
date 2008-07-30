
import sys

import eventFile

def readHeader(inFile):
    reader = eventFile.LSEReader(inFile)
    start = reader.begGEM()
    stop = reader.endGEM()
    nEvt = reader.evtcnt()
    return start, stop, nEvt


def verifyChunk((start, stop, nEvt)):
    print >> sys.stderr, '  Checking chunk %s' % start
    if nEvt <= 1:
        print >> sys.stderr, 'Chunk %d has %d <= 1 events!' % (start, nEvt)
        return False
    nMax = stop - start + 1
    if nMax <= 0:
        print >> sys.stderr, 'Chunk %d goes backwards!' % (start)
        return False
    if nEvt > nMax:
        print >> sys.stderr, 'Chunk %s has too many events: %d > %d' % (start, nEvt, nMax)
        return False
    return True


def verifyList(chunks):
    print >> sys.stderr, 'Testing chunks...'
    chunks = [chunk[0] for chunk in sorted(chunks)]
    for chunk in chunks:
        if not verifyChunk(chunk): return False
        continue
    lastStart = chunks[0][0]
    lastStop = chunks[0][1]
    print >> sys.stderr, 'Checking for overlap...'
    for start, stop, nEvt in chunks[1:]:
        if start <= lastStop:
            print >> sys.stderr, 'Chunk %d overlaps %d!' % (start, lastStart)
            return False
        lastStart = start
        lastStop = stop
        continue
    print >> sys.stderr, 'OK'
    return True


def verifyFiles(inFiles):
    if not inFiles:
        print >> sys.stderr, 'No input data, cannot continue!'
        return False
    chunks = sorted((readHeader(inFile), inFile) for inFile in inFiles)
    print >> sys.stderr, r"""((start, stop, nEvents), 'fileName')"""
    for chunk in chunks: print >> sys.stderr, chunk
    return verifyList(chunks)
