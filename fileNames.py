"""@brief Conventions for naming files.

@author W. Focke <focke@slac.stanford.edu>
"""

import glob
import hashlib
import os
import re
import sys

import config


fileTypes = {
    'cal': 'root',
    'calEor': 'root',
    'calTrend': 'root',
    'chunkList': 'txt',
    'crumbList': 'txt',
    'digi': 'root',
    'digiEor': 'root',
    'digiTrend': 'root',
    'fastMonError': 'xml',
    'fastMonHist': 'root',
    'fastMonHistAlarm': 'xml',
    'fastMonTuple': 'root',
    'ft1': 'fit',
    'ft2': 'fit',
    'ft2Fake': 'fit',
    'ft2Txt': 'txt',
    'gcr': 'root',
    'ls1': 'fit',
    'ls3': 'fit',
    'merit': 'root',
    'recon': 'root',
    'reconEor': 'root',
    'reconTrend': 'root',
    'svac': 'root',
    'svacHist': 'root',
    }

exportTags = {
    'ft1': 'gll_ph',
    'ft2': 'gll_pt',
    'ls1': 'gll_ev',
    'ls3': 'gll_lt',
    }


def fileName(dsType, dlId, runId=None, chunkId=None, crumbId=None, next=False):

    fields = []

    if runId is not None:
        level = 'run'
        fields.append(runId)
        if chunkId is not None:
            level = 'chunk'
            fields.append(chunkId)
            if crumbId is not None:
                level = 'crumb'
                fields.append(crumbId)
                pass
            pass
        pass
    else:
        level = 'downlink'
        fields.append(dlId)
        pass

    subDir = subDirectory(dsType, dlId, runId, chunkId, crumbId)
    
    if level == 'run':
        baseDir = config.L1Dir
        runDir = os.path.join(baseDir, subDir)

        if dsType in ['chunkList']:
            verStr = dlId
        else:
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            # This will not work without the global run lock!
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            #
            # And it blows for so many reasons on top of that.
            # Replace with something based on the filess that are
            # already present.
            #
            versionFile = os.path.join(runDir, dsType+'.version')
            print >> sys.stderr, 'Trying to read version from %s' % versionFile
            try:
                verNum = int(open(versionFile).readline().strip())
                print >> sys.stderr, 'Read %d' % verNum
            except IOError:
                if next:
                    print >> sys.stderr, 'First version'
                    verNum = -1
                else:
                    print >> sys.stderr, """
                    Drat.
                    We really should not be here.
                    Someone promised that there would be a version file, but it ain't there.
                    Maybe the caller forgot to specify 'next=True'?
                    Or the file got deleted?
                    """
                    raise
                pass
            if next:
                verNum += 1
                print >> sys.stderr, 'Writing new version %d to %s' % \
                      (verNum, versionFile)
                open(versionFile, 'w').write('%d\n' % verNum)
                pass
            verStr = 'v%03d' % verNum
            pass
        fields.append(verStr)
        pass

    if dsType in exportTags:
        tag = exportTags[dsType]
        pos = 0
    else:
        tag = dsType
        pos = len(fields)
        pass
    fields.insert(pos, tag)

    baseName = '.'.join(['_'.join(fields), fileTypes[dsType]])
    relativePath = os.path.join(subDir, baseName)

    if level != 'run':
        # temporary staging; load balance
        index = myHash(relativePath) % len(config.stageDirs)
        baseDir = config.stageDirs[index]
        pass

    fullName = os.path.join(baseDir, relativePath)

    return fullName


def myHash(str):
    return int(hashlib.md5(str).hexdigest(), 16)


def findPieces(fileType, dlId, runId=None, chunkId=None):
    """@brief find chunks or crumbs to merge.

    @arg fileType The type of file we're merging ('digi', 'reconMon', etc.)
    If this is None, will return a list of directories.

    @arg dlId

    @arg runId

    @arg [chunkId]

    @return A sequence of file names
    """

    if runId is None:
        # We're not merging anything, just finding downlink dirs to delete.
        argSets = [(fileType, dlId)]
    elif chunkId is None:
        # We are merging chunk files into a run file.
        # We have to find a file listing chunks for each downlink.
        dlId = '*'
        pattern = fileName('chunkList', dlId, runId)
        print >> sys.stderr, 'Looking for files of form %s' % pattern
        chunkFiles = glob.glob(pattern)
        print >> sys.stderr, 'Found %s' % chunkFiles
        chunkIds = []
        for chunkFile in chunkFiles:
            these = readList(chunkFile)
            chunkIds.extend(these)
            print >> sys.stderr, '%s: %s' % (chunkFile, these)
            continue
        chunkIds.sort()
        argSets = [(fileType, dlId, runId, chunkId)
                   for chunkId in chunkIds]
    else:
        # We are either merging crumb files into chunk files or
        # deleting crumb directories.
        # We know the name of the file listing the crumbs.
        crumbFile = fileName('crumbList', dlId, runId, chunkId)
        crumbIds = readList(crumbFile)
        crumbIds.sort()
        argSets = [(fileType, dlId, runId, chunkId, crumbId)
                   for crumbId in crumbIds]
        pass
    
    if fileType is None:
        funk = subDirectory
    else:
        funk = fileName
        pass

    pieces = [funk(*args) for args in argSets]

    if fileType is None:
        pieces = [os.path.join(baseDir, piece)
                  for piece in pieces
                  for baseDir in config.stageDirs]
        pass

    return pieces


def readList(inFile):
    items = [line.strip().split()[0] for line in open(inFile)]
    return items


def subDirectory(dsType, dlId, runId=None, chunkId=None, crumbId=None):

    dirs = []

    if runId is not None:
        level = 'run'
        # dirs.extend([runId, config.L1Version])
        dirs.extend([runId])
        if chunkId is not None:
            level = 'chunk'
            dirs.append(chunkId)
            if crumbId is not None:
                level = 'crumb'
                dirs.append(crumbId)
                pass
            pass
        pass
    else:
        level = 'downlink'
        dirs.extend(['downlinks', dlId])
        pass

    if level in ['chunk'] and dsType is not None:
        dirs.append(dsType)
        pass

    dirName = os.path.join(*dirs)
    
    return dirName


versRe = re.compile('_v([0-9]+)[\._][^/]+$')
def version(fileName):
    mob = versRe.search(os.path.basename(fileName))
    if mob:
        vers = int(mob.group(1))
    else:
        raise ValueError, "Can't parse version from %s" % fileName
    return vers
