#!/afs/slac/g/glast/isoc/flightOps/rhel3_gcc32/ISOC_PROD/bin/shisoc python2.5

"""@brief Merge results of chunk or crumb processing.

@author W. Focke <focke@slac.stanford.edu>
"""

import os
import sys
import time

if __name__ == "__main__":
    print >> sys.stderr, "This module is not supported as main script"
    sys.exit(1)

import config

import fileOps
import fileNames
import fitsFiles
import l1Logger
import lockFile
import pipeline
import runner


def merge(files, idArgs, level, outFileTypes, staged, workDir, **args):
    status = 0

    dlId, runId, chunkId, crumbId = idArgs

    assert len(outFileTypes) == 1
    fileType = outFileTypes[0]

    # This is backwards. Should be a map from fileType to merge function.
    # Which requires putting the per-type merge code into functions.
    # Which has some scope issues.
    mergeTypes = {
        'error': ['fastMonError'],
        'fits': ['ft1', 'ft2', 'ft1BadGti', 'ft1NoDiffRsp', 'ls1', 'ls3'],
        'report': ['calHist', 'digiHist', 'fastMonHist', 'meritHist', 'reconHist'],
        'tkr': ['tkrAnalysis'],
        'tree': ['cal', 'digi', 'gcr', 'merit', 'recon', 'svac', 'fastMonTuple'],
        'trend': ['calTrend', 'digiTrend', 'fastMonTrend', 'meritTrend', 'reconTrend'],
        }
    # Check whether any types occur in multiple lists.
    # This would not be necessary if the comments above were implemented.
    checkedTypes = set()
    for key, values in mergeTypes.items():
        newTypes = set(values)
        assert not newTypes & checkedTypes
        checkedTypes |= newTypes
        continue

    # This import is a bit flaky. If we attempt it (and it fails):
    # - when we actually need it, after staging input, we do unneeded I/O;
    # - unconditionally, we sometimes fail when we didn't even need that code.
    if fileType in mergeTypes['tree']: import rootFiles

    expectedInFiles = fileNames.findPieces(fileType, dlId, runId, chunkId)
    realInFiles = []
    missingInFiles = []
    for inFile in expectedInFiles:
        if fileOps.exists(inFile):
            realInFiles.append(inFile)
        else:
            print >> sys.stderr, "Couldn't find input file %s" % inFile
            missingInFiles.append(inFile)
            pass
        continue
    numInFiles = len(realInFiles)
    if numInFiles == 0:
        print >> sys.stderr, "No input files, cannot continue."
        return 1
        pass

    # Here we should send a message to the log watcher if we didn't find all of
    # the expected input files.
    if numInFiles != len(expectedInFiles):
        idStr = 'run %s' % runId
        target = '%s' %runId
        if level == 'chunk':
            idStr += ' chunk %s' % chunkId
            target += '.%s'  % chunkId
            pass
        msg = """Merging %(fileType)s file for %(idStr)s could not find all expected input files.""" % locals()
        print >> sys.stderr, msg

        kwargs = {'tgt': target}
    
        l1Logger.error(msg, **kwargs)

        print >> sys.stderr, 'Supressing cleanup.'

        process = pipeline.getProcess()
        streamPath = os.environ.get('PIPELINE_STREAMPATH')
        processInstance = os.environ.get('PIPELINE_PROCESSINSTANCE')
        timeStamp = time.ctime()
        content = 'Locked by %s %s pipk = %s at %s\n' % (process, streamPath, processInstance, timeStamp)
        for inFile in missingInFiles:
            content += '%s\n' % inFile
            continue
        fileNames.makeMergeLock(runId, content)
        
        pass

    outFile = files[fileType]

    if numInFiles == 1:
        # We're "merging" 1 file.  So it's just a copy.
        #
        # The output has already been "staged". Don't bother staging input.
        # This might seems wasteful
        # relative to copying the unstaged input to the unstaged output,
        # but they're probably on the same filesystem, and this reduces the
        # load on the file server in that case.
        print >> sys.stderr, 'Single input file, copying %s to %s' % \
              (realInFiles[0], outFile)
        fileOps.copy(realInFiles[0], outFile)
        if  fileType in ['merit'] and level == 'run':
            print >> sys.stderr, \
                  "Attempting to remove throttling lock for [%s,%s] at [%s]" % (dlId,runId,time.ctime())
            lockFile.unlockThrottle(dlId,runId)
            pass
        return status
    
    inFiles = [staged.stageIn(iFile) for iFile in realInFiles]
    
    for i_infile in range(len(inFiles)):
        print >> sys.stderr, "Infile ", i_infile, " is ", inFiles[i_infile], " and realInFile is ", realInFiles[i_infile]
        continue

    inFileString = ''.join([' -i %s ' % ff for ff in inFiles])

    treeNames = {
        'cal': 'CalTuple',
        'digi': 'Digi',
        'fastMonTuple': 'IsocDataTree',
        'gcr': 'GcrSelect',
        'merit': 'MeritTuple',
        'recon': 'Recon',
        'svac': 'Output',
        }

    print >> sys.stderr, '------------------- start merge ------------------'

    if fileType in mergeTypes['report']:
        setup = config.packages['Monitor']['setup']
        mergeConfig = config.mergeConfigs[fileType]
        app = config.apps['reportMerge']
        cmd = """
        cd %(workDir)s
        source %(setup)s
        %(app)s -c %(mergeConfig)s -o %(outFile)s %(inFileString)s
        """ % locals()
        status |= runner.run(cmd)


    elif fileType in mergeTypes['trend']:
        setup = config.packages['Monitor']['setup']
        app = config.apps['trendMerge']
        treeName = 'Time'
        cmd = '''
        cd %(workDir)s
        source %(setup)s
        %(app)s %(inFileString)s -o %(outFile)s -t %(treeName)s
        ''' % locals()
        status |= runner.run(cmd)


    elif fileType in mergeTypes['tree']:
        treeName = treeNames[fileType]
        #    status |= rootFiles.concatenate(outFile, inFiles, treeName, basketSize=111111)
        status |= rootFiles.concatenate(outFile, inFiles, treeName)


        # elif fileType in ['cal'] and level == 'chunk':
        #     treeName = treeNames[fileType]
        #     rootFiles.concatenate_cal(outFile, inFiles, treeName)


    elif fileType in mergeTypes['error']:
        app = config.apps['errorMerger']
        cmd = '''
        %(app)s -o %(outFile)s %(inFileString)s
        ''' % locals()
        status |= runner.run(cmd)


    elif fileType in mergeTypes['tkr']:
        python = config.python
        app = config.apps['tkrMerger']
        inFileString = ' %s' * len(inFiles) % tuple(inFiles)
        cmd = '''
        cd %(workDir)s
        %(python)s %(app)s %(outFile)s %(inFileString)s
        ''' % locals()
        status = runner.run(cmd)


    elif fileType in mergeTypes['fits']:
        status |= fitsFiles.mergeFiles(outFile, inFiles)


    else:
        app = config.hadd
        inFileString = ' %s' * len(inFiles) % tuple(inFiles)
        cmd = '''
        cd %(workDir)s
        echo $LD_LIBRARY_PATH
        %(app)s %(outFile)s %(inFileString)s
        ''' % locals()
        status = runner.run(cmd)


        pass

    print >> sys.stderr, '------------------- finish merge -----------------'

    if  fileType in ['merit'] and level == 'run':
        print >> sys.stderr, \
              "Attempting to remove throttling lock for [%s,%s] at [%s]" % (dlId,runId,time.ctime())
        lockFile.unlockThrottle(dlId,runId)
        
    return status

    
