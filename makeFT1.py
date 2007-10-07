#!/afs/slac/g/glast/isoc/flightOps/rhel3_gcc32/ISOC_PROD/bin/shisoc python2.5

import os
import sys

import config

import GPLinit

import fileNames
import runner
import stageFiles
#import pipeline
import registerPrep

files = fileNames.setup(os.environ['DOWNLINK_ID'], os.environ['RUNID'])

staged = stageFiles.StageSet()
finishOption = config.finishOption

if staged.setupOK:
    workDir = staged.stageDir
else:
    workDir = files['dirs']['run']
    pass

app = config.apps['makeFT1']
#app = os.path.join('$FITSGENROOT', config.cmtConfig, 'makeFT1.exe')

stagedMeritFile = staged.stageIn(files['run']['merit'])
realFt1File = files['run']['ft1']
stagedFt1File = staged.stageOut(realFt1File)

tStart = float(os.environ['tStart'])
tStop = float(os.environ['tStop'])

stSetup = config.stSetup
makeFT1Setup = os.path.join('$FITSGENROOT', 'cmt', 'setup.sh')

cmd = '''
cd %(workDir)s
#source %(stSetup)s
#source %(makeFT1Setup)s
%(app)s rootFile=%(stagedMeritFile)s fitsFile=%(stagedFt1File)s TCuts=DEFAULT event_classifier="Pass5_Classifier" tstart=%(tStart).17g tstop=%(tStop).17g
''' % locals()

status = runner.run(cmd)
if status: finishOption = 'wipe'

status |= staged.finish(finishOption)

ft1Export = files['run']['ft1Export']
if os.path.lexists(ft1Export):
    os.remove(ft1Export)
    pass
os.symlink(os.path.basename(realFt1File), ft1Export)

fileType = 'FT1'
registerPrep.prep(fileType, realFt1File)

sys.exit(status)
