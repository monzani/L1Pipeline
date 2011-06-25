#!/afs/slac/g/glast/isoc/flightOps/rhel3_gcc32/ISOC_PROD/bin/shisoc python2.5

"""@brief Filter merit file.

@author W. Focke <focke@slac.stanford.edu>
"""

import os
import sys

if __name__ == "__main__":
    print >> sys.stderr, "This module is not supported as main script"
    sys.exit(1)

import config

import PipelineSummary
import rootFiles
import variables


def readCut(cutFile):
    lines = [line.strip() for line in open(cutFile) if not line.startswith('#')]
    assert len(lines) == 1
    return lines[0]


def filterMerit(files, **extra):
    status = 0
    outFileType = 'filteredMerit'
    status |= _filter(files['merit'],
                      'MeritTuple',
                      files[outFileType],
                      outFileType)
    return status

def electronMerit(files, **extra):
    status = 0
    outFileType = 'electronMerit'
    status |= _filter(files['merit'],
                      'MeritTuple',
                      files[outFileType],
                      outFileType)
    return status


def _filter(inFile, treeName, outFile, outFileType):
    tCut = readCut(config.filterClassifyMap[outFileType]['cutFile'])
    logMsg = """Filtering:
    inFile: %(inFile)s
    outFile: %(outFile)s
    tCut: %(tCut)s""" % locals()
    print >> sys.stderr, logMsg
    status = 0
    status |= rootFiles.filter(inFile, treeName, outFile, tCut)
    metadata = {'sTCut': tCut}
    summary = PipelineSummary.PipelineSummary("pipeline_summary")
    name = variables.mangleName(outFileType, 'metadata')
    summary.add(name, metadata)
    summary.write()
    return status

