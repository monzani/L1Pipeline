#!/afs/slac/g/glast/isoc/flightOps/rhel3_gcc32/ISOC_PROD/bin/shisoc python2.5

import os
import sys

import config
import GPLinit
import time

import fileNames
import pipeline
import registerPrep
import runner
import stageFiles


head, dlId = os.path.split(os.environ['DOWNLINK_RAWDIR'])
if not dlId: head, dlId = os.path.split(head)
runId = os.environ['RUNID']
completeness = os.environ['completeness']

staged = stageFiles.StageSet(excludeIn=config.excludeIn)
finishOption = config.finishOption

realDigiFile = fileNames.fileName('digi', dlId, runId, next=False)
stagedDigiFile = staged.stageIn(realDigiFile)

realVerifyLogFile = fileNames.fileName('verifyLog', dlId, runId, next=True)
verifyLogFile = staged.stageOut(realVerifyLogFile)
realVerifyHistoFile = fileNames.fileName('verifyHisto', dlId, runId, next=True)
verifyHistoFile = staged.stageOut(realVerifyHistoFile)

workDir = os.path.dirname(verifyLogFile)
l1Setup = config.l1Setup
instDir = config.L1Build
glastExt = config.glastExt

package = config.packages['TestReport']
app = config.apps['runVerify']
jobOption = config.verifyOptions[completeness] 
truncation = config.verifyOptions['Truncation']

verifyLock = fileNames.checkVerifyLock(runId)
if (verifyLock): 
    print >> sys.stderr, 'Unlinking %s ... ' % verifyLock
    os.unlink(verifyLock)

cmd = '''
cd %(workDir)s
export INST_DIR=%(instDir)s 
export GLAST_EXT=%(glastExt)s
source %(l1Setup)s
%(app)s -d %(stagedDigiFile)s -x %(verifyLogFile)s -r %(verifyHistoFile)s -t %(truncation)s %(jobOption)s
''' % locals()

status = runner.run(cmd)
if (status == 153 or status == 154): 
    process = pipeline.getProcess()
    streamPath = os.environ.get('PIPELINE_STREAMPATH')
    processInstance = os.environ.get('PIPELINE_PROCESSINSTANCE')
    timeStamp = time.ctime()
    content = 'Locked by %s %s pipk = %s at %s\n' % (process, streamPath, processInstance, timeStamp)
    fileNames.makeVerifyLock(runId, content)
    status = 0

if status: finishOption = 'wipe'

status |= staged.finish(finishOption)

if not status:
    registerPrep.prep('verifyHisto', realVerifyHistoFile)
    registerPrep.prep('verifyLog', realVerifyLogFile)
    pass

sys.exit(status)
