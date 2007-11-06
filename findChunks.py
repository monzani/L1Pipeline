#!/afs/slac/g/glast/isoc/flightOps/rhel3_gcc32/ISOC_PROD/bin/shisoc python2.5

"""@brief Find new chunk files.

@author W. Focke <focke@slac.stanford.edu>
"""

import sys
import glob
import os
import re

import config
import fileNames
import lockFile
import pipeline

# recognize and parse a chunk
# this is a contract with the halfpipe
#chunkRe = re.compile('^(r[0-9]*)-(e[0-9]*)\.evt$')
chunkRe = re.compile('^(.[0-9]*)-(.[0-9]*)\.evt$')

dlId = os.environ['DOWNLINK_ID']
runId = os.environ['RUNID']
runDir = os.environ['RUN_RAWDIR']

files = fileNames.setup(dlId, runId)

rootDir = files['dirs']['run']

subTask = config.chunkSubTask[os.environ['DATASOURCE']]

## Find chunk files
# this is a contract with the halfpipe
chunkGlob = os.path.join(runDir, '*.evt')
print >> sys.stderr, 'Looking for files that match [%s].' % chunkGlob
chunkFiles = glob.glob(chunkGlob)
print >> sys.stderr, 'Found %s.' % chunkFiles

# set up a subStream for each run
for chunkFile in chunkFiles:

    fileBase = os.path.basename(chunkFile)
    match = chunkRe.match(fileBase)
    if match:
        runIdFromFile, chunkId = match.groups()
    else:
        print >> sys.stderr, 'Bad chunk file name %s' % fileBase
        continue
    stream = chunkId[1:]
    args = "EVTFILE=%(chunkFile)s,CHUNK_ID=%(chunkId)s" % locals()
    pipeline.createSubStream(subTask, stream, args)
    continue
