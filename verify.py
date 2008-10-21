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

staged = stageFiles.StageSet(excludeIn=config.excludeIn)
finishOption = config.finishOption

realDigiFile = fileNames.fileName('digi', dlId, runId, next=False)
stagedDigiFile = staged.stageIn(realDigiFile)

realVerifyLogFile = fileNames.fileName('verifyLog', dlId, runId, next=True)
verifyLogFile = staged.stageOut(realVerifyLogFile)
realVerifyHistoFile = fileNames.fileName('verifyHisto', dlId, runId, next=True)
verifyHistoFile = staged.stageOut(realVerifyHistoFile)

workDir = os.path.dirname(verifyLogFile)

setupScript = config.cmtScript
app = config.apps['runVerify']
jobOption = config.verifyOption[completeness]

cmd = '''
cd %(workDir)s
source %(setupScript)s
%(app)s -d %(stagedDigiFile)s -x %(verifyLogFile)s -r %(verifyHistoFile)s %(jobOption)
''' % locals()

status = runner.run(cmd)
if status: finishOption = 'wipe'

status |= staged.finish(finishOption)

if not status:
    registerPrep.prep('verifyHisto', realVerifyHistoFile)
    registerPrep.prep('verifyLog', realVerifyLogFile)
    pass

sys.exit(status)
