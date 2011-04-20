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

realFt1File = fileNames.fileName('ft1', dlId, runId, next=False)
stagedFt1File = staged.stageIn(realFt1File)

realVerifyFt1File = fileNames.fileName('verifyFt1Error', dlId, runId, next=True)
verifyFt1File = staged.stageOut(realVerifyFt1File)

workDir = os.path.dirname(verifyFt1File)

cmtPath = config.cmtPath

package = config.packages['TestReport']
setupScript = package['setup']
app = config.apps['ft1Verify']
truncation = config.verifyOptions['Truncation']

cmd = '''
cd %(workDir)s
export CMTPATH=%(cmtPath)s
source %(setupScript)s
%(app)s -f %(stagedFt1File)s -x %(verifyFt1File)s -t %(truncation)s
''' % locals()

status = runner.run(cmd)
if status: finishOption = 'wipe'

status |= staged.finish(finishOption)

if not status:
    registerPrep.prep('verifyFt1Error', realVerifyFt1File)
    pass

sys.exit(status)
