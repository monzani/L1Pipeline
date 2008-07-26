"""@brief Conventions for naming files.

@author W. Focke <focke@slac.stanford.edu>
"""

import cPickle
import glob
import hashlib
import os
import re
import sys

import config

import variables

fileTypes = {
    'acdPlots': 'tar',
    'acdPedsAnalyzer': 'root',
    'cal': 'root',
    'calHist': 'root',
    'calGainsAnalyzer': 'root',
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
    'fastMonHist': 'root',
    'fastMonHistAlarm': 'xml',
    'fastMonTrend': 'root',
    'fastMonTrendAlarm': 'xml',
    'fastMonTuple': 'root',
    'ft1': 'fit',
    'ft2': 'fit',
    'ft2Fake': 'fit',
    'ft2Txt': 'txt',
    'gcr': 'root',
    'ls1': 'fit',
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
    }

exportTags = {
    'ft1': 'gll_ph',
    'ft2': 'gll_pt',
    'ls1': 'gll_ev',
    'ls3': 'gll_lt',
    }

xrootFileTypes = ['fit', 'root']


stageDirs = [os.path.join(disk, config.stageBase)
             for disk, weight in config.stageDisks
             for ii in range(weight)]
uniqueStageDirs = set(stageDirs)

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
    return int(hashlib.md5(str).hexdigest(), 16)

def stageBalance(str):
    index = myHash(str) % len(stageDirs)
    baseDir = stageDirs[index]
    return baseDir


def findAndReadChunkLists(runId):
    dlId = '*'
    pattern = fileName('chunkList', dlId, runId)
    print >> sys.stderr, 'Looking for files of form %s' % pattern
    chunkFiles = glob.glob(pattern)
    print >> sys.stderr, 'Found %s' % chunkFiles
    chunks = []
    for chunkFile in chunkFiles:
        these = readList(chunkFile)
        print these
        chunks.extend(these.items())
        ids = sorted(this for this in these)
        print >> sys.stderr, '%s: %s' % (chunkFile, ids)
        continue
    return chunks


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
            # Should use findAndReadChunkLists here
            dlId = '*'
            pattern = fileName('chunkList', dlId, runId)
            print >> sys.stderr, 'Looking for files of form %s' % pattern
            chunkFiles = glob.glob(pattern)
            print >> sys.stderr, 'Found %s' % chunkFiles
            chunkIds = []
            for chunkFile in chunkFiles:
                these = readList(chunkFile).keys()
                chunkIds.extend(these)
                print >> sys.stderr, '%s: %s' % (chunkFile, these)
                continue
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
