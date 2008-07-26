
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
    delta = stop - start
    if delta < 0:
        print >> sys.stderr, 'Chunk %d goes backwards!' % (start)
        return False
    dp1 = delta + 1
    if nEvt > dp1:
        print >> sys.stderr, 'Chunk %s has too many events: %d > %d' % (start, nEvt, dp1)
        return False
    return True


def verifyList(chunks):
    print >> sys.stderr, 'Testing chunks...'
    chunks = sorted(chunks)
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
    chunks = [readHeader(inFile) for inFile in inFiles]
    return verifyList(chunks)
