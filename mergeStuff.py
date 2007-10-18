#!/afs/slac/g/glast/isoc/flightOps/rhel3_gcc32/ISOC_PROD/bin/shisoc python2.5

"""@brief Merge results of chunk or crumb processing.

@author W. Focke <focke@slac.stanford.edu>
"""

import glob
import os
import shutil
import string
import sys

import GPLinit

import runner

import config

import fileNames
import registerPrep
import stageFiles
import rootFiles

def finalize(status):
    if status:
        finishOption = 'wipe'
    else:
        finishOption = config.finishOption
    status |= inStage.finish(finishOption)
    # status |= outStage.finish()
    
    registerPrep.prep(fileType, realOutFile)
    sys.exit(status)

fileType = os.environ['fileType']
dlId = os.environ['DOWNLINK_ID']
runId = os.environ['RUNID']
chunkId = os.environ.get('CHUNK_ID')

if chunkId is None:
    mergeLevel = 'run'
    stageDirPieces = [dlId, runId, fileType]
else:
    mergeLevel = 'chunk'
    stageDirPieces = [dlId, runId, chunkId, fileType]
    pass

files = fileNames.setup(dlId, runId, chunkId)

realInFiles = fileNames.findPieces(fileType, dlId, runId, chunkId)
realOutFile = files[mergeLevel][fileType]

numInFiles = len(realInFiles)

if numInFiles == 0:
    print >> sys.stderr, "No input files, cannot continue."
    sys.exit(1)
    pass

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
    shutil.copyfile(inFiles[0], realOutFile)
    finalize(0)
    pass

outFile = outStage.stageOut(realOutFile)
workDir = os.path.dirname(outFile)
#os.chdir(workDir)

inFileString = ''.join([' -i %s ' % ff for ff in inFiles])

if fileType in ['digiEor', 'reconEor', 'fastMon']:
    setup = config.packages['Monitor']['setup']
    mergeConfig = config.mergeConfigs[fileType]
    app = config.apps['reportMerge']
    cmd = """
    cd %(workDir)s
    source %(setup)s
    %(app)s -c %(mergeConfig)s -o %(outFile)s %(inFileString)s
    """ % locals()

elif fileType in ['digiTrend', 'reconTrend']:
    setup = config.packages['Monitor']['setup']
    app = config.apps['trendMerge']
    treeName = 'Time'
    cmd = '''
    cd %(workDir)s
    source %(setup)s
    %(app)s %(inFileString)s -o %(outFile)s -t %(treeName)s
    ''' % locals()


elif fileType in ['digi', 'recon', 'gcr']:
    treeNames = {
        'digi': 'Digi',
        'recon': 'Recon',
        'gcr': 'GcrSelect',
        }
    #treeName = string.capitalize(fileType)
    treeName = treeNames[fileType]
    print >> sys.stderr, '------------------- start merge ------------------'
    rootFiles.concatenate_prune(outFile, inFiles, treeName)
    print >> sys.stderr, '------------------- finish merge -----------------'
    cmd = 'echo Nothing to do here.'


else:
    app = config.hadd
    inFileString = ' %s' * len(inFiles) % tuple(inFiles)
    cmd = '''
    cd %(workDir)s
    %(app)s %(outFile)s %(inFileString)s
    ''' % locals()

    pass

status = runner.run(cmd)

finalize(status)
