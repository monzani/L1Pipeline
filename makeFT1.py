#!/afs/slac/g/glast/isoc/flightOps/rhel3_gcc32/ISOC_PROD/bin/shisoc python2.5

import os
import sys

import config

import GPLinit

import fileNames
import runner
import stageFiles
import registerPrep

dicts = {
    'ft1': 'DEFAULT',
    'ls1': os.path.join(config.L1ProcROOT, 'data', 'LS1variables'),
    }

head, dlId = os.path.split(os.environ['DOWNLINK_RAWDIR'])
if not dlId: head, dlId = os.path.split(head)
runId = os.environ['RUNID']

fileType = os.environ['fileType']

staged = stageFiles.StageSet()
finishOption = config.finishOption

app = config.apps['makeFT1']

realMeritFile = fileNames.fileName('merit', dlId, runId)
stagedMeritFile = staged.stageIn(realMeritFile)
realFt1File = fileNames.fileName(fileType, dlId, runId, next=True)
stagedFt1File = staged.stageOut(realFt1File)

workDir = os.path.dirname(stagedFt1File)

tCuts = config.ft1Cuts

tStart = float(os.environ['tStart'])
tStop = float(os.environ['tStop'])

dictionary = dicts[fileType]

version = fileNames.version(realFt1File)

cmd = '''
cd %(workDir)s
%(app)s rootFile=%(stagedMeritFile)s fitsFile=%(stagedFt1File)s TCuts=%(tCuts)s event_classifier="Pass5_Classifier" tstart=%(tStart).17g tstop=%(tStop).17g dict_file=%(dictionary)s file_version=%(version)s
''' % locals()

status = runner.run(cmd)
if status: finishOption = 'wipe'

status |= staged.finish(finishOption)

if not status: registerPrep.prep(fileType, realFt1File)

sys.exit(status)
