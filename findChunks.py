#!/usr/bin/env python

"""@brief Find new chunk files.

@author W. Focke <focke@slac.stanford.edu>
"""

import sys
import glob
from os import path, environ
import re

import config
import fileNames
import pipeline

# recognize and parse a chunk
# this is a contract with the halfpipe
#chunkRe = re.compile('^(r[0-9]*)-(e[0-9]*)\.evt$')
chunkRe = re.compile('^(.[0-9]*)-(.[0-9]*)\.evt$')

dlId = environ['DOWNLINK_ID']
runId = environ['RUNID']
runDir = environ['RUN_RAWDIR']

files = fileNames.setup(dlId, runId)

rootDir = files['dirs']['run']

## Find chunk files
# this is a contract with the halfpipe
chunkGlob = path.join(runDir, '*.evt')
chunkFiles = glob.glob(chunkGlob)

# set up a subStream for each run
for chunkFile in chunkFiles:

    fileBase = path.basename(chunkFile)
    match = chunkRe.match(fileBase)
    if match:
        runIdFromFile, chunkId = match.groups()
    else:
        print >> sys.stderr, 'Bad chunk file name %s' % fileBase
        continue
    stream = chunkId[1:]
    args = "EVTFILE=%(chunkFile)s,CHUNK_ID=%(chunkId)s" % locals()
    pipeline.createSubStream("doChunk", stream, args)
    continue
