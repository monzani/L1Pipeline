#!/afs/slac/g/glast/isoc/flightOps/rhel3_gcc32/ISOC_PROD/bin/shisoc python2.5

"""@brief Find new chunk files.

@author W. Focke <focke@slac.stanford.edu>
"""

import sys
import glob
import os
import re

import config

import GPLinit

import fileNames
import lockFile
import pipeline
import stageFiles

status = 0

# recognize and parse a chunk
# this is a contract with the halfpipe
#chunkRe = re.compile('^(r[0-9]*)-(e[0-9]*)\.evt$')
chunkRe = re.compile('^(.[0-9]*)-(.[0-9]*)\.evt$')

head, dlId = os.path.split(os.environ['DOWNLINK_RAWDIR'])
if not dlId: head, dlId = os.path.split(head)
runId = os.environ['RUNID']
runDir = os.environ['RUN_RAWDIR']

staged = stageFiles.StageSet()
finishOption = config.finishOption

realChunkList = fileNames.fileName('chunkList', dlId, runId)
stagedChunkList = staged.stageOut(realChunkList)

subTask = config.chunkSubTask[os.environ['DATASOURCE']]

def findChunkFiles(runDir):
    # # Find chunk files
    # this is a contract with the halfpipe
    chunkGlob = os.path.join(runDir, '*.evt')
    print >> sys.stderr, 'Looking for files that match [%s].' % chunkGlob
    chunkFiles = glob.glob(chunkGlob)
    print >> sys.stderr, 'Found %s.' % chunkFiles

    # build a list of chunkIds
    goodChunks = {}
    for chunkFile in chunkFiles:
        fileBase = os.path.basename(chunkFile)
        match = chunkRe.match(fileBase)
        if match:
            runIdFromFile, chunkId = match.groups()
        else:
            print >> sys.stderr, 'Bad chunk file name %s' % fileBase
            continue
        goodChunks[chunkId] = chunkFile
        continue

    return goodChunks

goodChunks = findChunkFiles(runDir)
chunkIds = goodChunks.keys()
chunkIds.sort()

# Make chunkList
open(stagedChunkList, 'w').writelines(
    ('%s\n' % chunkId for chunkId in chunkIds))

# set up a subStream for each chunk
for chunkId, chunkFile in goodChunks.items():
    stream = chunkId[1:]
    args = "EVTFILE=%(chunkFile)s,CHUNK_ID=%(chunkId)s" % locals()
    pipeline.createSubStream(subTask, stream, args)
    continue

if status: finishOption = 'wipe'
status |= staged.finish(finishOption)

sys.exit(status)
