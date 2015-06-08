#!/afs/slac/g/glast/isoc/flightOps/rhel5_gcc41/ISOC_PROD/bin/shisoc python2.6

"""@brief Setup reconstruction of a chunk.

@author W. Focke <focke@slac.stanford.edu>
"""

import math
import os
import sys

import config

import crumble
import fileNames
import pipeline
import rootFiles
import variables


def setupCrumbs(files, idArgs, staged, piVersion, **args):

    status = 0
    
    digiCrumbVersion = piVersion
    digiVersionName = variables.mangleName('digi', 'ver')
    stagedDigiFile = files['digi']

    ft2FakeVersion = variables.getVar('ft2Fake', 'ver')
    ft2FakeVersionName = variables.mangleName('ft2Fake', 'ver')
    
    chunkEvents = rootFiles.getFileEvents(stagedDigiFile)
    print >> sys.stderr, "Chunk has %d events." % chunkEvents
    if chunkEvents < 1: return 1

    crumbSizes = crumble.crumble(chunkEvents)
    nCrumbs = len(crumbSizes)
    crumbStarts = [0] * nCrumbs
    for iCrumb in range(nCrumbs-1):
        crumbStarts[iCrumb+1] = crumbStarts[iCrumb] + crumbSizes[iCrumb]
        continue

    biggest = max(crumbStarts)

    print >> sys.stderr, "biggest start = ", biggest, "nCrumbs = ", nCrumbs

    if (nCrumbs == 1):
        cDigits = 1
    else:
        cDigits = int(math.ceil(math.log(biggest) / math.log(10)))
        pass
    cForm = 'b%0' + `cDigits` + 'd'

    crumbIds = [cForm % start for start in crumbStarts]

    # put crumb list in a variable
    crumbVar = os.sep.join(crumbIds)
    pipeline.setVariable('L1_crumb_list', crumbVar)

    crumbData = []
    for start, crumbId, nEvents in zip(crumbStarts, crumbIds, crumbSizes):
        crumbIdArgs = list(idArgs)
        crumbIdArgs[-1] = crumbId
        digiCrumbFile = fileNames.fileName('digi', version=digiCrumbVersion,
                                           *crumbIdArgs)
        stagedCrumbFile = staged.stageOut(digiCrumbFile)
        crumbData.append((stagedCrumbFile, nEvents, start))
    
        stream = crumbId[1:]
        streamArgs = 'CRUMB_ID=%(crumbId)s,crumbStart=%(start)s,crumbEvents=%(nEvents)s,%(digiVersionName)s=%(digiCrumbVersion)s,%(ft2FakeVersionName)s=%(ft2FakeVersion)s' % locals()
        pipeline.createSubStream("doCrumb", stream, streamArgs)
        continue

    rootFiles.hSplit(stagedDigiFile, 'Digi', crumbData)

    return status

