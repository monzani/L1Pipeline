#!/afs/slac/g/glast/isoc/flightOps/rhel3_gcc32/ISOC_PROD/bin/shisoc python2.5

import os
import sys

import config

import GPLinit

import fileNames
import runner
import stageFiles
import registerPrep

head, dlId = os.path.split(os.environ['DOWNLINK_RAWDIR'])
if not dlId: head, dlId = os.path.split(head)
runId = os.environ['RUNID']

fileType = os.environ['fileType']

staged = stageFiles.StageSet()
finishOption = config.finishOption

app = config.apps['compareDFm']

#input file
realDigiHist = fileNames.fileName('digiEor', dlId, runId)
stagedDigiHist = staged.stageIn(realDigiHist)
realFastHist = fileNames.fileName('fastMonHist', dlId, runId)
stagedFastHist = staged.stageIn(realFastHist)

#output
realOutFile = fileNames.fileName(fileType, dlId, runId, next=True)
stagedOutFile = staged.stageOut(realOutFile)

workDir = os.path.dirname(stagedOutFile)

cmd = '''
cd %(workDir)s
%(app)s %(stagedDigiHist)s %(stagedFastHist)s -o %(stagedOutFile)s
''' % locals()

status = runner.run(cmd)
if status: finishOption = 'wipe'

status |= staged.finish(finishOption)

if not status: registerPrep.prep(fileType, realOutFile)

sys.exit(status)