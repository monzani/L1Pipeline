"""@brief Conventions for naming files.

@author W. Focke <focke@slac.stanford.edu>
"""

import glob
import os
import sys
import time

import config

import glastTime
import lockFile
import procDirs


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

    # VERYBAD! We should not be getting this from args anymore.
    head, dlId = os.path.split(os.environ['DOWNLINK_RAWDIR'])
    if not dlId: head, dlId = os.path.split(head)
    
    runHead = runId

    dirs = procDirs.setup(dlId, runId, chunkId, crumbId, createDirs)
    files = {}
    files['run'] = {}

    files['dirs'] = dirs

    #files['downlink'] = {}
    #files['downlink']['runList'] = os.path.join(dirs['downlink'], 'runList')

    if chunkId is not None:
        files['chunk'] = _setupChunk(dirs, chunkId, runHead)
        if crumbId is not None:
            chunkHead = files['chunk']['head']
            files['crumb'] = _setupCrumb(dirs, crumbId, chunkHead)
            pass
        pass


    # # This doesn't work, it gets generated differently for different
    # # processes in the same stream.  So makeFT1 can't find the merit file.
    # timestamp = '%09d' % int(glastTime.met())
    # dlHead = join(runHead, timestamp, dlId)

    runDir = files['dirs']['run']
    try:
        # This picks up the time (MET) at which the run lock was created,
        # just before starting findChunks.  So it should be fixed for
        # a given run/downlink combo, and should sort into time order
        # (of file creation time), which should put the most-complete
        # version of a file highest.
        lockData = lockFile.readLock(runDir, runId, dlId)
        timeStamp = glastTime.timeStamp(lockData['time'])
        dlHead = join(runHead, timeStamp)
    except:
        # Use downlink ID as a fallback.
        print >> sys.stderr, "Problem reading lock from [%s]." % runDir
        dlHead = join(runHead, dlId)
        pass

    files['run']['head'] = dlHead

    files['run']['cal'] = os.path.join(
        dirs['run'], join(dlHead, 'cal.root'))
    files['run']['digi'] = os.path.join(
        dirs['run'], join(dlHead, 'digi.root'))
    files['run']['digiEor'] = os.path.join(
        dirs['run'], join(dlHead, 'digiEor.root'))
    files['run']['digiEorAlarm'] = os.path.join(
        dirs['run'], join(dlHead, 'digiEorAlarm.xml'))
    files['run']['digiTrend'] = os.path.join(
        dirs['run'], join(dlHead, 'digiTrend.root'))
    files['run']['digiTrendAlarm'] = os.path.join(
        dirs['run'], join(dlHead, 'digiTrendAlarm.xml'))
    files['run']['fastMonError'] = os.path.join(
        dirs['run'], join(dlHead, 'fastMonError.xml'))
    files['run']['fastMonHist'] = os.path.join(
        dirs['run'], join(dlHead, 'fastMonHist.root'))
    files['run']['fastMonHistAlarm'] = os.path.join(
        dirs['run'], join(dlHead, 'fastMonAlarm.xml'))
    files['run']['fastMonTuple'] = os.path.join(
        dirs['run'], join(dlHead, 'fastMonTuple.root'))
    files['run']['ft1'] = os.path.join(
        dirs['run'], join(dlHead, 'ft1.fits'))
    files['run']['ft1Export'] = os.path.join(
        dirs['run'], exportName(dlId, 'evsum'))
    files['run']['ft2Export'] = os.path.join(
        dirs['run'], exportName(dlId, 'pt'))
    files['run']['ft2'] = os.path.join(
        dirs['run'], join(dlHead, 'ft2.fits'))
    files['run']['ft2Txt'] = os.path.join(
        dirs['run'], join(dlHead, 'ft2.txt'))
    files['run']['gcr'] = os.path.join(
        dirs['run'], join(dlHead, 'gcr.root'))
    files['run']['m7'] = os.path.join(
        os.environ['DOWNLINK_RAWDIR'], 'magic7_%s.txt' % dlId)
    files['run']['merit'] = os.path.join(
        dirs['run'], join(dlHead, 'merit.root'))
    files['run']['recon'] = os.path.join(
        dirs['run'], join(dlHead, 'recon.root'))
    files['run']['reconEor'] = os.path.join(
        dirs['run'], join(dlHead, 'reconEor.root'))
    files['run']['reconEorAlarm'] = os.path.join(
        dirs['run'], join(dlHead, 'reconEorAlarm.xml'))
    files['run']['reconTrend'] = os.path.join(
        dirs['run'], join(dlHead, 'reconTrend.root'))
    files['run']['reconTrendAlarm'] = os.path.join(
        dirs['run'], join(dlHead, 'reconTrendAlarm.xml'))
    files['run']['svac'] = os.path.join(
        dirs['run'], join(dlHead, 'svac.root'))
    
    return files


def _setupChunk(dirs, chunkId, runHead):
    files = {}
    chunkHead = join(runHead, chunkId)
    files['head'] = chunkHead
    
    files['cal'] = os.path.join(
        dirs['cal'], join(chunkHead, 'cal.root'))
    files['digi'] = os.path.join(
        dirs['digi'], join(chunkHead, 'digi.root'))
    files['digiEor'] = os.path.join(
        dirs['digiEor'], join(chunkHead, 'digiEor.root'))
    files['digiTrend'] = os.path.join(
        dirs['digiTrend'], join(chunkHead, 'digiTrend.root'))
    files['event'] = os.environ.get('EVTFILE') # only set if at chunk level
    files['fastMonError'] = os.path.join(
        dirs['fastMon'], join(chunkHead, 'fastMonError.xml'))
    files['fastMonHist'] = os.path.join(
        dirs['fastMon'], join(chunkHead, 'fastMonHist.root'))
    files['fastMonTuple'] = os.path.join(
        dirs['fastMon'], join(chunkHead, 'fastMonTuple.root'))
    files['ft2Fake'] = os.path.join(
        dirs['ft2Fake'], join(chunkHead, 'ft2Fake.fits'))
    files['gcr'] = os.path.join(
        dirs['gcr'], join(chunkHead, 'gcr.root'))
    files['merit'] = os.path.join(
        dirs['merit'], join(chunkHead, 'merit.root'))
    files['recon'] = os.path.join(
        dirs['recon'], join(chunkHead, 'recon.root'))
    files['reconEor'] = os.path.join(
        dirs['reconEor'], join(chunkHead, 'reconEor.root'))
    files['reconTrend'] = os.path.join(
        dirs['reconTrend'], join(chunkHead, 'reconTrend.root'))
    files['svac'] = os.path.join(
        dirs['svac'], join(chunkHead, 'svac.root'))
    files['svacHist'] = os.path.join(
        dirs['svac'], join(chunkHead, 'svacHist.root'))

    return files


def _setupCrumb(dirs, crumbId, chunkHead):
    files = {}
    crumbHead = join(chunkHead, crumbId)
    files['head'] = crumbHead
    
    files['cal'] = os.path.join(
        dirs['crumb'], join(crumbHead, 'cal.root'))
    files['gcr'] = os.path.join(
        dirs['crumb'], join(crumbHead, 'gcr.root'))
    files['merit'] = os.path.join(
        dirs['crumb'], join(crumbHead, 'merit.root'))
    files['recon'] = os.path.join(
        dirs['crumb'], join(crumbHead, 'recon.root'))

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

    files = setup(dlId, runId, chunkId, crumbId, \
                  createDirs=False)
    pattern = files[level][fileType]

    print >> sys.stderr, "Searching for files that match [%s]." % pattern

    inFiles = glob.glob(pattern)
    inFiles.sort(key=os.path.basename)

    print >> sys.stderr, "Matching files are: %s" % inFiles
   
    return inFiles


def ft1ExportName(dlId):
    day = dlId[:-3]
    contact = dlId[-3:]
    
    version = '%.2d' % 0 # FIX THIS

    lD = len(day)
    if lD < 6:
        day = '0' * (6 - lD) + day # nasty hack

    name = 'gll_evsum_%s_c%s_v%s.fit' % (day, contact, version)
    return name

def exportName(dlId, fileType):
    day = dlId[:-3]
    contact = dlId[-3:]
    
    version = '%.2d' % 0 # FIX THIS

    lD = len(day)
    if lD < 6:
        day = '0' * (6 - lD) + day # nasty hack

    name = 'gll_%s_%s_c%s_v%s.fit' % (fileType, day, contact, version)
    return name
