#!/afs/slac/g/glast/isoc/flightOps/rhel3_gcc32/ISOC_PROD/bin/shisoc python2.5

import os
import sys

import GPLinit

import config

import fileNames
import registerPrep
import runner
import stageFiles

level = 'run'

dlId = os.environ['DOWNLINK_ID']
runId = os.environ['RUNID']
files = fileNames.setup(dlId, runId)

staged = stageFiles.StageSet()
finishOption = config.finishOption

fileType = os.environ['fileType']
alarmFileType = fileType + 'Alarm'
reportFileType = fileType + 'Report'

realInFile = files[level][fileType]
stagedInFile = staged.stageIn(realInFile)

realAlarmFile = files[level][alarmFileType]
stagedAlarmFile = staged.stageOut(realAlarmFile)

realReportFile = files[level][reportFileType]
stagedReportFile = staged.stageOut(realReportFile)

workDir = os.path.dirname(stagedAlarmFile)
#os.chdir(workDir)

python = config.python
app = config.apps['alarmHandler']
configFile = config.alarmConfigs[fileType]

reportBase = os.path.basename(stagedAlarmFile).split('.')[0]
brokenReportName = os.path.join(workDir, reportBase, 'html', 'index.html')

cmd = '''
cd %(workDir)s
%(python)s %(app)s -c %(configFile)s -o %(stagedAlarmFile)s -d %(workDir)s %(stagedInFile)s
mv %(brokenReportName)s %(stagedReportFile)s
''' % locals()

status = runner.run(cmd)
if status: finishOption = 'wipe'

status |= staged.finish(finishOption)

registerPrep.prep(reportFileType, realReportFile)

sys.exit(status)
