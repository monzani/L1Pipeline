#!/afs/slac/g/glast/isoc/flightOps/rhel3_gcc32/ISOC_PROD/bin/shisoc python2.5

"""@brief Filter merit file.

@author W. Focke <focke@slac.stanford.edu>
"""

import os
import sys

import config

import PipelineSummary
import rootFiles
import variables


def readCut(cutFile):
    lines = [line.strip() for line in open(cutFile) if not line.startswith('#')]
    assert len(lines) == 1
    return lines[0]


# def filterMerit(idArgs, files):
#     status = 0
#     tCut = readCut(config.ft1Cuts)
#     status |= rootFiles.filter(files['merit'],
#                                'MeritTuple',
#                                files['filteredMerit'],
#                                tCut)
#     metadata = {'sTCut': tCut}
#     #status |= variables.setVar('filteredMerit', 'metadata', repr(metadata)) # this chokes on nested quotes
#     summary = PipelineSummary.PipelineSummary("pipeline_summary")
#     name = variables.mangleName('filteredMerit', 'metadata')
#     summary.add(name, metadata)
#     summary.write()
#     return status


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
    tCut = readCut(config.cutFiles[outFileType])
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

