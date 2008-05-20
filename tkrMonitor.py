#!/afs/slac/g/glast/isoc/flightOps/rhel3_gcc32/ISOC_PROD/bin/shisoc python2.5

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

staged = stageFiles.StageSet()
finishOption = config.finishOption

realInFile = fileNames.fileName('tkrAnalysis', dlId, runId, chunkId, crumbId)
stagedInFile = staged.stageIn(realInFile)

realMonFile = fileNames.fileName('tkrMonitor', dlId, runId, chunkId, crumbId, next=True)
stagedMonFile = staged.stageOut(realMonFile)
realAlarmFile = fileNames.fileName('tkrAlarm', dlId, runId, chunkId, crumbId, next=True)
stagedAlarmFile = staged.stageOut(realAlarmFile)
realReportFile = fileNames.fileName('tkrReport', dlId, runId, chunkId, crumbId, next=True)
stagedReportFile = staged.stageOut(realReportFile)

workDir = os.path.dirname(stagedMonFile)

htmlBase = '%s_tkrReport' % runId
htmlDir = os.path.join(workDir, htmlBase)

logBase = '%s_tkrReport.log' % runId
logFile = os.path.join(workDir, logBase)

python = config.python
app = config.apps['tkrMonitor']
cmtScript = config.packages['calibTkrUtil']['setup']

cmd = """
cd %(workDir)s
source %(cmtScript)s
/afs/slac.stanford.edu/g/glast/ground/GLAST_EXT/rh9_gcc32opt/python/2.5.1/bin/python2.5 %(app)s %(stagedInFile)s %(stagedMonFile)s %(htmlDir)s %(stagedAlarmFile)s %(logFile)s
touch %(stagedAlarmFile)s
""" % locals()

status = runner.run(cmd)
if status: finishOption = 'wipe'

if not status:
    tkrReport = tarfile.open(stagedReportFile, 'w')
    tkrReport.add(htmlDir, htmlBase)
    tkrReport.close()
    pass

status |= staged.finish(finishOption)

if not status: registerPrep.prep('tkrMonitor', realMonFile)

sys.exit(status)
