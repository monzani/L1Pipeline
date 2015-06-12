#!/afs/slac/g/glast/isoc/flightOps/rhel6_gcc44/ISOC_PROD/bin/shisoc python2.6

import sys
import os

import config

import GPLinit

import fileNames
import fileOps
import registerPrep
import stageFiles

status = 0
finishOption = config.finishOption

head, dlId = os.path.split(os.environ['DOWNLINK_RAWDIR'])
if not dlId: head, dlId = os.path.split(head)
runId = os.environ['RUNID']

fileType = 'magic7Hp'

staged = stageFiles.StageSet(excludeIn=config.excludeIn)

realInFile = os.path.join(os.environ['DOWNLINK_RAWDIR'], 'magic7_%s.txt' % dlId)
stagedInFile = staged.stageIn(realInFile)

#outDir = fileNames.fileName(None, dlId, runId)
#outBase = os.path.basename(realInFile)
realOutFile = fileNames.fileName(fileType, dlId, runId, next=True)

if not status: status |= fileOps.copy(stagedInFile, realOutFile)

if status: finishOption = 'wipe'
status |= staged.finish(finishOption)

if not status: registerPrep.prep(fileType, realOutFile)

sys.exit(status)
