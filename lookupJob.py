import os
import sys
import time

import config
import variables

runId = os.environ['RUNID']

#location = 'SLAC_XROOT'
#locOpt = ' --site %s ' % location
 
fileTypes = os.environ['fileTypes']
typeList = fileTypes.split(',')

newFolder = os.environ['dataCatDir']
oldFolder = '/Data/Flight/Level1/LPA'
folders = {
    'DIGI': oldFolder,
    'MAGIC7L1': oldFolder,
    }

datacat = '''/afs/slac.stanford.edu/u/gl/glast/datacat/prod/datacat find --group %s --filter 'Name=="%s"'  --show-unscanned-locations   --show-non-ok-locations  %s '''

then = time.time()
print >> sys.stderr, then
for fileType in typeList:
    uType = fileType.upper()
    print >> sys.stderr, 'type:', uType

    folder = folders.get(uType, newFolder)

    cmd = datacat % (uType, runId, folder)
    print >> sys.stderr, cmd
    fileName = os.popen(cmd).read().strip()

    variables.setVar(fileType, 'fileName', fileName)

    now = time.time()
    print >> sys.stderr, now - then
    then = now
    continue
