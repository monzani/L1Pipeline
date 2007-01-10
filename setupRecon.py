#!/usr/bin/env python

"""@brief Setup reconstruction of a chunk.

@author W. Focke <focke@slac.stanford.edu>
"""

import math
import os
env = os.environ
import sys

import crumble

import config

digiFile = env['digiChunkFile']
chunkDir = env['chunkDir']

chunkEvents = 85643

cDigits = int(math.ceil(math.log(chunkEvents) / math.log(10)))
cForm = '%0' + `cDigits` + 'd'

crumbSizes = crumble.crumble(chunkEvents, config.maxCrumbSize)
nCrumbs = len(crumbSizes)
crumbStarts = [0] * nCrumbs
for iCrumb in range(nCrumbs-1):
    crumbStarts[iCrumb+1] = crumbStarts[iCrumb] + crumbSizes[iCrumb]
    pass

for iCrumb in range(nCrumbs):
    start = crumbStarts[iCrumb]
    crumbId = cForm % start
    nEvents = crumbSizes[iCrumb]
    reconBase = '_'.join((env['RUNID'], env['chunkId'], crumbId,
                          env['DOWNLINK_ID'], 'RECON.root'))
    reconFile = os.path.join(chunkDir, reconBase)
    args = 'crumbStart=%(start)s,crumbEvents=%(nEvents)s,reconCrumbFile=%(reconFile)s' % locals()
    print >> sys.stderr, args
    #pipeline.createSubstream("doCrumb", iCrumb+1, args)
    pass
