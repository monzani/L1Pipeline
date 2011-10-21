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

realFt2File = fileNames.fileName('ft2', dlId, runId, next=False)
stagedFt2File = staged.stageIn(realFt2File)

realVerifyFt2File = fileNames.fileName('verifyFt2Error', dlId, runId, next=True)
verifyFt2File = staged.stageOut(realVerifyFt2File)

workDir = os.path.dirname(verifyFt2File)
l1Setup = config.l1Setup
instDir = config.L1Build
glastExt = config.glastExt
             
package = config.packages['TestReport']
app = config.apps['ft2Verify']
truncation = config.verifyOptions['Truncation']

cmd = '''
cd %(workDir)s
export INST_DIR=%(instDir)s 
export GLAST_EXT=%(glastExt)s
source %(l1Setup)s
%(app)s -f %(stagedFt2File)s -x %(verifyFt2File)s -t %(truncation)s
''' % locals()

status = runner.run(cmd)
if status: finishOption = 'wipe'

status |= staged.finish(finishOption)

if not status:
    registerPrep.prep('verifyFt2Error', realVerifyFt2File)
    pass

sys.exit(status)
