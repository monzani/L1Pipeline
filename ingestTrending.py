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

dlId = os.environ['DOWNLINK_ID']
runId = os.environ['RUNID']
reportType = os.environ['reportType']

app = config.ingestor[reportType]

files = fileNames.setup(dlId, runId)
realInFile = files['run'][reportType]
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
