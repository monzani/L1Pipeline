"""@brief Directories for different processes.

@author W. Focke <focke@slac.stanford.edu>
"""

import glob
import os
import re
import sys

import config

def setup(dlId, runId=None, chunkId=None, crumbId=None, createDirs=False):
    """@brief Setup data directory names.  And create the directories.

    @arg dlId The dowlink ID.

    @arg [runId] The run ID.

    @arg [chunkId] The chunk ID.

    @arg [crumbId] The crumb ID.

    @return A dictionary containing the names of various data directories.
    
    """
    dirs = {}
    #dlDir = os.path.join(config.L1Dir, 'downlinks', dlId)
    #dirs['downlink'] = dlDir
    #if runId is None:
    #    return dirs
    #runBase = os.path.join(config.L1Dir, 'runs', runId)
    runBase = os.path.join(config.L1Dir, runId)
    runDir = os.path.join(runBase, config.glastVersion)
    dirs['run'] = runDir
    if chunkId is not None:
        _setupChunk(dirs, chunkId)
        if crumbId is not None:
            _setupCrumb(dirs, crumbId)
            pass
        pass

    if createDirs:
        for item in dirs.values():
            mkdir(item)
            continue
        pass
    
    return dirs


def _setupChunk(dirs, chunkId):

    runDir = dirs['run']
    chunkDir = os.path.join(runDir, chunkId)
    dirs['chunk'] = chunkDir
    digiMonDir = os.path.join(chunkDir, 'digiMon', config.packages['TestReport']['version'])
    dirs['digiMon'] = digiMonDir
    reconMonDir = os.path.join(chunkDir, 'reconMon', config.packages['TestReport']['version'])
    dirs['reconMon'] = reconMonDir
    return


def _setupCrumb(dirs, crumbId):

    runDir = dirs['run']
    chunkDir = dirs['chunk']
    crumbDir = os.path.join(chunkDir, crumbId)
    dirs['crumb'] = crumbDir
    return


def mkdir(path):

    """@brief Create a directory and any necessary parents.

    @arg path The directory to create.

    Succeeds if path already exists and is a directory.
    Raises os.error if path already exists and is not a directory.

    So, basically, like 'mkdir -p $path'.
    
    """
    if os.path.exists(path):
        if os.path.isdir(path):
            return
        raise os.error
    os.makedirs(path)
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
