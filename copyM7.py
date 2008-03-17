#!/afs/slac/g/glast/isoc/flightOps/rhel3_gcc32/ISOC_PROD/bin/shisoc python2.5

import sys
import os

import config

import GPLinit

import fileNames
import registerPrep
import stageFiles

status = 0
finishOption = config.finishOption

head, dlId = os.path.split(os.environ['DOWNLINK_RAWDIR'])
if not dlId: head, dlId = os.path.split(head)
runId = os.environ['RUNID']

fileType = 'magic7'

staged = stageFiles.StageSet()

realInFile = os.path.join(os.environ['DOWNLINK_RAWDIR'], 'magic7_%s.txt' % dlId)
stagedInFile = staged.stageIn(realInFile)

#outDir = fileNames.fileName(None, dlId, runId)
#outBase = os.path.basename(realInFile)
realOutFile = fileNames.fileName(fileType, dlId, runId)

if not status: status |= stageFiles.copy(stagedInFile, realOutFile)

if status: finishOption = 'wipe'
status |= staged.finish(finishOption)

if not status: registerPrep.prep(fileType, realOutFile)

sys.exit(status)
