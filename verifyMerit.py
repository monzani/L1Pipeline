#!/afs/slac/g/glast/isoc/flightOps/rhel6_gcc44/ISOC_PROD/bin/shisoc python2.6

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
l1Setup = config.l1Setup
instDir = config.L1Build
glastExt = config.glastExt

package = config.packages['TestReport']
app = config.apps['meritVerify']
truncation = config.verifyOptions['Truncation']

cmd = '''
cd %(workDir)s
export INST_DIR=%(instDir)s 
export GLAST_EXT=%(glastExt)s
source %(l1Setup)s
%(app)s -f %(stagedMeritFile)s -x %(verifyMeritFile)s -t %(truncation)s
''' % locals()

status = runner.run(cmd)
if status: finishOption = 'wipe'

status |= staged.finish(finishOption)

if not status:
    registerPrep.prep('verifyMeritError', realVerifyMeritFile)
    pass

sys.exit(status)
