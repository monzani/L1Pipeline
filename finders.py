
import glob
import os
import re
import sys


def findRunDirs(dlRawDir):
    # Figure out which runs have data in this dl
    # we assume that any subdirectory of the downlink directory represents a run
    # this is a contract with the halfpipe
    maybeIds = os.listdir(dlRawDir)

    print >> sys.stderr, "Possible runs:[%s]" % maybeIds

    runDirs = {}
    for candidate in maybeIds:
        maybeDir = os.path.join(dlRawDir, candidate)
        if os.path.isdir(maybeDir):
            runDirs[candidate] = {'runDir': maybeDir}
            pass
        continue

    return runDirs


chunkRe = re.compile('^(.[0-9]+)-(.[0-9]+)\.evt$')
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
        goodChunks[chunkId] = {'chunkFile': chunkFile}
        continue

    return goodChunks


def allChunks(runDirs):
    chunks = dict((runId, findRunDirs(runDir))
                  for runId, runDir in runDirs.items())
    return chunks


def flatten(chunkTree):
    flat = dict(((runId, chunk), chunkFile)
                for runId, chunks in chunkTree.items()
                for chunk, chunkFile in chunks.items())
    return flat
