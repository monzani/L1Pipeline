#!/afs/slac/g/glast/isoc/flightOps/rhel3_gcc32/ISOC_PROD/bin/shisoc --add-env=oracle11 python2.5

import os
import sys

import config

import GPLinit

import acqQuery
import fileNames
import runner
import stageFiles

staged = stageFiles.StageSet()
finishOption = config.finishOption

head, dlId = os.path.split(os.environ['DOWNLINK_RAWDIR'])
if not dlId: head, dlId = os.path.split(head)
runId = os.environ['RUNID']
reportType = os.environ['reportType']

#nMetStart = os.environ['tStart']
#nMetStop = os.environ['tStop']
nMetStart, nMetStop = acqQuery.runTimes(int(os.environ['runNumber']))

app = config.runIngestor

realInFile = fileNames.fileName(reportType, dlId, runId)
stagedInFile = staged.stageIn(realInFile)

version = os.environ['L1TrendVersion']

if config.testMode:
    db = 'dev'
else:
    db = 'prod'
    pass

fileType = reportType.upper()
cmd = '%(app)s %(stagedInFile)s %(version)s %(db)s %(reportType)s %(fileType)s %(nMetStart)s %(nMetStop)s' % locals()

status = runner.run(cmd)
if status: finishOption = 'wipe'

status |= staged.finish(finishOption)

sys.exit(status)
