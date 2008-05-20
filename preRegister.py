#!/afs/slac/g/glast/isoc/flightOps/rhel3_gcc32/ISOC_PROD/bin/shisoc python2.5

"""@brief Prepare to register a file.

@author W. Focke <focke@slac.stanford.edu>
"""

import os
import sys

import config

import GPLinit

import fileNames
import registerPrep


head, dlId = os.path.split(os.environ['DOWNLINK_RAWDIR'])
if not dlId: head, dlId = os.path.split(head)
runId = os.environ['RUNID']
chunkId = os.environ.get('CHUNK_ID')
crumbId = os.environ.get('CRUMB_ID')

fileType = os.environ.get('fileType')

theFile = fileNames.fileName(fileType, dlId, runId, chunkId, crumbId)

registerPrep.prep(fileType, theFile)

sys.exit(0)
