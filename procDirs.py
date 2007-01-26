"""@brief Directories for different processes.

@author W. Focke <focke@slac.stanford.edu>
"""

import os

import config


L1Disk = '/nfs/slac/g/svac/focke/L1'
L1Dir = os.path.join(L1Disk, 'rootData')

outputDirs = { \
    'mergeDigi': runDir,
    }


def setup(runId, downlinkId, chunkId=None, crumbId=None):
    global outputDirs
    runDir = os.path.join(L1Dir, runId)
    dlDir = os.path.join(runDir, downlinkId)
    if chunkId is not None:
        setupChunk()
        if crumbId is not None:
            setupCrumb()
            pass
        pass
    return

def setupChunk(chunkId):
    global outputDirs
    chunkDir = os.path.join(dlDir, chunkId)
    digiMonDir = os.path.join(chunkDir, 'digiMon', config.testReportVersion)
    reconMonDir = os.path.join(chunkDir, 'reconMon', config.testReportVersion)
    return

def setupCrumb(crumbId):
    global outputDirs
    crumbDir = os.path.join(chunkDir, crumbId)
    return
