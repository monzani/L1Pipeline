"""@brief Directories for different processes.

@author W. Focke <focke@slac.stanford.edu>
"""

import os

import config


L1Disk = '/nfs/slac/g/svac/focke/L1'
L1Dir = os.path.join(L1Disk, 'rootData')




def setup(runId, chunkId=None, crumbId=None):
    """@brief Setup data directory names.  And create the directories.

    @arg runId The run ID.

    @arg [chunkId] The chunk ID.

    @arg [crumbId] The crumb ID.

    @return A dictionary containing the names of various data directories.
    
    """
    dirs = {}
    runBase = os.path.join(L1Dir, runId)
    runDir = os.path.join(runBase, config.glastVersion)
    dirs['run'] = runDir
    if chunkId is not None:
        _setupChunk(dirs, chunkId)
        if crumbId is not None:
            _setupCrumb(dirs, crumbId)
            pass
        pass

    for item in dirs.values():
        mkdir(item)
    return dirs


def _setupChunk(dirs, chunkId):
    runDir = dirs['run']
    chunkDir = os.path.join(runDir, chunkId)
    dirs['chunk'] = chunkDir
    digiMonDir = os.path.join(chunkDir, 'digiMon', config.digiMonVersion)
    dirs['digiMon'] = digiMonDir
    reconMonDir = os.path.join(chunkDir, 'reconMon', config.reconMonVersion)
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
    os.mkdirs(path)
    return
