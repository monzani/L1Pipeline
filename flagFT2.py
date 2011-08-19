#!/afs/slac/g/glast/isoc/flightOps/rhel4_gcc34/ISOC_PROD/bin/shisoc python2.5

import sys

if __name__ == "__main__":
    print >> sys.stderr, "This module is not supported as main script"
    sys.exit(1)

import calendar
import os
import re
import time

import pyfits as pf

import config

import fileOps

import fileNames
import parseBTI
import pipeline
import registerPrep
import runner

#os.environ['PFILES'] = '/afs/slac.stanford.edu/u/ek/focke/pfiles;/afs/slac/g/glast/applications/astroTools/headas/i686-pc-linux-gnu-libc2.2.4/syspfiles'

dlId = 'dl'
chunkId = None
crumbId = None


getRanges = parseBTI.getRangesVar
setRanges = parseBTI.setRangesVar


def flagFT2(files, idArgs, outFileTypes, runDir, staged, workDir, **args):
    status = 0

    # figure out the output files
    # we have to do this here because genricScript (which handled the inputs)
    # is not set up to handle input and output files of the same type
    #
    #
    # Actually, no. They don't have the same type anymore.
    #
    # But usually, there will be no interval to flag, and we'd rather not
    # stage in inputs that we don't need.
    #
    # But since we're now comitted to 2 different file types, we've got to
    # copy the input to the output even if there are no BTIs.
    #
    # So I think that means just use the normal mechanism?
    # But then how do we match up the names?
    #
    outFiles = {}
    tmpFiles = {}
    hduLists = {}
    headers = {}
    data = {}
    versions = {}
    for outFileType in outFileTypes:
        inFileType = outFileType + 'NoQual'
        inFile = files[inFileType]

        stagedOutFile = files[outFileType]
        outFiles[outFileType] = stagedOutFile
        versions[outFileType] = fileNames.version(stagedOutFile)
        
        tmpFile = stagedOutFile + '.tmp'
        tmpFiles[outFileType] = tmpFile

        hduList = pf.open(inFile)
        hduLists[outFileType] = hduList
        headers[outFileType] = hduList[0].header
        data[outFileType] = hduList[1].data
        continue

    ranges = getRanges()
    newRanges = []
    for range in ranges:
        newRange = baddify(data, range)
        newRanges.append(newRange)
        continue

    for outFileType in outFileTypes:
        hduList = hduLists[outFileType]
        header = headers[outFileType]
        tmpFile = tmpFiles[outFileType]
        outFile = outFiles[outFileType]
        outBase = os.path.basename(outFile)
        version = versions[outFileType]

        header['FILENAME'] = outBase
        header['VERSION'] = version

        hduList.writeto(tmpFile)
        hduList.close()

        sumCmd = """HOME=%s
        source %s
        fchecksum infile=%s update=yes datasum=yes""" % \
                 (workDir, config.astroTools, tmpFile)
        status |= runner.run(sumCmd)

        os.rename(tmpFile, outFile)
        continue

    setRanges(newRanges)
 
    return status
   

def baddify(data, initialRange):
    print >> sys.stderr, initialRange
    newRange = badRange(data['ft2'], initialRange)
    print >> sys.stderr, newRange
    range1 = badRange(data['ft2Seconds'], newRange)
    print >> sys.stderr, range1
    if range1 != newRange:
        raise ValueError, "1-second ranges did not correctly aggregate to 30-second ranges!"
    return range1


def badRange(tab, ((iStart, iStop), newQual)):
    fStart = 9e9
    fStop = 0e0

    colStart = tab.field('START')
    colStop = tab.field('STOP')

    minCol = min(colStart)
    maxCol = max(colStop)
    if minCol > iStop or maxCol < iStart:
         raise ValueError, "These don't overlap! (%s %s) (%s %s)" % (minCol, maxCol, iStart, iStop)
    
    quality = tab.field('DATA_QUAL')
    for bin, (binStart, binStop) in enumerate(zip(colStart, colStop)):
        if not (binStart >= iStop or binStop <= iStart):
            quality[bin] = newQual
            if binStart < fStart: fStart = binStart
            if binStop > fStop: fStop = binStop
            pass
        continue
    return (fStart, fStop), newQual


