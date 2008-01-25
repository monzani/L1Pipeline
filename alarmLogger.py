#!/afs/slac/g/glast/isoc/flightOps/rhel3_gcc32/ISOC_PROD/bin/shisoc python2.5

import os
import sys

import GPLinit

import config

import alarmParser
import fileNames
import registerPrep
import runner
import stageFiles

head, dlId = os.path.split(os.environ['DOWNLINK_RAWDIR'])
if not dlId: head, dlId = os.path.split(head)
runId = os.environ['RUNID']

staged = stageFiles.StageSet()
finishOption = config.finishOption

fileType = os.environ['fileType']

realInFile = fileNames.fileName(fileType, dlId, runId)
stagedInFile = staged.stageIn(realInFile)

workDir = os.path.dirname(stagedInFile)

alarmParser.doAlarms(stagedInFile, fileType, runId)

status = staged.finish(finishOption)

registerPrep.prep(fileType, realInFile)

sys.exit(status)
