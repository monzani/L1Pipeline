#!/afs/slac/g/glast/isoc/flightOps/rhel3_gcc32/ISOC_PROD/bin/shisoc python2.5

import os
import sys

import config

import GPLinit

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

outFileType = fileType + 'Dist'
realOutFile = fileNames.fileName(outFileType, dlId, runId)
stagedOutFile = staged.stageOut(realOutFile)

workDir = os.path.dirname(stagedInFile)

app = config.apps['alarmPostProcessor']

configFile = config.alarmPostProcessorConfigs['fileType']

cmd = '%(app)s -c %(configFile)s -o %(stagedOutFile)s %(stagedInFile)s' % locals()

status = runner.run(cmd)

status |= staged.finish(finishOption)

if not status: registerPrep.prep(outFileType, realOutFile)

sys.exit(status)
