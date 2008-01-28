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

#app = config.ingestor[reportType]
app = config.trendIngestor

realInFile = fileNames.fileName(reportType, dlId, runId)
stagedInFile = staged.stageIn(realInFile)

version = fileNames.version(realInFile)

if config.testMode:
    db = 'dev'
else:
    db = 'prod'
    pass

if 'cal' in reportType:
    process = 'CalPed'
elif 'digi' in reportType:
    process = 'Digi'
elif 'recon' in reportType:
    process = 'Recon'
    pass

tdBin = {15: "15secs", 300: "5mins"}[config.tdBin[reportType]]

cmd = '%(app)s %(stagedInFile)s %(version)s %(db)s %(process)s %(tdBin)s' % locals()

status = runner.run(cmd)
if status: finishOption = 'wipe'

status |= staged.finish(finishOption)

sys.exit(status)
