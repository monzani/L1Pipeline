#!/afs/slac/g/glast/isoc/flightOps/rhel5_gcc41/ISOC_PROD/bin/shisoc python2.6

import os
import sys

import config

import GPLinit

import errorParser
import fileNames
import registerPrep
import runner
import stageFiles

head, dlId = os.path.split(os.environ['DOWNLINK_RAWDIR'])
if not dlId: head, dlId = os.path.split(head)
runId = os.environ['RUNID']

staged = stageFiles.StageSet(excludeIn=config.excludeIn)
finishOption = config.finishOption

fileType = os.environ['fileType']

realInFile = fileNames.fileName(fileType, dlId, runId)
stagedInFile = staged.stageIn(realInFile)

workDir = os.path.dirname(stagedInFile)

errorParser.doErrors(stagedInFile, fileType, runId)

status = staged.finish(finishOption)

sys.exit(status)
