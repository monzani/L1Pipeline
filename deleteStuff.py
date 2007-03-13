#!/usr/bin/env python

"""@brief Delete no-longer-needed files.

@author W. Focke <focke@slac.stanford.edu>
"""

import os
import sys

import fileNames

fileType = os.environ['fileType']
runId = os.environ['RUNID']

try:
    chunkId = os.environ['CHUNK_ID']
    dlId = os.environ['DOWNLINK_ID']
except KeyError:
    chunkId = None
    dlId = '*'
    pass

goners = fileNames.findPieces(fileType, dlId, runId, chunkId)

for goner in goners:
    #os.unlink(goner)
    print >> sys.stderr, '%s has left the building.' % goner
    continue
