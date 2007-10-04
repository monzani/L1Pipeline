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

level = 'run'

dlId = os.environ['DOWNLINK_ID']
runId = os.environ['RUNID']
files = fileNames.setup(dlId, runId)

staged = stageFiles.StageSet()
finishOption = config.finishOption

fileType = os.environ['fileType']

realInFile = files[level][fileType]
stagedInFile = staged.stageIn(realInFile)

workDir = os.path.dirname(stagedInFile)
#os.chdir(workDir)

alarmParser.doAlarms(stagedInFile, fileType)

status = staged.finish(finishOption)

registerPrep.prep(fileType, realInFile)

sys.exit(status)
