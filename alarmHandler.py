#!/afs/slac/g/glast/isoc/flightOps/rhel3_gcc32/ISOC_PROD/bin/shisoc python2.5

import os
import sys

import config

import GPLinit

import fileNames
import registerPrep
import runner
import stageFiles

level = 'run'

head, dlId = os.path.split(os.environ['DOWNLINK_RAWDIR'])
if not dlId: head, dlId = os.path.split(head)
runId = os.environ['RUNID']

staged = stageFiles.StageSet(excludeIn=config.excludeIn)
finishOption = config.finishOption

fileType = os.environ['fileType']
defaultAlarmFileType = fileType + 'Alarm'
alarmFileType = os.environ.get('alarmFileType', defaultAlarmFileType)

realInFile = fileNames.fileName(fileType, dlId, runId)
stagedInFile = staged.stageIn(realInFile)

realAlarmFile = fileNames.fileName(alarmFileType, dlId, runId, next=True)
stagedAlarmFile = staged.stageOut(realAlarmFile)

workDir = os.path.dirname(stagedAlarmFile)

python = config.python

package = config.packages['Common']
setup = package['setup']

if fileType in ['fastMonError','verifyLog']:
    app = config.apps['errorHandler']
    exceptionArgs = ''
    refArgs = ''
else:
    app = config.apps['alarmHandler']
    exceptionFile = config.alarmExceptions[fileType]
    exceptionArgs = '-x %s' % exceptionFile
    refArgs = '-R %s' % config.alarmRefDir
    pass

configFile = config.alarmConfigs[fileType]

cmd = '''
cd %(workDir)s
source %(setup)s
%(python)s %(app)s -c %(configFile)s %(exceptionArgs)s %(refArgs)s -o %(stagedAlarmFile)s %(stagedInFile)s
''' % locals()

status = runner.run(cmd)
if status: finishOption = 'wipe'

status |= staged.finish(finishOption)

if not status: registerPrep.prep(alarmFileType, realAlarmFile)

sys.exit(status)
