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


def filterMerit(idArgs, files):
    status = 0
    tCut = readCut(config.ft1Cuts)
    status |= rootFiles.filter(files['merit'],
                               'MeritTuple',
                               files['filteredMerit'],
                               tCut)
    metadata = {'sTCut': tCut}
    #status |= variables.setVar('filteredMerit', 'metadata', repr(metadata)) # this chokes on nested quotes
    summary = PipelineSummary.PipelineSummary("pipeline_summary")
    name = variables.mangleName('filteredMerit', 'metadata')
    summary.add(name, metadata)
    summary.write()
    return status

