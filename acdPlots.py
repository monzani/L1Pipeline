#!/afs/slac/g/glast/isoc/flightOps/rhel3_gcc32/ISOC_PROD/bin/shisoc python2.5

import sys
import os

import config

import GPLinit

import fileNames
import registerPrep
import runner
import stageFiles

status = 0
finishOption = config.finishOption

head, dlId = os.path.split(os.environ['DOWNLINK_RAWDIR'])
if not dlId: head, dlId = os.path.split(head)
runId = os.environ['RUNID']

staged = stageFiles.StageSet(excludeIn=config.excludeIn)

fileType = 'acdPlots'

realInFile = fileNames.fileName('digiHist', dlId, runId)
stagedInFile = staged.stageIn(realInFile)

realOutFile = fileNames.fileName(fileType, dlId, runId, next=True)
stagedOutFile = staged.stageOut(realOutFile)

app = config.apps['acdPlots']

libraryPath = config.libraryPath

cmd = '''
export LD_LIBRARY_PATH=%(libraryPath)s
%(app)s -i %(stagedInFile)s -t %(stagedOutFile)s
''' % locals()

status |= runner.run(cmd)

if status: finishOption = 'wipe'
status |= staged.finish(finishOption)

if not status: registerPrep.prep(fileType, realOutFile)

sys.exit(status)
