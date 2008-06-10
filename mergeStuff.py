#!/afs/slac/g/glast/isoc/flightOps/rhel3_gcc32/ISOC_PROD/bin/shisoc python2.5

"""@brief Merge results of chunk or crumb processing.

@author W. Focke <focke@slac.stanford.edu>
"""

import glob
import os
import shutil
import string
import sys

import config

import GPLinit

import fileNames
import l1Logger
import registerPrep
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

expectedInFiles = fileNames.findPieces(fileType, dlId, runId, chunkId)
realInFiles = []
for inFile in expectedInFiles:
    if os.path.isfile(inFile):
        realInFiles.append(inFile)
    else:
        print >> sys.stderr, "Couldn't find input file %s" % inFile
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
    if mergeLevel == 'chunk':
        idStr += ' chunk %s' % chunkId
        pass
    msg = """Merging %(fileType)s file for %(idStr)s could not find all expected input files.""" % locals()
    print >> sys.stderr, msg
    l1Logger.error(msg)
    pass

realOutFile = fileNames.fileName(fileType, dlId, runId, chunkId, next=True)

inStage = stageFiles.StageSet()

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
    }

print >> sys.stderr, '------------------- start merge ------------------'
status = 0



if fileType in ['calHist', 'digiHist', 'fastMonHist', 'reconHist', 'meritHist']:
    setup = config.packages['Monitor']['setup']
    mergeConfig = config.mergeConfigs[fileType]
    app = config.apps['reportMerge']
    cmd = """
    cd %(workDir)s
    source %(setup)s
    %(app)s -c %(mergeConfig)s -o %(outFile)s %(inFileString)s
    """ % locals()
    status |= runner.run(cmd)


elif fileType in ['calTrend', 'digiTrend', 'fastMonTrend', 'meritTrend',
                  'reconTrend']:
    setup = config.packages['Monitor']['setup']
    app = config.apps['trendMerge']
    treeName = 'Time'
    cmd = '''
    cd %(workDir)s
    source %(setup)s
    %(app)s %(inFileString)s -o %(outFile)s -t %(treeName)s
    ''' % locals()
    status |= runner.run(cmd)


elif fileType in ['digi', 'recon', 'gcr']:
    import rootFiles
    treeName = treeNames[fileType]
    status |= rootFiles.concatenate_prune(outFile, inFiles, treeName)


# elif fileType in ['cal'] and mergeLevel == 'chunk':
#     import rootFiles
#     treeName = treeNames[fileType]
#     rootFiles.concatenate_cal(outFile, inFiles, treeName)


elif fileType in ['fastMonError']:
    app = config.apps['errorMerger']
    cmd = '''
    %(app)s -o %(outFile)s %(inFileString)s
    ''' % locals()
    status |= runner.run(cmd)


elif fileType in ['tkrAnalysis']:
    python = config.python
    app = config.apps['tkrMerger']
    inFileString = ' %s' * len(inFiles) % tuple(inFiles)
    cmd = '''
    cd %(workDir)s
    %(python)s %(app)s %(outFile)s %(inFileString)s
    ''' % locals()
    status = runner.run(cmd)


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
