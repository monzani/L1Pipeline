#!/afs/slac/g/glast/isoc/flightOps/rhel3_gcc32/ISOC_PROD/bin/shisoc --add-env=oracle11 python2.5

import os
import sys

import config

import GPLinit

import acqQuery
import fileNames
import runner
import stageFiles
import registerPrep

head, dlId = os.path.split(os.environ['DOWNLINK_RAWDIR'])
if not dlId: head, dlId = os.path.split(head)
runId = os.environ['RUNID']
chunkId = os.environ.get('CHUNK_ID') # might not be set
crumbId = os.environ.get('CRUMB_ID') # might not be set
idArgs = (dlId, runId, chunkId, crumbId)

if chunkId is None:
    level = 'run'
    next = True
else:
    if crumbId is None:
        level = 'chunk'
    else:
        level = 'crumb'
        pass
    next = False
    pass

fileType = os.environ['fileType']

staged = stageFiles.StageSet(excludeIn=config.excludeIn)
finishOption = config.finishOption

evtClassDefsPython = config.packages['evtClassDefs']['python']

stSetup = config.stSetup
#stSetup = config.packages['fitsGen']['setup']
app = os.path.join('$FITSGENROOT', '$CMTCONFIG', 'makeFT1_kluge.exe')

realMeritFile = fileNames.fileName('merit', *idArgs)
stagedMeritFile = staged.stageIn(realMeritFile)

realFt1File = fileNames.fileName(fileType, next=next, *idArgs)
stagedFt1File = staged.stageOut(realFt1File)

workDir = os.path.dirname(stagedFt1File)

tCuts = config.ft1Cuts
classifier = config.ft1Classifier

runNumber = int(os.environ['runNumber'])
tStart, tStop = acqQuery.runTimes(runNumber)

dictionary = config.ft1Dicts[fileType[:3]]

if level == 'run':
    version = fileNames.version(realFt1File)
else:
    version = 0
    pass

cmd = '''
cd %(workDir)s
echo pfiles=[$PFILES]
source %(stSetup)s
PYTHONPATH=%(evtClassDefsPython)s:$PYTHONPATH ; export PYTHONPATH
echo pfiles=[$PFILES]
%(app)s rootFile=%(stagedMeritFile)s fitsFile=%(stagedFt1File)s TCuts=%(tCuts)s event_classifier="%(classifier)s" tstart=%(tStart).17g tstop=%(tStop).17g dict_file=%(dictionary)s file_version=%(version)s
''' % locals()

status = runner.run(cmd)
if status: finishOption = 'wipe'

status |= staged.finish(finishOption)

if level == 'run' and not status: registerPrep.prep(fileType, realFt1File)

sys.exit(status)
