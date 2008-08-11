
import os
import sys

import eventFile

def readHeader(inFile):
    print >> sys.stderr, 'Reading %s ...' % inFile
    headerData = {}
    headerData['name'] = os.path.basename(inFile)
    reader = eventFile.LSEReader(inFile)
    headerData['begGEM'] = reader.begGEM()
    headerData['endGEM'] = reader.endGEM()
    headerData['nEvt'] = reader.evtcnt()
    headerData['begSec'] = reader.begSec()
    headerData['endSec'] = reader.endSec()
    print >> sys.stderr, headerData
    return headerData


def verifyChunk(headerData):
    begGEM = headerData['begGEM']
    print >> sys.stderr, '  Checking chunk %s ...' % begGEM,

    nEvt = headerData['nEvt']
    endGEM = headerData['endGEM']
    begSec = headerData['begSec']
    endSec = headerData['endSec']

    if nEvt <= 1:
        print >> sys.stderr, 'chunk has %d <= 1 events!' % nEvt
        return False

    nMax = endGEM - begGEM + 1
    if nMax <= 0:
        print >> sys.stderr, 'events go backwards!'
        return False

    if nEvt > nMax:
        print >> sys.stderr, 'chunk has too many events: %d > %d' % (nEvt, nMax)
        return False
    
    if begSec > endSec:
        print >> sys.stderr, 'times go backwards!'
        return False

    print >> sys.stderr, 'OK'
    return True


def verifyList(chunks):
    print >> sys.stderr, 'Testing chunks...'

    byGEM = sorted(chunks, key=lambda x:x['begGEM'])
    for chunk in byGEM:
        if not verifyChunk(chunk): return False
        continue

    print >> sys.stderr, 'Testing ordering...'
    bySec = sorted(chunks, key=lambda x:x['begSec'])
    if bySec != byGEM:
        print >> sys.stderr, 'Sort by time != sort by gemId!'
        return False
    byName = sorted(chunks, key=lambda x:x['name'])
    if byName != byGEM:
        print >> sys.stderr, 'Sort by name != sort by gemId!'
        return False

    print >> sys.stderr, 'Checking for gemId overlap...'
    lastStart = byGEM[0]['begGEM']
    lastStop = byGEM[0]['endGEM']
    for chunk in byGEM[1:]:
        begGEM = chunk['begGEM']
        endGEM = chunk['endGEM']
        if begGEM <= lastStop:
            print >> sys.stderr, 'Chunk %d overlaps %d!' % (begGEM, lastStart)
            return False
        lastStart = begGEM
        lastStop = endGEM
        continue

    print >> sys.stderr, 'Checking for time overlap...'
    lastGEM = bySec[0]['begGEM']
    lastStart = bySec[0]['begSec']
    lastStop = bySec[0]['endSec']
    for chunk in bySec[1:]:
        begGEM = chunk['begGEM']
        begSec = chunk['begSec']
        endSec = chunk['endSec']
        if begSec < lastStop:
            print >> sys.stderr, 'Chunk %d overlaps %d!' % (begGEM, lastGEM)
            return False
        lastGEM = begGEM
        lastStart = begSec
        lastStop = endSec
        continue

    print >> sys.stderr, 'OK'
    return True


