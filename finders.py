
import glob
import os
import re
import sys

import fileNames


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


def findAndReadChunkLists(runId):
    dlId = '*'
    pattern = fileNames.fileName('chunkList', dlId, runId)
    print >> sys.stderr, 'Looking for files of form %s' % pattern
    chunkFiles = glob.glob(pattern)
    print >> sys.stderr, 'Found %s' % chunkFiles

    badChunkFiles = [fileNames.fileName('chunkList', badDl, runId) for badDl in os.environ.get('deliveriesToIgnore', '').split(':') if badDl]
    print >> sys.stderr, 'Ignoring %s' % badChunkFiles
    
    chunks = []
    for chunkFile in chunkFiles:
        if chunkFile in badChunkFiles:
            print >> sys.stderr, 'Skipping %s' % chunkFile
            continue
        these = fileNames.readList(chunkFile)
        # print >> sys.stderr, these
        chunks.extend(these.items())
        ids = sorted(this for this in these)
        print >> sys.stderr, '%s: %s' % (chunkFile, ids)
        continue
    return chunks


def allChunks(runDirs):
    chunks = dict((runId, findRunDirs(runDir))
                  for runId, runDir in runDirs.items())
    return chunks


def flatten(chunkTree):
    flat = dict(((runId, chunk), chunkFile)
                for runId, chunks in chunkTree.items()
                for chunk, chunkFile in chunks.items())
    return flat
