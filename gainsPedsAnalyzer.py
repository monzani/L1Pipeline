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
reportType = os.environ['reportType']

realInFile = fileNames.fileName(fileType, dlId, runId)
stagedInFile = staged.stageIn(realInFile)

outFileType = reportType
realOutFile = fileNames.fileName(outFileType, dlId, runId, next=True)
stagedOutFile = staged.stageOut(realOutFile)

workDir = os.path.dirname(stagedInFile)
python = config.python

app = config.apps[reportType]

cmd = '%(python)s %(app)s -o %(stagedOutFile)s %(stagedInFile)s' % locals()

status = runner.run(cmd)

status |= staged.finish(finishOption)

if not status: registerPrep.prep(outFileType, realOutFile)

sys.exit(status)
