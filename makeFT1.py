#!/afs/slac/g/glast/isoc/flightOps/rhel3_gcc32/ISOC_PROD/bin/shisoc --add-env=oracle11 python2.5

import os
import sys

import config

import GPLinit

import acqQuery
import fileNames
import meritFiles
import runner
import stageFiles
import registerPrep
import rounding

head, dlId = os.path.split(os.environ['DOWNLINK_RAWDIR'])
if not dlId: head, dlId = os.path.split(head)
runId = os.environ['RUNID']

fileType = os.environ['fileType']

staged = stageFiles.StageSet(excludeIn=config.excludeIn)
finishOption = config.finishOption

evtClassDefsPython = config.packages['evtClassDefs']['python']

stSetup = config.stSetup
app = os.path.join('$FITSGENROOT', '$CMTCONFIG', 'makeFT1_kluge.exe')
gtmktime = os.path.join('$DATASUBSELECTORROOT', '$CMTCONFIG', 'gtmktime.exe')

realMeritFile = fileNames.fileName('merit', dlId, runId)
stagedMeritFile = staged.stageIn(realMeritFile)
realFt2File =fileNames.fileName('ft2Seconds', dlId, runId)
stagedFt2File = staged.stageIn(realFt2File)

realFt1File = fileNames.fileName(fileType, dlId, runId, next=True)
stagedFt1File = staged.stageOut(realFt1File)

workDir = os.path.dirname(stagedFt1File)

tCuts = config.ft1Cuts
classifier = config.ft1Classifier

#tStart = float(os.environ['tStart'])
#tStop = float(os.environ['tStop'])
runNumber = int(os.environ['runNumber'])

# run start and stop from ACQSUMMARY
tStart, tStop = acqQuery.runTimes(runNumber)
print 'ACQSUMMARY:', tStart, tStop

# run start and stop from merit file
mStart, mStop = meritFiles.startAndStop(stagedMeritFile)
print 'merit:', mStart, mStop

#cutStart = mStart - config.ft1Pad
#cutStop = mStop + config.ft1Pad
cutStart = rounding.roundDown(mStart, config.ft1Digits)
cutStop = rounding.roundUp(mStop, config.ft1Digits)

dictionary = config.ft1Dicts[fileType]

version = fileNames.version(realFt1File)

cmtPath = config.stCmtPath
cfitsioPath = config.cfitsioPath

filter = 'LIVETIME>0'

tempFT1 = '%s/tmpFt1_1.fits' % workDir

cmd = '''
cd %(workDir)s
export CMTPATH=%(cmtPath)s
source %(stSetup)s
PYTHONPATH=%(evtClassDefsPython)s:$PYTHONPATH ; export PYTHONPATH
%(app)s rootFile=%(stagedMeritFile)s fitsFile=%(stagedFt1File)s TCuts=%(tCuts)s event_classifier="%(classifier)s" tstart=%(cutStart).17g tstop=%(cutStop).17g dict_file=%(dictionary)s file_version=%(version)s || exit 1
mv %(stagedFt1File)s %(tempFT1)s || exit 1
%(gtmktime)s overwrite=yes roicut=no scfile=%(stagedFt2File)s filter="%(filter)s" evfile=%(tempFT1)s outFile=%(stagedFt1File)s || exit 1
''' % locals()

status = runner.run(cmd)
if status: finishOption = 'wipe'

status |= staged.finish(finishOption)

if not status: registerPrep.prep(fileType, realFt1File)

sys.exit(status)
