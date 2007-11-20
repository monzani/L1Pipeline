"""@brief Directories for different processes.

@author W. Focke <focke@slac.stanford.edu>
"""

import glob
import hashlib
import os
import re
import sys

import config
import runner

def setup(dlId, runId=None, chunkId=None, crumbId=None, createDirs=False):
    """@brief Setup data directory names.  And create the directories.

    @arg dlId The dowlink ID.

    @arg [runId] The run ID.

    @arg [chunkId] The chunk ID.

    @arg [crumbId] The crumb ID.

    @return A dictionary containing the names of various data directories.
    
    """
    dirs = {}
    runBase = os.path.join(config.L1Dir, runId)
    runDir = os.path.join(runBase, config.L1Version)
    dirs['run'] = runDir

    if chunkId is not None:
        _setupChunk(dirs, runId, chunkId)
        if crumbId is not None:
            _setupCrumb(dirs, runId, chunkId, crumbId)
            pass
        pass

    if createDirs:
        for item in dirs.values():
            mkdir(item)
            continue
        pass
    
    return dirs


def _setupChunk(dirs, runId, chunkId):

    # runStage = dirs['run']
    runStage = getRunStageBase(dirs, runId)
    chunkDir = os.path.join(runStage, 'chunkLinks', chunkId)
    dirs['chunk'] = chunkDir

    dirs['cal'] = os.path.join(chunkDir, 'cal')
    dirs['digi'] = os.path.join(chunkDir, 'digi')
    dirs['digiEor'] = os.path.join(chunkDir, 'digiEor')
    dirs['digiTrend'] = os.path.join(chunkDir, 'digiTrend')
    dirs['fastMon'] = os.path.join(chunkDir, 'fastMon')
    dirs['gcr'] = os.path.join(chunkDir, 'gcr')
    dirs['ft2Fake'] = os.path.join(chunkDir, 'ft2Fake')
    dirs['merit'] = os.path.join(chunkDir, 'merit')
    dirs['recon'] = os.path.join(chunkDir, 'recon')
    dirs['reconEor'] = os.path.join(chunkDir, 'reconEor')
    dirs['reconTrend'] = os.path.join(chunkDir, 'reconTrend')
    dirs['svac'] = os.path.join(chunkDir, 'svac')
    
    return


def _setupCrumb(dirs, runId, chunkId, crumbId):
    #chunkDir = dirs['chunk']
    runStage = getRunStageBase(dirs, runId)
    crumbDir = os.path.join(runStage, 'crumbLinks', chunkId, crumbId)
    dirs['crumb'] = crumbDir
    return


def mkdir(path):

    """@brief Create a directory and any necessary parents.

    @arg path The directory to create.

    Succeeds if path already exists and is a directory.
    Raises os.error if path already exists and is not a directory.

    So, basically, like 'mkdir -p $path'.
    
    """
    #if os.path.exists(path):
    #    if os.path.isdir(path):
    #        return
    #    raise os.error
    # # Race condition here!
    # os.makedirs(path)
    #
    # # punt
    if not os.path.exists(path):
        runner.run('mkdir -p %s' % path)
    return


def findPieceDirs(dlId, runId, chunkId=None):
    """@brief find chunks or crumb directories.

    @arg dlId

    @arg runId

    @arg [chunkId]

    @return A sequence of directory names
    """

    if chunkId is None:
        chunkId = '*'
        crumbId = None
        level = 'chunk'
        filter = '^e[0-9]*$'
    else:
        crumbId = '*'
        level = 'crumb'
        filter = '^b[0-9]*$'
        pass

    dirs = setup(dlId, runId, chunkId, crumbId, createDirs=False)
    pattern = dirs[level]
    pieceDirs = glob.glob(pattern)

    print >> sys.stderr, '----------------------------------------------'
    print >> sys.stderr, 'Pattern (first pass) is "%s", matching items are:' \
          % pattern
    for piece in pieceDirs:
        print >> sys.stderr, piece
        continue
    print >> sys.stderr, '----------------------------------------------'

    filterRe = re.compile(filter)
    pieceDirs = [d for d in pieceDirs if filterRe.match(os.path.basename(d))]

    print >> sys.stderr, '----------------------------------------------'
    print >> sys.stderr, 'Filter (second pass) is "%s", matching items are:' \
          % filter
    for piece in pieceDirs:
        print >> sys.stderr, piece
        continue
    print >> sys.stderr, '----------------------------------------------'

    pieceDirs.sort(key=os.path.basename)
   
    return pieceDirs

def myHash(str):
    return int(hashlib.md5(str).hexdigest(), 16)

def getRunStageBase(dirs, runId):
    index = myHash(runId) % len(config.stageDirs)
    base = config.stageDirs[index]
    stager = os.path.join(base, runId)
    return stager


def getStageDir(*args):
    stageDir = os.path.join(*args)
    return stageDir
