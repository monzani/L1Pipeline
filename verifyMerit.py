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

realMeritFile = fileNames.fileName('merit', dlId, runId, next=False)
stagedMeritFile = staged.stageIn(realMeritFile)

realVerifyMeritFile = fileNames.fileName('verifyMeritError', dlId, runId, next=True)
verifyMeritFile = staged.stageOut(realVerifyMeritFile)

workDir = os.path.dirname(verifyMeritFile)

cmtPath = config.cmtPath

package = config.packages['TestReport']
setupScript = package['setup']
app = config.apps['meritVerify']
truncation = config.verifyOptions['Truncation']

cmd = '''
cd %(workDir)s
export CMTPATH=%(cmtPath)s
source %(setupScript)s
%(app)s -f %(stagedMeritFile)s -x %(verifyMeritFile)s -t %(truncation)s
''' % locals()

status = runner.run(cmd)
if status: finishOption = 'wipe'

status |= staged.finish(finishOption)

if not status:
    registerPrep.prep('verifyMeritError', realVerifyMeritFile)
    pass

sys.exit(status)
