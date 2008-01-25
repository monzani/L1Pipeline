#!/afs/slac/g/glast/isoc/flightOps/rhel3_gcc32/ISOC_PROD/bin/shisoc python2.5

"""@brief Setup reconstruction of a chunk.

@author W. Focke <focke@slac.stanford.edu>
"""

import math
import os
import sys

import config

import GPLinit

import crumble
import fileNames
import pipeline
import rootFiles
import stageFiles

status = 0

head, dlId = os.path.split(os.environ['DOWNLINK_RAWDIR'])
if not dlId: head, dlId = os.path.split(head)
runId = os.environ['RUNID']
chunkId = os.environ['CHUNK_ID']

staged = stageFiles.StageSet()
finishOption = config.finishOption

realDigiFile = fileNames.fileName('digi', dlId, runId, chunkId)
stagedDigiFile = staged.stageIn(realDigiFile)
realCrumbList = fileNames.fileName('crumbList', dlId, runId, chunkId)
stagedCrumbList = staged.stageOut(realCrumbList)

chunkEvents = rootFiles.getFileEvents(stagedDigiFile)
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

# write crumb list
open(stagedCrumbList, 'w').writelines(
    ('%s\n' % crumbId for crumbId in crumbIds))

for start, crumbId, nEvents in zip(crumbStarts, crumbIds, crumbSizes):
    stream = crumbId[1:]
    args = 'CRUMB_ID=%(crumbId)s,crumbStart=%(start)s,crumbEvents=%(nEvents)s' % locals()
    pipeline.createSubStream("doCrumb", stream, args)
    pass

if status: finishOption = 'wipe'
status |= staged.finish(finishOption)

sys.exit(status)
