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

# Stage input digi even if it's on afs to avoid reading it multiple times.
staged = stageFiles.StageSet(excludeIn=None)
finishOption = config.finishOption

realDigiFile = fileNames.fileName('digi', dlId, runId, chunkId)
stagedDigiFile = staged.stageIn(realDigiFile)
realCrumbList = fileNames.fileName('crumbList', dlId, runId, chunkId)
stagedCrumbList = staged.stageOut(realCrumbList)

chunkEvents = rootFiles.getFileEvents(stagedDigiFile)
print >> sys.stderr, "Chunk has %d events." % chunkEvents

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
cForm = 'b%0' + `cDigits` + 'd'

crumbIds = [cForm % start for start in crumbStarts]

# write crumb list
#open(stagedCrumbList, 'w').writelines(
#    ('%s\n' % crumbId for crumbId in crumbIds))
crumbListData = dict((crumbId, {}) for crumbId in crumbIds)
fileNames.writeList(crumbListData, stagedCrumbList)

crumbData = []
for start, crumbId, nEvents in zip(crumbStarts, crumbIds, crumbSizes):
    digiCrumbFile = fileNames.fileName('digi', dlId, runId, chunkId, crumbId)
    stagedCrumbFile = staged.stageOut(digiCrumbFile)
    crumbData.append((stagedCrumbFile, nEvents, start))
    
    stream = crumbId[1:]
    args = 'CRUMB_ID=%(crumbId)s,crumbStart=%(start)s,crumbEvents=%(nEvents)s' % locals()
    pipeline.createSubStream("doCrumb", stream, args)
    continue

rootFiles.hSplit(stagedDigiFile, 'Digi', crumbData)

if status: finishOption = 'wipe'
status |= staged.finish(finishOption)

sys.exit(status)
