"""@brief Conventions for naming files.

@author W. Focke <focke@slac.stanford.edu>
"""

import bisect
import cPickle
import glob
import hashlib
import math
import os
import random
import re
import sys
import time

import config

import finders
import variables

fileTypes = {
    'acdPlots': 'tar',
    'acdPedsAlarm': 'xml',
    'acdPedsAnalyzer': 'root',
    'cal': 'root',
    'calGainsAlarm': 'xml',
    'calGainsAnalyzer': 'root',
    'calHist': 'root',
    'calHistAlarm': 'xml',
    'calPedsAlarm': 'xml',
    'calPedsAnalyzer': 'root',
    'calTrend': 'root',
    'chunkList': 'txt',
    'compareDFm': 'xml',
    'crumbList': 'txt',
    'digi': 'root',
    'digiHist': 'root',
    'digiHistAlarm': 'xml',
    'digiTrend': 'root',
    'digiTrendAlarm': 'xml',
    'fastMonError': 'xml',
    'fastMonErrorAlarm': 'xml',
    'fastMonHist': 'root',
    'fastMonHistAlarm': 'xml',
    'fastMonTrend': 'root',
    'fastMonTrendAlarm': 'xml',
    'fastMonTuple': 'root',
    'ft1': 'fit',
    'ft1BadGti': 'fit',
    'ft1NoDiffRsp': 'fit',
    'ft2': 'fit',
    'ft2Seconds': 'fit',
    'ft2Fake': 'fit',
    'ft2Txt': 'txt',
    'gcr': 'root',
    'ls1': 'fit',
    'ls1BadGti': 'fit',
    'ls3': 'fit',
    'magic7Hp': 'txt',
    'magic7L1': 'txt',
    'merit': 'root',
    'meritHist': 'root',
    'meritHistAlarm': 'xml',
    'meritTrend': 'root',
    'meritTrendAlarm': 'xml',
    'recon': 'root',
    'reconHist': 'root',
    'reconHistAlarm': 'xml',
    'reconHistAlarmDist': 'root',
    'reconTrend': 'root',
    'reconTrendAlarm': 'xml',
    'svac': 'root',
    'svacHist': 'root',
    'timeSpan': 'txt',
    'tkrAlarm': 'xml',
    'tkrAnalysis': 'root',
    'tkrMonitor': 'root',
    'tkrReport': 'tar',
    'tkrTrend': 'root',
    'tkrTrendAlarm': 'xml',
    'verifyLog': 'xml',
    'verifyHisto': 'root',
    'verifyErrorAlarm': 'xml',
    }

exportTags = { # files exported to FSSC use a different naming rule
    'ft1': 'gll_ph',
    'ft2': 'gll_pt',
    'ls1': 'gll_ev',
    'ls3': 'gll_lt',
    }

xrootFileTypes = ['fit', 'root'] # these will be stored in xroot instead of nfs


stageDirs = [os.path.join(disk, config.stageBase)
             for disk, weight in config.stageDisks
             for ii in range(weight)]
uniqueStageDirs = set(stageDirs)

mergeLockBase = 'dontCleanUp' # lock file for merge errors
def mergeLockName(runId):
    runDir = fileName(None, None, runId)
    lockName = os.path.join(runDir, mergeLockBase)
    return lockName
def makeMergeLock(runId):
    cleanupLock = mergeLockName(runId)
    print >> sys.stderr, 'Trying to create %s ... ' % cleanupLock,
    if os.path.exists(cleanupLock):
        print >> sys.stderr, 'already there.'
    else:
        fp = open(cleanupLock, 'w')
        fp.close()
        print >> sys.stderr, 'OK'
        pass
    return
def checkMergeLock(runId):
    cleanupLock = mergeLockName(runId)
    print >> sys.stderr, 'Checking for %s ... ' % cleanupLock,
    if os.path.exists(cleanupLock):
        print >> sys.stderr, 'yep.'
        return cleanupLock
    else:
        print >> sys.stderr, 'nope.'
        return False
    return


def dataCatGroup(fileType):
    dsType = fileType.upper()
    return dsType

def dataCatFolder(fileType):
    dsType = dataCatGroup(fileType)
    folder = '/'.join([config.dataCatDir, dsType])
    return folder

def dataCatName(fileType, fileName):
    folder = dataCatFolder(fileType)
    junk, baseName = os.path.split(fileName)
    name = ':'.join([folder, baseName])
    return name

sites = ['SLAC', 'SLAC_XROOT']
def getSite(fileName):
    site = sites[fileName.startswith('root:')]    
    return site

def fileName(fileType, dlId, runId=None, chunkId=None, crumbId=None, next=False):

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

    subDir = subDirectory(fileType, dlId, runId, chunkId, crumbId)
    
    if level == 'run':
        runDir = os.path.join(config.L1Dir, subDir)

        if fileType is None:
            return runDir
        
        if fileTypes[fileType] in xrootFileTypes:
            subDir = xrootSubDirectory(fileType, dlId, runId)
            baseDir = config.xrootBase
        else:
            baseDir = config.L1Dir
            pass

        
        if fileType in ['chunkList']:
            verStr = dlId
        else:
            verNum = int(variables.getVar(fileType, 'ver'))
            if next:
                verNum += 1
                pass
            verStr = 'v%03d' % verNum
            if fileType in ['magic7Hp']:
                verStr = '_'.join([dlId, verStr])
                pass
            pass
        fields.append(verStr)
        pass

    if fileType in exportTags:
        tag = exportTags[fileType]
        pos = 0
    else:
        tag = fileType
        pos = len(fields)
        pass
    fields.insert(pos, tag)

    baseName = '.'.join(['_'.join(fields), fileTypes[fileType]])
    relativePath = os.path.join(subDir, baseName)

    if level != 'run':
        # temporary staging; load balance
        #index = myHash(relativePath) % len(config.stageDirs)
        #baseDir = config.stageDirs[index]
        baseDir = stageBalance(relativePath)
        pass

    fullName = os.path.join(baseDir, relativePath)

    return fullName


def myHash(str):
    hasher = hashlib.md5(str)
    digest = hasher.hexdigest()
    hash = int(digest, 16)
    return hash

def stageBalance(str):
    index = myHash(str) % len(stageDirs)
    baseDir = stageDirs[index]
    return baseDir


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
        if fileType is None:
            # Just finding run buffers to delete
            argSets = [(fileType, dlId, runId, chunkId)]
        else:
            # We are merging chunk files into a run file.
            # We have to find a file listing chunks for each downlink.
            #
            allChunks = finders.findAndReadChunkLists(runId)
            chunkIds = [chunkData[0] for chunkData in allChunks]
            chunkIds.sort()
            argSets = [(fileType, dlId, runId, chunkId)
                       for chunkId in chunkIds]
            pass
        pass
    else:
        # We are either merging crumb files into chunk files or
        # deleting crumb directories.
        # We know the name of the file listing the crumbs.
        crumbFile = fileName('crumbList', dlId, runId, chunkId)
        crumbIds = readList(crumbFile).keys()
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
                  for baseDir in uniqueStageDirs]
        pass

    return pieces


def writeListPickle(data, outFile):
    cPickle.dump(data, open(outFile, 'w'))
    return

def readListPickle(inFile):
    return cPickle.load(open(inFile))

def writeListRepr(data, outFile):
    open(outFile, 'w').write(repr(data))
    return

def readListRepr(inFile):
    return eval(open(inFile).read())

def readListCombo(inFile):
    try:
        data = readListPickle(inFile)
    except cPickle.UnpicklingError:
        data = readListRepr(inFile)
    return data

readList = readListCombo
writeList = writeListRepr


def subDirectory(fileType, dlId, runId=None, chunkId=None, crumbId=None):

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

    if level in ['crumb', 'chunk'] and fileType is not None:
        dirs.append(fileType)
        pass

    dirName = os.path.join(*dirs)
    
    return dirName

def xrootSubDirectory(fileType, dlId, runId=None):
    subDir = fileType
    return subDir


versRe = re.compile('_v([0-9]+)[\._][^/]+$')
def version(fileName):
    mob = versRe.search(os.path.basename(fileName))
    if mob:
        vers = int(mob.group(1))
    else:
        raise ValueError, "Can't parse version from %s" % fileName
    return vers


def tokenDir(dlHead, runId):
    tokenDirName = os.path.join(dlHead, 'chunktokens', runId)
    return tokenDirName

def chunkToken(dlHead, runId, chunkId):
    tokenDirName = tokenDir(dlHead, runId)
    token = os.path.join(tokenDirName, '-'.join([runId, chunkId]))
    return token


def mangleChunkList(realName):
    # mangle chunk list name to get around JIRA LONE-67
    mangledName = realName + '.tmp'
    return mangledName


def preMakeDirs(dirs, dlId, runId=None, chunkId=None, crumbId=None):
    import stageFiles
    buffers = list(uniqueStageDirs)
    random.shuffle(buffers)
    mid = subDirectory(None, dlId, runId, chunkId, crumbId)
    allDirs = [os.path.join(buf, mid, sub) for buf in buffers for sub in dirs]
    print >> sys.stderr, 'Creating directories %s ... ' % allDirs,
    start = time.time()
    for dir in allDirs: stageFiles.makedirs(dir)
    stop = time.time()
    print >> sys.stderr, '%g s.' % (stop - start)
    return



defaultMinMultiplicity = 1280
defaultNameCopies = 320
big = 2 ** (16*8) # specific to MD5

class consistentHash(object):

    def __init__(self, slots, minMultiplicity=None, nameCopies=None):
        """
        @arg slots A sequence of (item, name, weight)
                   Item can be anything, it's what is returned on a lookup.
                   Name is a string. They have to be all different.
                   Weight is a number.
        """
        if minMultiplicity is None: minMultiplicity = defaultMinMultiplicity
        if nameCopies is None: nameCopies = defaultNameCopies
        
        # allWeights = [float(weight) for item, name, weight in slots]
        # minWeight = min(allWeights)

        table = []
        for item, name, weight in slots:
            # multiplicity = int(math.ceil(weight / minWeight * minMultiplicity)) # bad idea
            multiplicity = int(math.ceil(weight * minMultiplicity))
            base = name * nameCopies
            table.extend([(myHash(base + ':%d' % copy), item) for copy in range(multiplicity)])
            continue
        table.sort()
        # put a copy of the first entry at the end to handle wraparound
        firstKey, firstItem = table[0]
        wrapKey = big + firstKey
        table.append((wrapKey, firstItem))

        self.keys, self.items = zip(*table)

        return


    def lookup(self, item):
        key = myHash(item)
        pos = bisect.bisect_left(self.keys, key)
        try:
            slot = self.items[pos]
        except:
            print pos, len(self.items), key, self.keys[-1]
        return slot

    pass
