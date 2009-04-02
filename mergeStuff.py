#!/afs/slac/g/glast/isoc/flightOps/rhel3_gcc32/ISOC_PROD/bin/shisoc python2.5

"""@brief Merge results of chunk or crumb processing.

@author W. Focke <focke@slac.stanford.edu>
"""

import glob
import os
import shutil
import string
import sys
import time

import config

import GPLinit

import fileNames
import fitsFiles
import l1Logger
import pipeline
import registerPrep
import rootFiles
import runner
import stageFiles


def finalize(status):
    if status:
        finishOption = 'wipe'
    else:
        finishOption = config.finishOption
    status |= inStage.finish(finishOption)
    # status |= outStage.finish()
    
    if not status: registerPrep.prep(fileType, realOutFile)
    sys.exit(status)

head, dlId = os.path.split(os.environ['DOWNLINK_RAWDIR'])
if not dlId: head, dlId = os.path.split(head)
runId = os.environ['RUNID']
chunkId = os.environ.get('CHUNK_ID')

fileType = os.environ['fileType']

if chunkId is None:
    mergeLevel = 'run'
    stageDirPieces = [dlId, runId, fileType]
else:
    mergeLevel = 'chunk'
    stageDirPieces = [dlId, runId, chunkId, fileType]
    pass

# This is backwards. Should be a map from fileType to merge function.
# Which requires putting the per-type merge code into functions.
# Which has some scope issues.
mergeTypes = {
    'report': ['calHist', 'digiHist', 'fastMonHist', 'reconHist', 'meritHist'],
    'trend': ['calTrend', 'digiTrend', 'fastMonTrend', 'meritTrend', 'reconTrend'],
    'tree': ['digi', 'recon', 'gcr', 'cal', 'svac'],
    'error': ['fastMonError'],
    'tkr': ['tkrAnalysis'],
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
    if stageFiles.checkFile(inFile):
        realInFiles.append(inFile)
    else:
        print >> sys.stderr, "Couldn't find input file %s" % inFile
        missingInFiles.append(inFile)
        pass
    continue
numInFiles = len(realInFiles)
if numInFiles == 0:
    print >> sys.stderr, "No input files, cannot continue."
    sys.exit(1)
    pass

# Here we should send a message to the log watcher if we didn't find all of
# the expected input files.
if numInFiles != len(expectedInFiles):
    idStr = 'run %s' % runId
    target = '%s' %runId
    if mergeLevel == 'chunk':
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

realOutFile = fileNames.fileName(fileType, dlId, runId, chunkId, next=True)

# avoid afs cache thash
if mergeLevel == 'run' and fileType in []: # not obviously helpful
    stageKWArgs = {'excludeIn': None}
else:
    stageKWArgs = {'excludeIn': config.excludeIn}
    pass

inStage = stageFiles.StageSet(**stageKWArgs)

outStageDir = '_'.join(stageDirPieces)
# outStage = stageFiles.StageSet(outStageDir, config.afsStage)
outStage = inStage

inFiles = [inStage.stageIn(iFile) for iFile in realInFiles]

# inFiles = []
# for realInFile in realInFiles[::-1]:
#     # Stage in input files in reverse order.  Then, if we run out of space
#     # on the input staging filesystem (/scratch), and some input files don't
#     # get staged, it's the ones that are merged in last, and are thus open
#     # the longest, that do get staged.

#     inFile = inStage.stageIn(realInFile)

#     # Put any input files that wouldn't fit on the input filesystem on
#     # the output filesystem.
#     if inFile == realInFile:
#         inFile = outStage.stageIn(relInFile)
#         pass

#     inFiles.append(inFile)
#     continue
# inFiles.reverse()

for i_infile in range(len(inFiles)):
    print >> sys.stderr, "Infile ", i_infile, " is ", inFiles[i_infile], " and realInFile is ", realInFiles[i_infile]

if numInFiles == 1:
    # We're "merging" 1 file.  So it's just a copy.
    # 
    # Stage the input, but not the output.  This might seems wasteful
    # relative to copying the unstaged input to the unstaged output,
    # but they're probably on the same filesystem, and this reduces the
    # load on the file server in that case.
    print >> sys.stderr, 'Single input file, copying %s to %s' % \
          (inFiles[0], realOutFile)
    #shutil.copyfile(inFiles[0], realOutFile) # Dude, we've got an INTERFACE for that!
    stageFiles.copy(inFiles[0], realOutFile) # Much better.
    finalize(0)
    pass

outFile = outStage.stageOut(realOutFile)
workDir = os.path.dirname(outFile)
#os.chdir(workDir)

inFileString = ''.join([' -i %s ' % ff for ff in inFiles])

treeNames = {
    'cal': 'CalTuple',
    'digi': 'Digi',
    'gcr': 'GcrSelect',
    'recon': 'Recon',
    'svac': 'Output',
    }

print >> sys.stderr, '------------------- start merge ------------------'
status = 0



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
    status |= rootFiles.concatenate_prune(outFile, inFiles, treeName)


# elif fileType in ['cal'] and mergeLevel == 'chunk':
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


elif realOutFile.endswith('.fit'):
    status |= fitsFiles.mergeFiles(outFile, inFiles)


else:
    app = config.hadd
    inFileString = ' %s' * len(inFiles) % tuple(inFiles)
    cmd = '''
    cd %(workDir)s
    %(app)s %(outFile)s %(inFileString)s
    ''' % locals()
    status = runner.run(cmd)


    pass

print >> sys.stderr, '------------------- finish merge -----------------'

finalize(status)
