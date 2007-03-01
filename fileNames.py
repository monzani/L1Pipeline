"""@brief Conventions for naming files.

@author W. Focke <focke@slac.stanford.edu>
"""

import glob
import os

import config
import procDirs

headFields = 3

def baseHead(inFile):
    """@brief DEPRECATED

    Parses out the portion of a filename that does not depend on
    the file type.
    """

    inDir, inName = os.path.split(inFile)

    cut = inName.rindex('.')
    inBase = inName[:cut]
    allFields = inBase.split('_')

    goodFields = allFields[:headFields]
    head = '_'.join(goodFields)

    return head

def join(*args):
    joined = '_'.join(args)
    return joined


def setup(dlId, runId=None, chunkId=None, crumbId=None, createDirs=True):
    """@brief Setup data directory names.

    @arg dlId The dowlink ID.

    @arg [runId] The run ID.

    @arg [chunkId] The chunk ID.

    @arg [crumbId] The crumb ID.

    @return A dictionary containing the names of various data files.
    
    """
    runHead = runId

    dirs = procDirs.setup(dlId, runId, chunkId, crumbId, createDirs)
    files = {}
    files['run'] = {}

    files['dirs'] = dirs

    files['downlink'] = {}
    files['downlink']['runList'] = os.path.join(dirs['downlink'], 'runList')

    if chunkId is not None:
        files['chunk'] = _setupChunk(dirs, chunkId, runHead)
        if crumbId is not None:
            chunkHead = files['chunk']['head']
            files['crumb'] = _setupCrumb(dirs, crumbId, chunkHead)
            pass
        pass

    dlHead = join(runHead, dlId)
    files['run']['head'] = dlHead
    files['run']['digi'] = os.path.join(dirs['run'], \
                                        join(dlHead, 'digi.root'))
    files['run']['digiMon'] = os.path.join(dirs['run'], \
                                           join(dlHead, 'digiHist.root'))
    files['run']['recon'] = os.path.join(dirs['run'], \
                                         join(dlHead, 'recon.root'))
    files['run']['merit'] = os.path.join(dirs['run'], \
                                         join(dlHead, 'merit.root'))
    files['run']['cal'] = os.path.join(dirs['run'], \
                                       join(dlHead, 'cal.root'))
    files['run']['reconMon'] = os.path.join(dirs['run'],
                                            join(dlHead, 'reconHist.root'))
    files['run']['svac'] = os.path.join(dirs['run'], join(dlHead, 'svac.root'))
    
    
    return files


def _setupChunk(dirs, chunkId, runHead):
    files = {}
    chunkHead = join(runHead, chunkId)
    files['head'] = chunkHead
    files['digi'] = os.path.join(dirs['chunk'], \
                                 join(chunkHead, 'digi.root'))
    files['digiMon'] = os.path.join(dirs['chunk'], \
                                    join(chunkHead, 'digiHist.root'))
    files['recon'] = os.path.join(dirs['chunk'], \
                                  join(chunkHead, 'recon.root'))
    files['merit'] = os.path.join(dirs['chunk'], \
                                  join(chunkHead, 'merit.root'))
    files['cal'] = os.path.join(dirs['chunk'], \
                                join(chunkHead, 'cal.root'))
    files['reconMon'] = os.path.join(dirs['chunk'], \
                                     join(chunkHead, 'reconHist.root'))
    files['svac'] = os.path.join(dirs['chunk'], \
                                 join(chunkHead, 'svac.root'))

    return files


def _setupCrumb(dirs, crumbId, chunkHead):
    files = {}
    crumbHead = join(chunkHead, crumbId)
    files['head'] = crumbHead
    files['recon'] = os.path.join(dirs['crumb'], \
                                  join(crumbHead, 'recon.root'))
    files['merit'] = os.path.join(dirs['crumb'], \
                                  join(crumbHead, 'merit.root'))
    files['cal'] = os.path.join(dirs['crumb'], \
                                join(crumbHead, 'cal.root'))
    return files


def findPieces(fileType, dlId, runId, chunkId=None):
    """@brief find chunks or crumbs to merge.

    @arg fileType The type of file we're merging ('digi', 'reconMon', etc.)

    @arg dlId

    @arg runId

    @arg [chunkId]

    @return A sequence of file names
    """

    if chunkId is None:
        chunkId = '*'
        crumbId = None
        level = 'chunk'
    else:
        crumbId = '*'
        level = 'crumb'
        pass

    files = setup(os.environ['DOWNLINK_ID'], runId, chunkId, crumbId, \
                  createDirs=False)
    pattern = files[level][fileType]
    inFiles = glob.glob(pattern)

    inFiles.sort(key=os.path.basename)
   
    return inFiles
