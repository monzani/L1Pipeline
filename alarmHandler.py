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

realInFile = files[level][fileType]
stagedInFile = staged.stageIn(realInFile)

realAlarmFile = files[level][alarmFileType]
stagedAlarmFile = staged.stageOut(realAlarmFile)

workDir = os.path.dirname(stagedAlarmFile)

python = config.python
app = config.apps['alarmHandler']
configFile = config.alarmConfigs[fileType]

cmd = '''
cd %(workDir)s
%(python)s %(app)s -c %(configFile)s -o %(stagedAlarmFile)s %(stagedInFile)s
''' % locals()

status = runner.run(cmd)
if status: finishOption = 'wipe'

status |= staged.finish(finishOption)

registerPrep.prep(alarmFileType, realAlarmFile)

sys.exit(status)
