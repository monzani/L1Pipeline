"""@brief Conventions for naming files.

@author W. Focke <focke@slac.stanford.edu>
"""

import bisect
import cPickle
import glob
import math
import os
import random
import re
import sys
import time

import config

try:
    import fileOps
except ImportError:
    print >> sys.stderr, "Couldn't import fileOps. This is normal when installing, but may cause trouble otherwise."
    pass

import finders
import variables

fileTypes = {
    None: None,
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
    'digiGap': 'txt',
    'digiHist': 'root',
    'digiHistAlarm': 'xml',
    'digiTrend': 'root',
    'digiTrendAlarm': 'xml',
    'electronFT1': 'fit',
    'electronFT1BadGti': 'fit',
    'electronMerit': 'root',
    'event': 'evt',
    'extendedFT1': 'fit',
    'extendedLS1': 'fit',
    'fastMonError': 'xml',
    'fastMonErrorAlarm': 'xml',
    'fastMonHist': 'root',
    'fastMonHistAlarm': 'xml',
    'fastMonTrend': 'root',
    'fastMonTrendAlarm': 'xml',
    'fastMonTuple': 'root',
    'filteredMerit': 'root',
    'ft1': 'fit',
    'ft1BadGti': 'fit',
    'ft1NoDiffRsp': 'fit',
    'ft2': 'fit',
    'ft2NoQual': 'fit',
    'ft2Seconds': 'fit',
    'ft2SecondsNoQual': 'fit',
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
    'orbitPlot': 'png',
    'recon': 'root',
    'reconHist': 'root',
    'reconHistAlarm': 'xml',
    'reconHistAlarmDist': 'root',
    'reconTrend': 'root',
    'reconTrendAlarm': 'xml',
    'solarFlareHist': 'root',
    'solarFlareLog': 'xml',
    'solarFlarePlot': 'png',
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
    'verifyFt1Error': 'xml',
    'verifyFt1ErrorAlarm': 'xml',
    'verifyFt2Error': 'xml',
    'verifyFt2ErrorAlarm': 'xml',
    'verifyMeritError': 'xml',
    'verifyMeritErrorAlarm': 'xml',
    }

elFt1PTag = '_p%03d' % config.elFt1ProcVer
exFt1PTag = '_p%03d' % config.exFt1ProcVer
exLs1PTag = '_p%03d' % config.exLs1ProcVer
ft1PTag = '_p%03d' % config.ft1ProcVer
ft2PTag = '_p%03d' % config.ft2ProcVer
ls1PTag = '_p%03d' % config.ls1ProcVer
exportTags = { # files exported to FSSC use a different naming rule
    'electronFT1': 'gll_el' + elFt1PTag,
    'extendedFT1': 'gll_xp' + exFt1PTag,
    'extendedLS1': 'gll_xe' + exLs1PTag,
    'ft1': 'gll_ph' + ft1PTag,
    'ft2': 'gll_pt' + ft2PTag,
    'ls1': 'gll_ev' + ls1PTag,
    'ls3': 'gll_lt',
    }

xrootFileTypes = ['fit', 'root'] # these will be stored in xroot instead of nfs


mergeLockBase = 'dontCleanUp' # lock file for merge errors
def mergeLockName(runId):
    runDir = fileName(None, None, runId)
    lockName = os.path.join(runDir, mergeLockBase)
    return lockName
def makeMergeLock(runId, content=''):
    cleanupLock = mergeLockName(runId)
    print >> sys.stderr, 'Trying to append to %s ... ' % cleanupLock,
    fp = open(cleanupLock, 'a')
    fp.write(content)
    fp.close()
    print >> sys.stderr, 'OK'
    return
def checkMergeLock(runId):
    cleanupLock = mergeLockName(runId)
    print >> sys.stderr, 'Checking for %s ... ' % cleanupLock,
    if os.path.exists(cleanupLock):
        print >> sys.stderr, 'yep.'
        fp = open(cleanupLock)
        print >> sys.stderr, 'Contents:'
        print >> sys.stderr, fp.read()
        fp.close()
        return cleanupLock
    else:
        print >> sys.stderr, 'nope.'
        return False
    return


verifyLockBase = 'verifyLock' # lock file for missing data
def verifyLockName(runId):
    runDir = fileName(None, None, runId)
    verifyLockName = os.path.join(runDir, verifyLockBase)
    return verifyLockName
def makeVerifyLock(runId, content=''):
    verifyLock = verifyLockName(runId)
    print >> sys.stderr, 'Trying to append to %s ... ' % verifyLock,
    fp = open(verifyLock, 'a')
    fp.write(content)
    fp.close()
    print >> sys.stderr, 'OK'
    return
def checkVerifyLock(runId):
    verifyLock = verifyLockName(runId)
    print >> sys.stderr, 'Checking for %s ... ' % verifyLock,
    if os.path.exists(verifyLock):
        print >> sys.stderr, 'yep.'
        fp = open(verifyLock)
        print >> sys.stderr, 'Contents:'
        print >> sys.stderr, fp.read()
        fp.close()
        return verifyLock
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

dataCatExceptions = { 
    'filteredMerit': 'MERIT',
    }
def dataCatType(fileType):
    dcType = dataCatExceptions.get(fileType) or fileType.upper()
    return dcType

sites = ['SLAC', 'SLAC_XROOT']
def getSite(fileName):
    site = sites[fileName.startswith('root:')]    
    return site

def fileName(fileType, dlId, runId=None, chunkId=None, crumbId=None,
             next=False, version=None, ignoreName=False):

    if fileType is not None and not ignoreName:
        try:
            fullName = variables.getVar(fileType, 'fileName')
        except KeyError:
            fullName = None
            pass
        if fullName is not None: return fullName
        pass

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

    if level == 'run' and fileTypes[fileType] in xrootFileTypes:
        subDir = xrootSubDirectory(fileType, dlId, runId)
    else:
        subDir = subDirectory(fileType, dlId, runId, chunkId, crumbId)
        pass
    
    if level == 'run' and fileType is None:
        runDir = os.path.join(config.L1Dir, subDir)
        return runDir
        
    # Assign a version. Maybe.
    if fileType in ['chunkList']:
        verStr = dlId
    else:
        if version is None:
            try:
                version = int(variables.getVar(fileType, 'ver'))
            except KeyError:
                version = int(os.environ['PIPELINE_PROCESSINSTANCE'])
                pass
            pass

        # it's an error if next and version was the PI but we don't check ATM
        if next:
            version += 1
            # if we're reprocessing, we probably aren't starting from 0
            baseVersion = int(os.environ.get('baseVersion', '0'))
            version = max(version, baseVersion)
            pass
        
        if level in ['run']:
            format = '%03d'
        else:
            format = '%s'
            pass

        verStr = 'v' + format % version
        pass

    if fileType in ['magic7Hp']:
        verStr = '_'.join([dlId, verStr])
        pass
    pass

    if verStr is not None: fields.append(verStr)

    # handle different naming convention for files sent to FSSC
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

    baseDir = baseDirectory(fileType, level, relativePath)
    
    fullName = os.path.join(baseDir, relativePath)

    return fullName


def findPieces(fileType, dlId, runId=None, chunkId=None):
    """@brief find chunks or crumbs to merge.

    @arg fileType The type of file we're merging ('digi', 'reconMon', etc.)
    If this is None, will return a list of directories.

    @arg dlId

    @arg runId

    @arg [chunkId]

    @return A sequence of file names
    """

    if chunkId is not None:
        level = 'chunk'
    elif runId is not None:
        level = 'run'
    else:
        level = 'downlink'
        pass

    if level == 'downlink':
        # We're not merging anything, just finding downlink dirs to delete.
        argSets = [(fileType, dlId)]
    elif level == 'run' and fileType is None:
        # Just finding run buffers to delete
        argSets = [(fileType, dlId, runId, chunkId)]
    else:
        # We are either
        # deleting crumb directories.
        if fileType is None:
            crumbVar = variables.getVar('crumb', 'list')
            crumbIds = crumbVar.split(os.sep)
            crumbIds.sort()
            argSets = [(fileType, dlId, runId, chunkId, crumbId)
                       for crumbId in crumbIds]
        # or merging crumbs into chunks or chunks into runs
        else:            
            goodPis = os.environ['goodPis']
            tags = goodPis.split(',')
            versionTags = [tag.split(':') for tag in tags]
            if level == 'run':
                head = (fileType, dlId, runId,)
                tail = (None, None,)
            elif level == 'chunk':
                head = (fileType, dlId, runId, chunkId)
                tail = (None,)
                pass
            argSets = [head + (pieceId,) + tail + (ver,)
                       for (pieceId, ver) in versionTags]
            pass
        pass
    
    if fileType is None:
        funk = subDirectory
    else:
        funk = fileName
        pass

    pieces = [funk(*args) for args in argSets]

    if fileType is None:
        if level in ['run', 'downlink']:
            baseDirs = [config.xrootStage]
        else:
            baseDirs = [baseDirectory(fileType, level, pieces[0])]
            pass

        pieces = [os.path.join(baseDir, piece)
                  for piece in pieces
                  for baseDir in baseDirs]
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
        runTag = int(runId[1:])
        runTag = '%d' % runTag
        runTag = runTag[:3]
        dirs.extend(['runs', runTag, runId])
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


def dlDirectory(dlRawDir):
    subDir = os.path.basename(dlRawDir)
    midDir = subDir[:4]
    directory = os.path.join(config.dlStorage, midDir, subDir)
    return directory


def baseDirectory(fileType, level, relativePath):
    if level == 'downlink':
        baseDir = config.L1Dir
    elif level == 'run':
        if fileTypes[fileType] in xrootFileTypes:
            baseDir = config.xrootBase
        elif fileType is None:
            baseDir = config.xrootStage
        else:
            baseDir = config.L1Dir
            pass
    elif level == 'chunk' and fileType is None:
        # deleting crumb directories
        baseDir = config.xrootStage
    elif level in ['crumb', 'chunk']:
        baseDir = config.xrootStage
        pass
    # We will choke here if there is a hole in the logic. It's a feature.
    return baseDir


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

