#!/afs/slac/g/glast/isoc/flightOps/rhel5_gcc41/ISOC_PROD/bin/shisoc python2.6

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

staged = stageFiles.StageSet(excludeIn=config.excludeIn)
finishOption = config.finishOption

fileType = os.environ['fileType']

realInFile = fileNames.fileName(fileType, dlId, runId)
stagedInFile = staged.stageIn(realInFile)

outFileType = fileType + 'Dist'
realOutFile = fileNames.fileName(outFileType, dlId, runId, next=True)
stagedOutFile = staged.stageOut(realOutFile)

workDir = os.path.dirname(stagedInFile)
python = config.python

app = config.apps['alarmPostProcessor']

configFile = config.alarmPostProcessorConfigs[fileType]

cmd = '%(python)s %(app)s -c %(configFile)s -o %(stagedOutFile)s %(stagedInFile)s' % locals()

status = runner.run(cmd)

status |= staged.finish(finishOption)

if not status: registerPrep.prep(outFileType, realOutFile)

sys.exit(status)
