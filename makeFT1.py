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

fileType = os.environ['fileType']

staged = stageFiles.StageSet()
finishOption = config.finishOption

evtClassDefsPython = config.packages['evtClassDefs']['python']

stSetup = config.stSetup
#app = config.apps['makeFT1']
appSetup = os.path.join('$FITSGENROOT', 'cmt', 'setup.sh')
app = os.path.join('$FITSGENROOT', '$CMTCONFIG', 'makeFT1.exe')

realMeritFile = fileNames.fileName('merit', dlId, runId)
stagedMeritFile = staged.stageIn(realMeritFile)
realFt1File = fileNames.fileName(fileType, dlId, runId, next=True)
stagedFt1File = staged.stageOut(realFt1File)

workDir = os.path.dirname(stagedFt1File)

tCuts = config.ft1Cuts
classifier = config.ft1Classifier

tStart = float(os.environ['tStart'])
tStop = float(os.environ['tStop'])

dictionary = config.ft1Dicts[fileType]

version = fileNames.version(realFt1File)

cfitsioPath = config.cfitsioPath

cmd = '''
cd %(workDir)s
source %(stSetup)s
#source %(appSetup)s
PYTHONPATH=%(evtClassDefsPython)s:$PYTHONPATH ; export PYTHONPATH
#LD_LIBRARY_PATH=%(cfitsioPath)s:$LD_LIBRARY_PATH ; export LD_LIBRARY_PATH
%(app)s rootFile=%(stagedMeritFile)s fitsFile=%(stagedFt1File)s TCuts=%(tCuts)s event_classifier="%(classifier)s" tstart=%(tStart).17g tstop=%(tStop).17g dict_file=%(dictionary)s file_version=%(version)s
''' % locals()

status = runner.run(cmd)
if status: finishOption = 'wipe'

status |= staged.finish(finishOption)

if not status: registerPrep.prep(fileType, realFt1File)

sys.exit(status)
