#!/afs/slac/g/glast/isoc/flightOps/rhel5_gcc41/ISOC_PROD/bin/shisoc python2.6

"""@brief Process TKR analysis file.

@author W. Focke <focke@slac.stanford.edu>
"""

import os
import sys
import tarfile

import config

import GPLinit

import fileNames
import registerPrep
import runner
import stageFiles


head, dlId = os.path.split(os.environ['DOWNLINK_RAWDIR'])
if not dlId: head, dlId = os.path.split(head)
runId = os.environ['RUNID']
chunkId = os.environ.get('CHUNK_ID')
crumbId = os.environ.get('CRUMB_ID')

staged = stageFiles.StageSet(excludeIn=config.excludeIn)
finishOption = config.finishOption

realInFile = fileNames.fileName('tkrAnalysis', dlId, runId, chunkId, crumbId)
stagedInFile = staged.stageIn(realInFile)

realMonFile = fileNames.fileName('tkrMonitor', dlId, runId, chunkId, crumbId, next=True)
stagedMonFile = staged.stageOut(realMonFile)
realReportFile = fileNames.fileName('tkrReport', dlId, runId, chunkId, crumbId, next=True)
stagedReportFile = staged.stageOut(realReportFile)

workDir = os.path.dirname(stagedMonFile)

#realAlarmFile = fileNames.fileName('tkrAlarm', dlId, runId, chunkId, crumbId, next=True)
#stagedAlarmFile = staged.stageOut(realAlarmFile)
stagedAlarmFile = os.path.join(workDir, 'aintNoAlarmFile.xml')

htmlBase = '%s_tkrReport' % runId
htmlDir = os.path.join(workDir, htmlBase)

logBase = '%s_tkrReport.log' % runId
logFile = os.path.join(workDir, logBase)

python = config.python
app = config.apps['tkrMonitor']
l1Setup = config.l1Setup
instDir = config.L1Build
glastExt = config.glastExt

cmd = """
cd %(workDir)s
export INST_DIR=%(instDir)s 
export GLAST_EXT=%(glastExt)s
source %(l1Setup)s
%(python)s %(app)s %(stagedInFile)s %(stagedMonFile)s %(htmlDir)s %(stagedAlarmFile)s %(logFile)s
""" % locals()

#do nothing. TKR analysis is not working.
#status = runner.run(cmd)
#if status: finishOption = 'wipe'
#
#if not status:
#    tkrReport = tarfile.open(stagedReportFile, 'w')
#    tkrReport.add(htmlDir, htmlBase)
#    tkrReport.close()
#    pass

status = 0

if not status:
    tkrReport = tarfile.open(stagedReportFile, 'w')
    tkrReport.close()
    open(stagedMonFile,"w")
    pass

status |= staged.finish(finishOption)

if not status:
    registerPrep.prep('tkrMonitor', realMonFile)
    registerPrep.prep('tkrReport', realReportFile)
    # registerPrep.prep('tkrAlarm', realAlarmFile)
    pass

sys.exit(status)
