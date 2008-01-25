#!/afs/slac/g/glast/isoc/flightOps/rhel3_gcc32/ISOC_PROD/bin/shisoc python2.5

import os
import sys

import config

import GPLinit

import fileNames
import runner
import stageFiles

staged = stageFiles.StageSet()
finishOption = config.finishOption

head, dlId = os.path.split(os.environ['DOWNLINK_RAWDIR'])
if not dlId: head, dlId = os.path.split(head)
runId = os.environ['RUNID']
reportType = os.environ['reportType']

app = config.ingestor[reportType]

realInFile = fileNames.fileName(reportType, dlId, runId)
stagedInFile = staged.stageIn(realInFile)

version = '0'

if config.testMode:
    db = 'dev'
else:
    db = 'prod'

cmd = '%(app)s %(stagedInFile)s %(version)s %(db)s' % locals()

status = runner.run(cmd)
if status: finishOption = 'wipe'

status |= staged.finish(finishOption)

sys.exit(status)
