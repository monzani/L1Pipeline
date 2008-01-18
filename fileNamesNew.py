"""@brief Conventions for naming files.

@author W. Focke <focke@slac.stanford.edu>
"""

import glob
import hashlib
import os
import sys
import time

import config

import glastTime
import lockFile


fileTypes = {
    'cal': 'root',
    'chunkList': 'txt',
    'crumbList': 'txt',
    'digi': 'root',
    'digiEor': 'root',
    'digiTrend': 'root',
    'fastMonAlarm': 'xml',
    'fastMonError': 'xml',
    'fastMonHist': 'root',
    'fastMonTuple': 'root',
    'ft1': 'fits',
    'ft2': 'fits',
    'ft2Fake': 'fits',
    'ft2Txt': 'txt',
    'gcr': 'root',
    'ls3': 'fits',
    'merit': 'root',
    'recon': 'root',
    'reconEor': 'root',
    'reconTrend': 'root',
    'svac': 'root',
    'svacHist': 'root',
    }


def fileName(dsType, dlId, runId=None, chunkId=None, crumbId=None):

    dirs = []
    fields = []

    if runId is not None:
        dirs.extend([runId, config.L1Version])
        fields.append(runId)
        level = 'run'
        if chunkId is not None:
            dirs.append(chunkId)
            fields.append(chunkId)
            level = 'chunk'
            if crumbId is not None:
                dirs.append(crumbId)
                fields.append(crumbId)
                level = 'crumb'
                pass
            pass
        pass
    else:
        dirs.append(dlId)
        fields.append(dlId)
        level = 'downlink'
        pass
            
    if dsType in ['chunkList']:
        fields.append(dlId)
        pass

    if level == 'chunk': dirs.append(dsType)

    # file version goes here
    # replicate current behavior for now
    if level == 'run':
        baseDir = config.L1Dir
        runDir = os.path.join([baseDir] + dirs)
        try:
            lockData = lockFile.readLock(runDir, runId, dlId)
            version = glastTime.timeStamp(lockData['time'])
        except:
            print >> sys.stderr, "Problem reading lock from [%s]." % runDir
            version = dlId
            pass
        fields.append(version)
        pass

    fields.append(dsType)
    baseName = '.'.join(['_'.join(fields), fileTypes[dsType]])
    parts = dirs + [baseName]
    relativePath = os.path.join(*parts)

    if level != 'run':
        # temporary staging; load balance
        index = myHash(relativePath) % len(config.stageDirs)
        baseDir = config.stageDirs[index]
        pass

    fullName = os.path.join(baseDir, relativePath)

    return fullName


def myHash(str):
    return int(hashlib.md5(str).hexdigest(), 16)


def findPieces(fileType, dlId, runId, chunkId=None):
    """@brief find chunks or crumbs to merge.

    @arg fileType The type of file we're merging ('digi', 'reconMon', etc.)

    @arg dlId

    @arg runId

    @arg [chunkId]

    @return A sequence of file names
    """

    pieces = []
    if chunkId is None:
        # We are merging chunk files into a run file.
        # We have to find a file listing chunks for each downlink.
        dlId = '*'
        pattern = fileName('chunkList', dlId, runId)
        print >> sys.stderr, 'Looking for files of form %s' % pattern
        chunkFiles = glob.glob(pattern)
        chunkFiles.sort()
        print >> sys.stderr, 'Found %s' % chunkFiles
        for chunkFile in chunkFiles:
            these = []
            chunkIds = readList(chunkFile)
            for chunkId in chunkIds:
                these.append(fileName(fileType, dlId, runId, chunkId))
                continue
            print >> sys.stderr, '%s: %s' % (chunkFile, these)
            pieces.extend(these)
            continue
    else:
        # We are merging crumb files into chunk files.
        # We know the name of the file listing the crumbs.
        crumbFile = fileName('crumbList', dlId, runId, chunkId)
        crumbIds = readList(crumbFile)
        for crumbId in crumbIds:
            pieces.append(fileName(fileType, dlId, runId, chunkId, crumbId))
            continue
        pass

    return pieces


def readList(inFile):
    items = [line.strip().split()[0] for line in open(inFile)]
    items.sort()
    return items
