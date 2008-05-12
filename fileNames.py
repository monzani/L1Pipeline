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


fileTypes = {
    'acdPlots': 'tar',
    'cal': 'root',
    'calEor': 'root',
    'calTrend': 'root',
    'chunkList': 'txt',
    'compareDFm': 'xml',
    'crumbList': 'txt',
    'digi': 'root',
    'digiEor': 'root',
    'digiEorAlarm': 'xml',
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
    'magic7': 'txt',
    'merit': 'root',
    'meritEor': 'root',
    'meritTrend': 'root',
    'recon': 'root',
    'reconEor': 'root',
    'reconEorAlarm': 'xml',
    'reconEorAlarmDist': 'root',
    'reconTrend': 'root',
    'reconTrendAlarm': 'xml',
    'svac': 'root',
    'svacHist': 'root',
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


def dataCatName(fileType, fileName):
    dsType = fileType.upper()
    junk, baseName = os.path.split(fileName)
    name = '%s/%s:%s' % (config.dataCatDir, dsType, baseName)
    return name

sites = ['SLAC', 'SLAC_XROOT']
def sitedName(fileName):
    site = sites[fileName.startswith('root:')]
    filePath = '%s@%s' % (fileName, site)
    return filePath


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
        runDir = os.path.join(config.L1Dir, subDir)

        if dsType is None:
            return runDir
        
        if fileTypes[dsType] in xrootFileTypes:
            subDir = xrootSubDirectory(dsType, dlId, runId)
            baseDir = config.xrootBase
        else:
            baseDir = config.L1Dir
            pass
        
        if dsType in ['chunkList', 'magic7']:
            verStr = dlId
        else:
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            # This has horrible concurrency issues.
            # It is protected by the global run lock.
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            #
            # And it blows for so many reasons on top of that.
            # Replace with something based on the files that are
            # already present.
            # Or not.
            # It has to work this way to use xrootd and not data catalog lookup.
            # So it has to stay for now.
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
            these = readList(chunkFile).keys()
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


def readListOld(inFile):
    items = [line.strip().split()[0] for line in open(inFile)]
    return items

def readListNew(inFile):
    return cPickle.load(open(inFile))

def writeList(data, outFile):
    cPickle.dump(data, open(outFile, 'w'))
    return

readList = readListNew


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

    if level in ['crumb', 'chunk'] and dsType is not None:
        dirs.append(dsType)
        pass

    dirName = os.path.join(*dirs)
    
    return dirName

def xrootSubDirectory(dsType, dlId, runId=None):
    subDir = dsType
    return subDir


versRe = re.compile('_v([0-9]+)[\._][^/]+$')
def version(fileName):
    mob = versRe.search(os.path.basename(fileName))
    if mob:
        vers = int(mob.group(1))
    else:
        raise ValueError, "Can't parse version from %s" % fileName
    return vers
