#!/afs/slac/g/glast/isoc/flightOps/rhel3_gcc32/ISOC_PROD/bin/shisoc python2.5

"""@brief Setup reconstruction of a chunk.

@author W. Focke <focke@slac.stanford.edu>
"""

import math
from os import path, environ
import sys

import config

import balance
import crumble
import fileNames
import pipeline
import rootFiles

dlId = environ['DOWNLINK_ID']
runId = environ['RUNID']
chunkId = environ['CHUNK_ID']

files = fileNames.setup(dlId, runId, chunkId)

digiFile = files['chunk']['digi']
chunkDir = files['dirs']['chunk']

chunkEvents = rootFiles.getFileEvents(digiFile)
print >> sys.stderr, "Chunk has %d events." % chunkEvents

crumbSizes = crumble.crumble(chunkEvents, config.maxCrumbSize)
nCrumbs = len(crumbSizes)
crumbStarts = [0] * nCrumbs
for iCrumb in range(nCrumbs-1):
    crumbStarts[iCrumb+1] = crumbStarts[iCrumb] + crumbSizes[iCrumb]
    pass

biggest = max(crumbStarts)

print >> sys.stderr, "biggest start = ", biggest, "nCrumbs = ", nCrumbs

if (nCrumbs == 1):
    cDigits = 1
else:
    cDigits = int(math.ceil(math.log(biggest) / math.log(10)))
cForm = 'b%0' + `cDigits` + 'd'

crumbIds = [cForm % start for start in crumbStarts]
balance.balance(crumbIds, runId, chunkId)

for start, crumbId, nEvents in zip(crumbStarts, crumbIds, crumbSizes):
    stream = crumbId[1:]
    args = 'CRUMB_ID=%(crumbId)s,crumbStart=%(start)s,crumbEvents=%(nEvents)s' % locals()
    pipeline.createSubStream("doCrumb", stream, args)
    pass
