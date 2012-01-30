import os
import sys
import time

import config

import acqQuery
import chunkTester
import fileNames
import finders
import pipeline
import variables

runId = os.environ['RUNID']
runNumber = int(runId[1:])

#location = 'SLAC_XROOT'
#locOpt = ' --site %s ' % location
 
fileTypes = os.environ['fileTypes']
typeList = fileTypes.split(',')

newFolder = os.environ['dataCatDir']
oldFolder = '/Data/Flight/Level1/LPA'
folders = {
    'DIGI': oldFolder,
    'MAGIC7L1': oldFolder,
    'MERIT': oldFolder,
    }

mode = config.mode

datacat = '''/afs/slac.stanford.edu/u/gl/glast/datacat/%s/datacat find --group %s --filter 'Name=="%s"'  --show-unscanned-locations   --show-non-ok-locations  %s '''

then = time.time()
print >> sys.stderr, then
for fileType in typeList:
    uType = fileType.upper()
    print >> sys.stderr, 'type:', uType

    folder = folders.get(uType, newFolder)

    cmd = datacat % (mode, uType, runId, folder)
    print >> sys.stderr, cmd
    fileName = os.popen(cmd).read().strip()

    if not fileName:
        print >> sys.stderr, "Couldn't get file name for %s" % fileType
        sys.exit(1)
        pass
    print >> sys.stderr, fileName

    version = fileNames.version(fileName)
    variables.setVar(fileType, 'ver', version)
    variables.setVar(fileType, 'fileName', fileName)

    now = time.time()
    print >> sys.stderr, now - then
    then = now
    continue


mootKey, mootAlias = acqQuery.query([runNumber], ['moot_key', 'moot_alias'])[runNumber]
pipeline.setVariable('mootKey', mootKey)
pipeline.setVariable('mootAlias', mootAlias)


# check that the chunks aren't crazy
chunks = finders.findAndReadChunkLists(runId)
chunkHeaders = [chunkData['headerData'] for chunkId, chunkData in chunks]
testResult = chunkTester.verifyList(chunkHeaders)
if not testResult:
    print >> sys.stderr, 'Run %s has bad crazy chunks.' % runId
    status |= 1
    sys.exit(status)
    pass
tStart, tStop = testResult
pipeline.setVariable('tStart', '%.17g' % tStart)
pipeline.setVariable('tStop', '%.17g' % tStop)
