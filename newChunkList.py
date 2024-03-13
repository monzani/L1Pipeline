#!/sdf/data/fermi/a/isoc/flightOps/rhel6_gcc44/ISOC_PROD/bin/shisoc --add-env=flightops python2.6

"""
Generate new chunkLists to patch up halfpipe issues.
Argument is the fully-qualified path to a run delivery subdirectory (like /afs/slac.stanford.edu/g/glast/ground/PipelineStaging6/halfPipe/080723006/r0238495579).
Creates a chunkList in the current directory, with an appropriate name plus '.new' (like r0238495579_080723006_chunkList.txt.new).
"""

import glob
import os
import sys

import chunkTester
import fileNames
import finders

inDir = sys.argv[1]

chunks = finders.findChunkFiles(inDir)

for chunk in chunks.values():
    chunk['headerData'] = chunkTester.readHeader(chunk['chunkFile'])
    continue

head, runId = inDir, ''
while not runId:
    head, runId = os.path.split(head)
    continue
head, dlId = os.path.split(head)

outName = '_'.join([runId, dlId, 'chunkList.txt.new'])

print >> sys.stderr, 'Creating %s' % outName
# fileNames.writeListPickle(chunks, outName) # for old format
fileNames.writeList(chunks, outName)
