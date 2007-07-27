#!/afs/slac/g/glast/isoc/flightOps/rhel3_gcc32/ISOC_PROD/bin/shisoc python2.5

import os
import sys

import config

import GPLinit

import fileNames
import runner
import stageFiles

staged = stageFiles.StageSet()

dlId = os.environ['DOWNLINK_ID']
runId = os.environ['RUNID']
reportType = os.environ['reportType']

app = config.ingestor[reportType]

files = fileNames.setup(dlId, runId)
realInFile = files['run'][reportType]
stagedInFile = staged.stageIn(realInFile)

cmd = '%(app)s %(stagedInFile)s' % locals()

status = runner.run(cmd)

staged.finish()

sys.exit(status)
