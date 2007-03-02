#!/usr/bin/env python

"""@brief Setup reconstruction of a chunk.

@author W. Focke <focke@slac.stanford.edu>
"""

from os import path, environ
import math

import config
import fileNames
import crumble
import pipeline

files = fileNames.setup(environ['DOWNLINK_ID'], environ['RUNID'], \
                        environ['CHUNK_ID'])

digiFile = files['chunk']['digi']
chunkDir = files['dirs']['chunk']

chunkEvents = 85643

cDigits = int(math.ceil(math.log(chunkEvents) / math.log(10)))
cForm = '%0' + `cDigits` + 'd'

crumbSizes = crumble.crumble(chunkEvents, config.maxCrumbSize)
nCrumbs = len(crumbSizes)
crumbStarts = [0] * nCrumbs
for iCrumb in range(nCrumbs-1):
    crumbStarts[iCrumb+1] = crumbStarts[iCrumb] + crumbSizes[iCrumb]
    pass

argList = []
for iCrumb in range(nCrumbs):
    start = crumbStarts[iCrumb]
    crumbId = cForm % start
    nEvents = crumbSizes[iCrumb]
#    reconBase = '_'.join((environ['RUNID'], environ['CHUNK_ID'], crumbId,
#                          environ['DOWNLINK_ID'], 'RECON.root'))
#    reconFile = path.join(chunkDir, reconBase)
    args = 'CRUMB_ID=%(crumbId)s,crumbStart=%(start)s,crumbEvents=%(nEvents)s' % locals()
    argList.append(args)
    pass

# Will this work?  Can't set variables that contain commas
# or colons?
allArgs = config.joiner.join(argList) 
pipeline.setVariable('crumbList', allArgs)
