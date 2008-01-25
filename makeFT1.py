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
    'ls1': os.path.join(config.L1ProcROOT, 'LS1variables'),
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

tStart = float(os.environ['tStart'])
tStop = float(os.environ['tStop'])

dictionary = dicts[fileType]

stSetup = config.stSetup
makeFT1Setup = os.path.join('$FITSGENROOT', 'cmt', 'setup.sh')

cmd = '''
cd %(workDir)s
#source %(stSetup)s
#source %(makeFT1Setup)s
%(app)s rootFile=%(stagedMeritFile)s fitsFile=%(stagedFt1File)s TCuts=DEFAULT event_classifier="Pass5_Classifier" tstart=%(tStart).17g tstop=%(tStop).17g dict_file=%(dictionary)s
''' % locals()

status = runner.run(cmd)
if status: finishOption = 'wipe'

status |= staged.finish(finishOption)

registerPrep.prep(fileType, realFt1File)

sys.exit(status)
