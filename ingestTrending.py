#!/afs/slac/g/glast/isoc/flightOps/rhel6_gcc44/ISOC_PROD/bin/shisoc python2.6

import os
import sys

import config

import GPLinit

import fileNames
import runner
import stageFiles

staged = stageFiles.StageSet(excludeIn=config.excludeIn)
finishOption = config.finishOption

head, dlId = os.path.split(os.environ['DOWNLINK_RAWDIR'])
if not dlId: head, dlId = os.path.split(head)
runId = os.environ['RUNID']
reportType = os.environ['reportType']

#app = config.ingestor[reportType]
app = config.trendIngestor

realInFile = fileNames.fileName(reportType, dlId, runId)
stagedInFile = staged.stageIn(realInFile)

workDir = os.path.dirname(stagedInFile)

#version = fileNames.version(realInFile)
version = os.environ['L1TrendVersion']

if config.testMode:
    db = 'dev'
else:
    db = 'prod'
    pass

processes = {
    'calTrend': 'CalPed',
    'digiTrend': 'Digi',
    'fastMonTrend': 'FastMon',
    'meritTrend': 'Merit',
    'reconTrend': 'Recon',
    'tkrTrend': 'TkrMon',
    }
process = processes.get(reportType, 'UnknownProcess')

timeBins = {
    15: "15secs",
    300: "5mins",
    1000000000: "run"
    }
tdBin = timeBins.get(config.tdBin[reportType], 'UnknownTimeBin')

cmd = '''
cd %(workDir)s
%(app)s %(stagedInFile)s %(version)s %(db)s %(process)s %(tdBin)s
''' % locals()

status = runner.run(cmd)
if status: finishOption = 'wipe'

status |= staged.finish(finishOption)

sys.exit(status)
